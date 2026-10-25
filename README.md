# 🦥 Sloth Digest

> **Slow and steady: rewards laziness by reading busy group chats overnight on your local machine so you wake up completely calm.**  
> Built for the **Dev.to Hacktoberfest Open-Source AI Challenge** (Week 3 Theme: *"Slow and Steady"*).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Hacktoberfest](https://img.shields.io/badge/Hacktoberfest-2026-orange.svg)](https://hacktoberfest.com/)
[![Privacy: 100% Offline](https://img.shields.io/badge/Privacy-100%25%20Offline-success.svg)](#privacy-guarantee)
[![WCAG 2.2 AA](https://img.shields.io/badge/WCAG-2.2%20AA%20Compliant-blue.svg)](docs/05_evaluation.md)
[![Tests: Passing](https://img.shields.io/badge/Tests-17%20Passed-brightgreen.svg)](#testing)

---

## The Problem
You belong to 15 busy group chats: hackathon teams, college project channels, student councils, and family groups. Over an evening, hundreds of messages accumulate: inside jokes, memes, fragmented planning, and reaction emoji.

You face a stressful choice:
1. **The Compulsive Catch-Up**: Spend 40 minutes scrolling through trivial banter just to find if someone asked you a question.
2. **The Passive Neglect**: Mute everything and risk missing a crucial deadline or assignment.

## The Solution: Radical Laziness
**Do nothing. Go to sleep.**

Sloth Digest processes your exported WhatsApp chats (`.txt` or `.zip`) overnight on your local machine using an open-weight model via Ollama. When you wake up, a serene, zero-urgency dashboard gives you:
1. **A Two-Line Morning Digest** — What happened while you rested.
2. **Who is Waiting on You** — Action items and requests directly concerning you.
3. **Dates & Deadlines Mentioned** — Chronological commitments.
4. **The Safe to Ignore Counter** — Celebrating how much noise you avoided (e.g. *"384 messages safely bypassed"*).

---

## 🔒 Privacy Guarantee: Zero Cloud Telemetry

- **100% Localhost**: Chat parsing, database storage, and LLM inference run strictly on `127.0.0.1`.
- **Permanent Status Chip**: Fixed UI indicator displays `"Offline · nothing leaves this machine · [qwen2.5:1.5b]"`.
- **Automated Airgap Test**: Build fails if any socket attempts a non-localhost connection (`tests/test_network_airgap.py`).

---

## ⚡ 60-Second Quick Start

### Prerequisites
1. **Python 3.10+** and **Node.js 20+**.
2. **Ollama**: Download from [ollama.com](https://ollama.com).
3. Pull the default 1.5B model (fits comfortably in 8 GB RAM):
   ```bash
   ollama pull qwen2.5:1.5b
   ```

### 1. Clone & Setup
```bash
git clone https://github.com/Dhiraj201226/Sloth-Digest.git
cd Sloth-Digest

# Install Python backend requirements
pip install -r requirements.txt

# Build the frontend assets
cd frontend
npm install
npm run build
cd ..
```

### 2. Start the Local Server
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```
Open **`http://localhost:8000`** in your browser!

*(Optional: For frontend live reload during development, run `npm run dev` inside `frontend/` on `http://localhost:5173`)*.

---

## 🌙 Overnight Automation (`sloth run`)

For the ultimate lazy workflow:
1. Drop your exported chats into the `watched_chats/` folder before bed.
2. Schedule the nightly runner via cron or Windows Task Scheduler:
   ```bash
   python sloth.py run
   ```
3. In the morning, simply open the page. Your digest is already rendered and waiting for your coffee!

### 🧹 File & Inbox Tidier (Stretch Goal)
Messy chat export names like `WhatsApp Chat - CS301 (1).txt` cluttering your downloads?
Run:
```bash
python sloth.py tidy --apply
```
Or click the **Inbox Tidier** button in the web UI to standardize filenames and archive stale chats in 1 click.

---

## 🛡️ The Hallucination Guard

Small models can sometimes invent dates or tasks. Sloth Digest eliminates hallucinations through **hard citation grounding**:
- Every extracted action item and deadline records an exact foreign key to the source line number, timestamp, sender, and raw text.
- Click **"View Source"** on any card to slide open the source drawer and inspect the original chat text.
- If an item cannot be grounded in the text, it is discarded.

---

## 🧪 Testing & Verification

```bash
# Run backend pytest suite (parser, chunker, API, orchestrator, airgap test)
python -m pytest -v tests/

# Run frontend Vitest component logic suite
cd frontend && npm test && cd ..

# Run accessibility & WCAG contrast audit
python -m pytest tests/test_playwright_a11y.py

# Run factual quality spot-check against synthetic datasets
python evaluation/spot_check_quality.py
```

---

## 📚 Documentation Index

- [`docs/01_requirements.md`](docs/01_requirements.md) — Personas, 6 Scenarios, MoSCoW Stories, Usability Specifications U1–U10.
- [`docs/02_design.md`](docs/02_design.md) — Iteration 1 vs. 2, Nielsen Heuristics, 12-Column Grid, WCAG 2.2 AA.
- [`docs/03_architecture.md`](docs/03_architecture.md) — Mermaid Diagrams, Data Flow, SQLite Schema, Threat Model, ADRs.
- [`docs/05_evaluation.md`](docs/05_evaluation.md) — Heuristic Evaluation, Cognitive Walkthrough, Lighthouse/Axe, Usability Test Plan, Fact Spot-Checks.
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — Running log of all engineering & HCI decisions.
- [`docs/DEVTO_POST.md`](docs/DEVTO_POST.md) — Full Dev.to challenge submission post draft.

---

## 🤝 Contributing

Contributions are welcome! Check out our [Contributing Guide](CONTRIBUTING.md) and browse the [Good First Issues](docs/GOOD_FIRST_ISSUES.md).

## 📄 License

Distributed under the [MIT License](LICENSE).
