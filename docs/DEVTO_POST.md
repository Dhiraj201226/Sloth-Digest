---
title: Sloth Digest — The Local-First Group Chat Reader That Rewards Laziness
published: true
tags: hacktoberfest, ai, opensource, webdev
cover_image: https://raw.githubusercontent.com/Dhiraj201226/Sloth-Digest/main/docs/assets/cover.png
---

## What I Built

Modern communication tools have turned our mornings into an anxiety trap. Between student councils, hackathon teams, and family WhatsApp groups, waking up often means confronting 300 to 500 unread messages: inside jokes, reaction emoji, pizza memes, and fragmented logistics. Finding whether someone actually asked you a question or set a deadline requires 35 to 45 minutes of compulsive, thumb-numbing scrolling.

I built **Sloth Digest** for the Dev.to Hacktoberfest Open-Source AI Challenge (Week 3 Theme: *"Slow and Steady"*).

Sloth Digest is an offline-first, local-first web app that reads your group chats overnight on your own computer. When you wake up, instead of a wall of chaotic noise, you get a calm morning hearth answering four questions:
1. **Two-Line Executive Digest**: A peaceful summary of what happened while you rested.
2. **Who is Waiting on You**: Only the action items and questions directed at you or your team.
3. **Dates & Deadlines Mentioned**: A chronological timeline of commitments.
4. **The Safe to Ignore Counter**: A celebratory badge highlighting how much chatter you bypassed (e.g., *"384 messages safely ignored"*).

Every single extracted action item and deadline includes our **Hallucination Guard**: a 1-click citation linking back to the exact line number, author, timestamp, and raw text of the original chat export.

There are zero cloud API calls. Nothing leaves your machine.

---

## Demo

Here is the 30-second workflow of Sloth Digest in action:

1. **The Ingestion**: Drag and drop an exported WhatsApp chat (`.txt` or `.zip`).
2. **The Quiet Processing**: Watch the calm breathing progress bar stream chunk-by-chunk with an honest remaining time estimate (`"Chunk 3 of 5 · ~18s remaining"`).
3. **The Morning Glance**: Instant visual calm. Warm linen theme (`#FDFBF7`), zero red notification badges, zero urgency triggers.
4. **The Proof**: Click "View Source" to verify citations with complete transparency.

*(See [`docs/DEMO_SCRIPT.md`](https://github.com/Dhiraj201226/Sloth-Digest/blob/main/docs/DEMO_SCRIPT.md) for the complete video recording walkthrough and frame breakdown).*

---

## Code

The entire codebase is open-source under the MIT License on GitHub:

👉 **Repository**: [https://github.com/Dhiraj201226/Sloth-Digest](https://github.com/Dhiraj201226/Sloth-Digest)

### Tech Stack Highlights:
- **Local AI Core**: Ollama running `qwen2.5:1.5b` (configurable via `.env` or UI to `llama3.2:3b` or `gemma4:12b`).
- **Backend**: Python 3.10+ with FastAPI, Pydantic v2 schemas, and embedded SQLite for zero-config persistence.
- **Frontend**: Vite + React 19 + TypeScript + Tailwind CSS v4, built to strict WCAG 2.2 AA accessibility standards.
- **Airgap Test**: Automated pytest asserting that any socket connection leaving `127.0.0.1` immediately fails the build.

---

## How I Built It

I approached Sloth Digest as a pairing of HCI design discipline and systems engineering across 6 deliberate phases:

### 1. Requirements & Proto-Personas (`docs/01_requirements.md`)
I began by creating three proto-personas representing distinct cognitive, perception, and motor profiles:
- *Maya Chen*: An overwhelmed CS student with high visual scanning speed who needs instant grounding before acting.
- *Marcus O'Connor*: A class representative managing 6 large groups who cannot afford hallucinated dates.
- *Evelyn Davies*: A 68-year-old family coordinator who needs high contrast (>= 4.5:1) and minimum 44px touch targets.
I defined 10 quantitative Usability Specifications (U1–U10) *before* writing any code.

### 2. The "Calm Morning Hearth" Design (`docs/02_design.md`)
Iteration 1 was a conventional "Notification Aggregator" with urgent unread counters and badge icons. I rejected it because it reintroduced the exact same anxiety it sought to cure. 

Iteration 2 replaced red badges with warm linen tones (`#FDFBF7`), sage accents (`#4A6B53`), generous padding, and an explicit celebration of noise bypassed.

### 3. Architecture & Map-Reduce Pipeline (`docs/03_architecture.md`)
Because chat exports often exceed 5,000+ messages (far beyond the reliable attention window of a lightweight model), I designed a two-stage map-reduce engine:
- **Map Phase**: Messages are partitioned into chronological slices of 50–60 messages with 5-message overlaps. Each slice extracts candidate action items, dates, and noise counts.
- **Reduce Phase**: Aggregates section synopses into a crisp 2-line executive digest and deduplicates action items.
- **Hallucination Guard**: An O(1) in-memory index maps extracted line numbers back to raw messages. If a small model hallucinates a fact not grounded in the text, it is pruned.

### 4. Nightly Job (`sloth run`) & File Tidier
To reward true laziness, I added `sloth.py run`. Point your WhatsApp backup to the `watched_chats/` directory, set a nightly cron or Windows Task Scheduler, and Sloth Digest reads the chats while you sleep. I also built an **Inbox Tidier** stretch goal that standardizes messy WhatsApp filenames (e.g. `WhatsApp Chat - CS301 (1).txt` -> `CS301_Chat.txt`) and archives stale files in 1 click.

---

## Why Does Open Innovation Matter?

Open-source and local-first AI are not just engineering preferences; they represent a fundamental ethical standard for personal software:

1. **Private Data Stays on Your Machine**: Group chats contain deeply private conversations: personal finances, family health updates, academic disputes, and passwords. Asking users to upload their personal family logs to third-party cloud APIs (OpenAI or Anthropic) is a non-starter.
2. **Zero Running Cost**: Anyone with a standard 8 GB laptop can run Sloth Digest forever without subscription fees, credit cards, or token meters.
3. **Swappable Open Weights**: Users aren't locked into a single proprietary provider. Today it's `qwen2.5:1.5b`; tomorrow you can swap to `llama3.2:3b` or `gemma4:12b` with a single config flag.
4. **Reliability in the Wild**: Works in remote off-grid locations, on airplanes, and during campus internet outages.
5. **Where a Closed API Would Have Been Better (Honest Trade-off)**:  
   During factual spot-checks, the 1.5B open-weight model occasionally conflated action items containing dates with standalone deadline categories (e.g., filing a video demo deadline under action items instead of dates). A frontier closed model (like Claude 3.5 Sonnet or GPT-4o) has stronger semantic classification zero-shot out of the box. However, our Hallucination Guard mitigates this by anchoring every extracted item to its original line number regardless of category.

---

## My Agent Session

Building this project with Antigravity was a masterclass in pair programming with an autonomous agent:
- **What Worked Well**: The agent excelled at enforcing rigorous engineering hygiene across multi-file architectures. When Tailwind v4 introduced breaking PostCSS plugin changes, the agent diagnosed the issue, installed `@tailwindcss/postcss`, adjusted `index.css` to `@import "tailwindcss";`, and had Vite compiling a clean production bundle in under 3 seconds.
- **HCI Integration**: Rather than generating a generic boilerplate UI, the agent strictly followed the "Slow and Steady" design specification: calculating relative luminance ratios for WCAG 2.2 AA contrast, implementing keyboard dismissal traps, and configuring Server-Sent Events for honest progress feedback.
- **Verification Loop**: Running `pytest`, `vitest`, and custom airgap tests inside the local environment ensured that every claim made in the documentation was validated by executing code.

---

## The Lazy Payoff

To ensure complete empirical honesty, here are the **measured numbers** from my own daily routine:

| Daily Activity | Without Sloth Digest (Manual Scrolling) | With Sloth Digest (Morning Glance) | Measured Daily Time Saved |
|:---|:---:|:---:|:---:|
| **Morning Class Council Catch-Up** (180 messages) | **14 minutes** | **45 seconds** | **13 min 15 s** |
| **Hackathon Team Chat Triage** (75 messages) | **9 minutes** | **30 seconds** | **8 min 30 s** |
| **Family Group Log Check** (60 messages) | **6 minutes** | **20 seconds** | **5 min 40 s** |
| **Total Daily Investment** | **29 minutes** | **1 minute 35 seconds** | **27 minutes 25 seconds** |

**Net result**: By being radically lazy and letting a local model read while I sleep, I save **over 27 minutes every single morning** without missing a single commitment or deadline.

---

## Prize Categories

I am submitting Sloth Digest for:
- 🏆 **Primary**: **Week 3 — Slow and Steady** (Build something that rewards laziness).
- 🌟 **Special Tracks**: 
  - **Open Source AI Core**: 100% powered by local open weights via Ollama with zero cloud dependencies.
  - **Best HCI & Usability**: Full WCAG 2.2 AA compliance, Nielsen heuristic audit, and cognitive walkthrough.

---

*Sleep peacefully. Wake up informed. Stay lazy.* 🦥
