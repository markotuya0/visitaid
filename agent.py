"""
VisitAid — Real-Time AI Eyes for the Visually Impaired
WeMakeDevs Vision Hackathon 2025

HOW TO RUN:
    uv run agent.py serve

HOW IT WORKS:
    1. This file starts an AI agent as an HTTP server
    2. When someone connects via Stream (camera + mic), the agent joins their call
    3. Gemini Realtime watches the camera feed and understands the scene
    4. ElevenLabs speaks responses, Deepgram listens for user voice input
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger("visitaid")

# Vision Agents core — the main building blocks
from vision_agents.core import Agent, AgentLauncher, User, Runner

# Plugins — each one connects to a different AI service
from vision_agents.plugins import getstream   # Stream video network
from vision_agents.plugins import gemini      # Google's AI brain (sees + talks)
from vision_agents.plugins import elevenlabs  # Natural-sounding voice output
from vision_agents.plugins import deepgram    # Voice input (hears the user)

# Load all API keys from .env file automatically
load_dotenv()

# Validate required API keys are present before anything else runs
REQUIRED_KEYS = {
    "STREAM_API_KEY": "https://getstream.io/dashboard/",
    "STREAM_API_SECRET": "https://getstream.io/dashboard/",
    "GOOGLE_API_KEY": "https://aistudio.google.com/apikey",
    "ELEVENLABS_API_KEY": "https://elevenlabs.io/app/settings/api-keys",
    "DEEPGRAM_API_KEY": "https://console.deepgram.com/",
}

missing = [
    f"  - {key}  → Get it from: {url}"
    for key, url in REQUIRED_KEYS.items()
    if not os.getenv(key)
]

if missing:
    logger.error("Missing API keys! The agent cannot start without these:")
    for line in missing:
        logger.error(line)
    logger.error("Copy .env.example to .env and fill in the values: cp .env.example .env")
    sys.exit(1)

# Read the agent's instructions from a separate file
instructions_path = Path("instructions.md")
if not instructions_path.exists():
    logger.error("instructions.md not found! The agent needs this file for its behavior rules.")
    sys.exit(1)

INSTRUCTIONS = instructions_path.read_text().strip()
if not INSTRUCTIONS:
    logger.error("instructions.md is empty! The agent needs behavior rules to function.")
    sys.exit(1)


async def create_agent(**kwargs) -> Agent:
    """
    This function defines WHAT the agent is — its brain, tools, and personality.
    It gets called once when the server starts.
    """

    return Agent(
        # The video network — handles the live camera connection
        edge=getstream.Edge(),

        # The agent's identity in the call
        agent_user=User(name="VisitAid", id="visitaid-agent"),

        # The agent's personality and behavior rules (loaded from instructions.md)
        instructions=INSTRUCTIONS,

        # The AI brain — Gemini Realtime natively sees video + speaks
        # fps=3 means it processes 3 video frames per second
        # Higher fps = more responsive but costs more API credits
        llm=gemini.Realtime(fps=3),

        # Processors run before the LLM to pre-process video frames
        processors=[],

        # Text-to-speech — converts Gemini's text responses into natural voice
        tts=elevenlabs.TTS(),

        # Speech-to-text — converts the user's voice into text for Gemini
        stt=deepgram.STT(),
    )


async def join_call(agent: Agent, call_type: str, call_id: str, **kwargs) -> None:
    """
    This function defines WHAT HAPPENS when someone connects to the agent.
    It runs every time a new video call starts.
    """

    if not call_type or not call_id:
        logger.warning("Invalid call request: call_type=%r, call_id=%r", call_type, call_id)
        return

    # Try to create the call, retry once on transient failure
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

            # Greet the user — also "wakes up" the agent since video alone
            # doesn't trigger responses (a Vision Agents quirk).
            # Retry once on failure, then fall back to a simpler message.
            greeting = (
                "VisitAid is active. I'm watching through your camera now. "
                "Tell me what you need, or ask me what's around you."
            )
            for attempt in range(2):
                try:
                    await agent.simple_response(greeting)
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


if __name__ == "__main__":
    # SDK provides /health (200 OK) and /ready endpoints out of the box
    Runner(AgentLauncher(
        create_agent=create_agent,
        join_call=join_call,
    )).cli()