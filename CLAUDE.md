# VisitAid — Claude Code Project Brain

## What This Project Is
A real-time AI assistant for visually impaired people.
A phone camera streams live video → Vision Agents SDK processes it → Gemini Realtime describes the scene and speaks responses.

## The Stack
- **Language:** Python 3.12
- **Package manager:** `uv` (NOT pip, NOT poetry — always use `uv`)
- **Core SDK:** `vision-agents` (by Stream)
- **AI Brain:** Gemini Realtime (via Google AI Studio) — handles vision, STT, and TTS natively
- **Video Network:** Stream edge (getstream.io)

## Project Structure
```
visitaid/
├── agent.py           ← main agent (~130 lines)
├── instructions.md    ← agent personality, hazard rules, emergency mode
├── pyproject.toml     ← dependencies (managed by uv)
├── Dockerfile         ← container build
├── docker-compose.yml ← local Docker dev
├── railway.toml       ← Railway cloud deployment
├── .env.example       ← API key template
└── .env               ← actual keys (never commit)
```

## Key Commands
```bash
uv run agent.py run          # start agent with browser demo UI
uv run agent.py serve        # start HTTP server (production)
uv add <package>             # install a new package
```

## How the Agent Works
```
Phone Camera → Stream Video Network → Gemini Realtime (sees + hears + speaks)
```
Gemini Realtime is a single multimodal model that handles video understanding,
speech recognition, and voice output all in one. No separate STT/TTS needed.

## Code Rules
- Always use `async/await` — Vision Agents is fully async
- Never hardcode API keys — always use `os.getenv()` or `load_dotenv()`
- Keep the instructions prompt in `instructions.md`, not inline in code
- FPS should stay at 3 or lower for Gemini (cost + performance)
