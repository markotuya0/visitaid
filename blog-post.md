---
title: I Built an AI That Sees the World for People Who Can't — in 48 Hours
published: false
tags: ai, hackathon, accessibility, python
cover_image:
---

# I Built an AI That Sees the World for People Who Can't — in 48 Hours

250 million people worldwide are visually impaired. Most assistive apps require tapping buttons, pointing cameras manually, and waiting for results. That's not how a sighted guide works. A guide watches continuously and speaks up when it matters.

So I built one.

**VisitAid** is a real-time AI assistant that watches through your phone camera and talks to you like a trusted guide. It warns about obstacles before you hit them, reads signs when you ask, and describes your full surroundings in an emergency.

I built it solo in 48 hours for the [WeMakeDevs Vision Hackathon](https://www.wemakedevs.org/) using the [Vision Agents SDK](https://github.com/AugieDoebling/vision-agents) by Stream.

## The Problem

Close your eyes for 10 seconds and try to walk across your room.

That moment of uncertainty — "is there something in front of me?" — is constant for visually impaired people. Existing tools like Be My Eyes or Seeing AI are helpful, but they're **reactive**: you point your camera, tap a button, wait for a response. They don't watch continuously. They don't warn you about the chair you're about to walk into.

I wanted to build something **proactive** — an AI that watches all the time and speaks up when it matters, without being asked.

## The Solution

VisitAid works like this:

```
Phone Camera  ->  Stream Video Network  ->  Gemini Realtime  ->  Voice Response
                                                |
                                       Sees video + hears voice
                                       in one multimodal model
```

1. You start a video session from your phone
2. The camera streams live to the VisitAid server via Stream's video network
3. Google's Gemini Realtime model watches the video at 3 frames per second
4. When it sees a hazard, it speaks immediately. When you ask a question, it answers.

The key insight: Gemini Realtime is a **multimodal model** — it processes video, audio input, and audio output in one model. No separate OCR service, no separate speech-to-text, no separate text-to-speech. One model does everything.

## The Tech Decisions (and Why)

### Why Vision Agents SDK?

I needed to connect a phone camera to an AI model with real-time audio. That's three hard problems: WebRTC video streaming, model orchestration, and bidirectional audio.

Vision Agents SDK handles all three. My entire agent is ~120 lines of Python. The SDK does the heavy lifting:

```python
async def create_agent(**kwargs) -> Agent:
    return Agent(
        edge=getstream.Edge(),          # Video network
        agent_user=User(name="VisitAid", id="visitaid-agent"),
        instructions=INSTRUCTIONS,       # Behavior rules
        llm=gemini.Realtime(fps=3),     # AI brain
        processors=[],
        tts=elevenlabs.TTS(),
        stt=deepgram.STT(),
    )
```

That's the entire agent definition. Stream handles the video connection, Gemini handles everything else.

### Why Gemini Realtime (not GPT-4o, not Claude)?

Gemini Realtime has native multimodal streaming. It processes video frames + audio in real-time in a single model call. GPT-4o Vision requires separate API calls per frame. For an accessibility tool where **latency means someone walks into a wall**, real-time streaming wins.

### Why 3 FPS?

Cost vs. responsiveness tradeoff. At 3 frames per second, the agent processes a new frame every ~330ms. That's fast enough to catch a chair in your path but cheap enough to run continuously. Higher FPS = more API credits burned per minute.

### Why Prompt Engineering Over Code?

The agent's behavior — hazard detection, text reading, emergency mode — is all defined in `instructions.md`, not in code. Why?

1. **Iteration speed.** I can change how the agent warns about obstacles without touching Python.
2. **No extra dependencies.** Gemini already sees objects, reads text, and understands scenes. I don't need YOLO for object detection or Tesseract for OCR — I just need to tell Gemini *when and how* to use abilities it already has.
3. **Behavior is nuanced.** "Warn about obstacles but don't repeat yourself, prioritize by distance, stay quiet when the scene is safe" — that's hard to code but easy to describe in natural language.

Here's a snippet of the hazard detection instructions:

```markdown
## Proactive Hazard Detection

You MUST proactively warn about hazards even when the user hasn't asked.

**Hazard warning format:**
- Immediate danger: "Warning: [object] directly ahead, very close. Stop."
- Nearby danger: "Careful: [object] to your [left/right], about [distance]."

**Rules:**
- Only warn about NEW hazards — do not repeat warnings for the same object
- If the scene is safe, stay quiet — do not narrate "all clear" constantly
```

## Features That Make It Stand Out

### 1. Proactive Hazard Detection
The agent warns about obstacles **without being asked**. Walking toward a chair? *"Warning: chair directly ahead, very close. Stop."* A cyclist approaching? *"Heads up: cyclist approaching from your left."*

### 2. Text Reading Mode
Say "read that" and the agent reads every piece of visible text — signs, labels, screens, handwriting. Exactly as written, not summarized.

### 3. Emergency Mode
Say "help" and the agent switches from concise 2-sentence responses to a full scene dump: landmarks, signs, people nearby, anything that helps identify your location. It stays in this mode until you say you're okay.

## What I Learned

### The 80/20 of AI Engineering
80% of the value came from **prompt design**, not code. The agent's behavior rules (99 lines of markdown) matter more than the server code (120 lines of Python). Knowing when to write code vs. when to write instructions is the most important AI engineering skill.

### Multimodal Models Change the Architecture
Before Gemini Realtime, building this would mean: separate video processing pipeline, separate speech-to-text, separate text-to-speech, separate object detection model, orchestration layer to coordinate everything. Now it's one model that handles all modalities. The architecture went from complex microservices to a single prompt.

### Accessibility is Underserved in AI
Most AI demos are "look at this cool chatbot." Very few are "this helps someone navigate the world." The accessibility space has real, unsolved problems where AI can make a genuine difference. If you're looking for a meaningful project, start here.

## What's Next

- **Mobile app** — currently requires a Stream video client; a dedicated iOS/Android app would make it accessible to anyone
- **Offline mode** — local models for areas without internet
- **Navigation integration** — combine with GPS for turn-by-turn walking directions
- **Multi-language support** — Gemini supports 40+ languages, the instructions just need translation

## Try It Yourself

```bash
git clone https://github.com/markotuya0/visitaid.git
cd visitaid
uv sync
cp .env.example .env  # Add your API keys
uv run agent.py serve
```

You need API keys from [Stream](https://getstream.io), [Google AI Studio](https://aistudio.google.com), [ElevenLabs](https://elevenlabs.io), and [Deepgram](https://deepgram.com).

---

Built for the [WeMakeDevs Vision Hackathon](https://www.wemakedevs.org/) using the [Vision Agents SDK](https://github.com/AugieDoebling/vision-agents) by Stream.

[GitHub Repo](https://github.com/markotuya0/visitaid) | [Demo Video](#)
