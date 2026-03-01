"""
VisitAid — Real-Time AI Eyes for the Visually Impaired

Usage: uv run agent.py serve
"""

import asyncio
import logging
import os
import ssl
import sys
from pathlib import Path

import certifi
from dotenv import load_dotenv

# Fix macOS missing SSL root certificates
os.environ.setdefault("SSL_CERT_FILE", certifi.where())
ssl.create_default_context().load_verify_locations(certifi.where())

from vision_agents.core import Agent, AgentLauncher, User, Runner
from vision_agents.plugins import getstream, gemini, elevenlabs, deepgram

logger = logging.getLogger("visitaid")

load_dotenv()

# --- Startup validation ---

REQUIRED_KEYS = {
    "STREAM_API_KEY": "https://getstream.io/dashboard/",
    "STREAM_API_SECRET": "https://getstream.io/dashboard/",
    "GOOGLE_API_KEY": "https://aistudio.google.com/apikey",
    "ELEVENLABS_API_KEY": "https://elevenlabs.io/app/settings/api-keys",
    "DEEPGRAM_API_KEY": "https://console.deepgram.com/",
}

missing = [
    f"  - {key}  -> Get it from: {url}"
    for key, url in REQUIRED_KEYS.items()
    if not os.getenv(key)
]

if missing:
    logger.error("Missing API keys! The agent cannot start without these:")
    for line in missing:
        logger.error(line)
    logger.error("Copy .env.example to .env and fill in the values: cp .env.example .env")
    sys.exit(1)

instructions_path = Path("instructions.md")
if not instructions_path.exists():
    logger.error("instructions.md not found! The agent needs this file for its behavior rules.")
    sys.exit(1)

INSTRUCTIONS = instructions_path.read_text().strip()
if not INSTRUCTIONS:
    logger.error("instructions.md is empty! The agent needs behavior rules to function.")
    sys.exit(1)


# --- Agent definition ---

async def create_agent(**kwargs) -> Agent:
    """Define the agent: its brain, voice, and behavior."""
    return Agent(
        edge=getstream.Edge(),
        agent_user=User(name="VisitAid", id="visitaid-agent"),
        instructions=INSTRUCTIONS,
        llm=gemini.Realtime(fps=3),
        processors=[],
        tts=elevenlabs.TTS(),
        stt=deepgram.STT(),
    )


# --- Call lifecycle ---

GREETING = (
    "VisitAid is active. I'm watching through your camera now. "
    "Tell me what you need, or ask me what's around you."
)


async def join_call(agent: Agent, call_type: str, call_id: str, **kwargs) -> None:
    """Handle an incoming video call: join, greet, and run until finished."""
    if not call_type or not call_id:
        logger.warning("Invalid call request: call_type=%r, call_id=%r", call_type, call_id)
        return

    # Register agent user with Stream before creating the call
    try:
        await agent.create_user()
    except Exception as e:
        logger.error("Failed to register agent user: %s", e)
        return

    # Create call with one retry on transient failure
    call = None
    for attempt in range(2):
        try:
            call = await agent.create_call(call_type, call_id)
            break
        except Exception as e:
            if attempt == 0:
                logger.warning("Failed to create call %s, retrying: %s", call_id, e)
                await asyncio.sleep(2)
            else:
                logger.error("Failed to create call %s after retry: %s", call_id, e)
                return

    try:
        async with agent.join(call):
            # Greeting wakes up the agent (video alone doesn't trigger responses)
            for attempt in range(2):
                try:
                    await agent.simple_response(GREETING)
                    break
                except Exception:
                    if attempt == 0:
                        logger.warning("Greeting failed, retrying in 2s...")
                        await asyncio.sleep(2)
                    else:
                        logger.warning("Greeting retry failed, continuing without greeting")

            await agent.finish()
    except Exception as e:
        logger.error("Call %s ended with error: %s", call_id, e)


# --- Entry point ---

if __name__ == "__main__":
    Runner(AgentLauncher(
        create_agent=create_agent,
        join_call=join_call,
    )).cli()
