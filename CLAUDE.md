# VisitAid — Claude Code Project Brain

## What This Project Is
A real-time AI assistant for visually impaired people.
A phone camera streams live video → Vision Agents SDK processes it → AI describes the scene and answers voice questions.

Built for the WeMakeDevs Vision Hackathon (deadline: Mar 1).

## The Stack
- **Language:** Python 3.12
- **Package manager:** `uv` (NOT pip, NOT poetry — always use `uv`)
- **Core SDK:** `vision-agents` (by Stream)
- **AI Brain:** Gemini Realtime (via Google AI Studio)
- **Object Detection:** YOLO via `ultralytics` plugin
- **Text Reading:** Moondream plugin
- **Voice Out:** ElevenLabs TTS
- **Voice In:** Deepgram STT
- **Video Network:** Stream edge (getstream.io)

## Project Structure
```
visitaid/
├── CLAUDE.md          ← you are here
├── .env               ← API keys (NEVER touch or expose this)
├── .gitignore
├── agent.py           ← main agent file (the core logic)
├── instructions.md    ← the agent's personality/behavior prompt
├── pyproject.toml     ← managed by uv automatically
└── .claude/
    └── skills/
        └── explain/
            └── SKILL.md   ← explains what was built after each step
```

## Key Commands
```bash
uv run agent.py serve        # start the agent server
uv add <package>             # install a new package
uv run agent.py --help       # see all options
```

## How the Agent Works (Mental Model)
```
Camera → Vision Agents SDK → [YOLO processor] → [Gemini Realtime] → ElevenLabs voice
                                                         ↑
                                               [Deepgram hears user]
```

## Code Rules
- Always use `async/await` — Vision Agents is fully async
- Never hardcode API keys — always use `os.getenv()` or `load_dotenv()`
- Keep the instructions prompt in `instructions.md`, not inline in code
- FPS should stay at 3 or lower for Gemini (cost + performance)
- Use `conf_threshold=0.5` minimum for YOLO (avoid false positives)

## After Every Change
After writing or modifying any code, always:
1. Explain what you just built in plain English (no jargon)
2. Explain WHY it works that way (the concept)
3. Explain what the user should see/hear when it runs
4. List any new API keys or installs needed
Use simple analogies. The developer is a frontend dev learning AI engineering.

## Hackathon Context
- Solo submission
- Judged on: impact, creativity, technical quality, real-time performance, UX, SDK usage
- Must use Vision Agents SDK prominently
- Demo video needed (60-90 seconds)
- Blog post needed for $500 prize
- Deadline: March 1