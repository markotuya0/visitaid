# VisitAid

**Real-time AI eyes for visually impaired people. Built in 48 hours for WeMakeDevs Vision Hackathon 2025. 154 lines of Python. Fully autonomous — no button presses, no tapping, no waiting.**

250 million people worldwide are visually impaired. Existing assistive tools require tapping, waiting, and looking at screens. VisitAid watches continuously through a phone camera and speaks in real-time — like having a trusted guide walking beside you.

> Built for the [WeMakeDevs Vision Hackathon](https://www.wemakedevs.org/) using the [Vision Agents SDK](https://github.com/AugieDoebling/vision-agents) by Stream.

<!-- Demo video: uncomment and replace URL when recorded
[![VisitAid Demo](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://youtu.be/VIDEO_ID)
-->

---

## What It Does

| Feature | How It Works |
|---------|-------------|
| **Scene Description** | Point your camera anywhere. Ask "what's around me?" and hear a spatial description. |
| **Hazard Detection** | Agent proactively warns about obstacles — chairs, stairs, vehicles — without being asked. |
| **Text Reading** | Say "read that" to hear signs, labels, screens, or handwriting read back exactly. |
| **Emergency Mode** | Say "help" and the agent gives a full detailed scene dump to help identify your location. |
| **Voice Conversation** | Ask any question about what the camera sees. The agent responds naturally. |

## Architecture

```
Phone Camera                                          User's Ears
     |                                                      ^
     v                                                      |
 [Stream Video Network]  -->  [Vision Agents SDK]  -->  [Gemini Realtime]
                                                            |
                                                     Understands scene,
                                                     speaks response via
                                                     built-in voice I/O
```

**How the pipeline works:**
1. Phone streams live video via Stream's edge network
2. Vision Agents SDK receives frames at 3 FPS
3. Gemini Realtime processes video + audio in one model
4. Gemini speaks responses directly back to the user

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Vision Agents](https://img.shields.io/badge/Vision_Agents_SDK-0.3.8-green)
![Gemini](https://img.shields.io/badge/Gemini-Realtime-orange?logo=google&logoColor=white)
![Stream](https://img.shields.io/badge/Stream-Video_Network-blue?logo=data:image/svg+xml;base64,)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker&logoColor=white)

| Component | Service | Role |
|-----------|---------|------|
| AI Brain | Gemini Realtime | Sees video, understands scenes, speaks responses |
| Video Network | Stream (getstream.io) | Connects phone camera to agent server |
| Voice Output | Gemini built-in | Natural speech synthesis |
| Voice Input | Gemini built-in | Speech recognition |
| Orchestration | Vision Agents SDK | Wires all components together |

## Quick Start

### Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- API keys (see below)

### 1. Clone and install

```bash
git clone https://github.com/markotuya0/visitaid.git
cd visitaid
uv sync
```

### 2. Set up API keys

```bash
cp .env.example .env
# Edit .env and add your keys
```

You need keys from:
- [Stream](https://getstream.io/dashboard/) — video network
- [Google AI Studio](https://aistudio.google.com/apikey) — Gemini
- [ElevenLabs](https://elevenlabs.io/app/settings/api-keys) — voice (fallback)
- [Deepgram](https://console.deepgram.com/) — speech recognition (fallback)

### 3. Run

```bash
uv run agent.py serve
```

The agent starts on `http://127.0.0.1:8000`. Connect via a Stream video client to start a session.

### Run with Docker

```bash
docker compose up
```

## Deploy to Railway

1. Push this repo to GitHub
2. Connect the repo on [Railway](https://railway.app/)
3. Add your API keys as environment variables
4. Railway auto-detects `railway.toml` and deploys

## Project Structure

```
visitaid/
├── agent.py           # Main agent — server, call handling, error recovery
├── instructions.md    # Agent personality, hazard rules, emergency mode
├── pyproject.toml     # Dependencies (managed by uv)
├── Dockerfile         # Container build
├── docker-compose.yml # Local Docker dev
├── railway.toml       # Railway cloud deployment
├── .env.example       # API key template with docs
└── .env               # Your actual keys (not in git)
```

## How It's Built

VisitAid is intentionally simple — one Python file, one instructions file, zero frameworks beyond the SDK. The complexity lives in the AI models, not the code.

- **`agent.py`** (154 lines) — Creates the agent, handles calls, retries on failure
- **`instructions.md`** (99 lines) — Defines how the agent behaves: safety-first hazard warnings, text reading format, emergency mode triggers, personality rules

The Vision Agents SDK handles all the hard parts: WebRTC video streaming, model orchestration, audio I/O, and call lifecycle.

## License

MIT

---

Built by [@markotuya0](https://github.com/markotuya0) for the WeMakeDevs Vision Hackathon 2025.

Powered by [Vision Agents SDK](https://github.com/AugieDoebling/vision-agents) by Stream.
