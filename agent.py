"""
VisitAid — Real-Time AI Eyes for the Visually Impaired
WeMakeDevs Vision Hackathon 2025

HOW TO RUN:
    uv run agent.py serve

HOW IT WORKS:
    1. This file starts an AI agent as an HTTP server
    2. When someone connects via Stream (camera + mic), the agent joins their call
    3. The agent watches their camera using Gemini (understanding scenes + objects)
    4. The agent speaks back using ElevenLabs and listens via Deepgram

NOTE: YOLO processor is disabled on Intel Macs (PyTorch compatibility issue).
      Gemini can still detect objects natively — it just won't have pre-labeled boxes.
      To enable YOLO, use Apple Silicon Mac or Linux with:
      uv add "vision-agents[ultralytics]"
"""

from pathlib import Path
from dotenv import load_dotenv

# Vision Agents core — the main building blocks
from vision_agents.core import Agent, AgentLauncher, User, Runner

# Plugins — each one connects to a different AI service
from vision_agents.plugins import getstream   # Stream video network
from vision_agents.plugins import gemini      # Google's AI brain (sees + talks)
from vision_agents.plugins import elevenlabs  # Natural-sounding voice output
from vision_agents.plugins import deepgram    # Voice input (hears the user)

# YOLO import disabled — uncomment on Apple Silicon or Linux:
# from vision_agents.plugins import ultralytics

# Load all API keys from .env file automatically
load_dotenv()

# Read the agent's instructions from a separate file
# (keeping prompts in .md files makes them easy to edit without touching code)
INSTRUCTIONS = Path("instructions.md").read_text()


async def create_agent(**kwargs) -> Agent:
    """
    This function defines WHAT the agent is — its brain, tools, and personality.
    It gets called once when the server starts.
    """

    # YOLO Processor — disabled on Intel Mac (PyTorch doesn't support macOS x86_64 + Python 3.12)
    # Uncomment on Apple Silicon or Linux:
    #
    # obstacle_detector = ultralytics.YOLOProcessor(
    #     model_path="yolo11n.pt",   # "n" = nano model (smallest, fastest)
    #     device="cpu",              # Change to "cuda" if you have an NVIDIA GPU
    #     conf_threshold=0.5,        # Only report detections with 50%+ confidence
    # )

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

        # Processors run BEFORE the LLM — they pre-process video frames
        # Currently empty on Intel Mac. Add obstacle_detector here when YOLO is enabled.
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

    # Create a "call" — Stream's term for a video session
    call = await agent.create_call(call_type, call_id)

    # Join the call and start processing audio + video
    async with agent.join(call):

        # Greet the user as soon as they connect
        # This also "wakes up" the agent — video alone doesn't trigger responses
        # The agent needs audio or text to start (a Vision Agents quirk)
        await agent.simple_response(
            "VisitAid is active. I'm watching through your camera now. "
            "Tell me what you need, or ask me what's around you."
        )

        # Keep the agent running until the call ends
        await agent.finish()


if __name__ == "__main__":
    # Wire everything together and start the HTTP server
    # After running `uv run agent.py serve`, the agent listens for incoming calls
    Runner(AgentLauncher(
        create_agent=create_agent,
        join_call=join_call
    )).cli()