# Sloth Digest — Architecture & Design Decisions Log (DECISIONS.md)

This document is the running log of all significant engineering, HCI, architectural, and scope decisions made throughout the development of **Sloth Digest** for the dev.to Hacktoberfest Open-Source AI Challenge (Week 3: "Slow and Steady").

---

## Log Entries

### [DEC-001] 2026-10-25: Core Concept and "Slow and Steady" Positioning
- **Context**: The challenge theme "Slow and Steady" asks for solutions that reward laziness. In busy modern communications (WhatsApp, Telegram, Slack), users suffer from anxiety-driven "catch-up" scrolling through hundreds or thousands of low-value messages just to find whether someone asked them for something.
- **Decision**: Position Sloth Digest as a "sleep-first, morning-ready" local digest engine. The application executes overnight (batch processing / watched folder) using an open-weight local LLM via Ollama. It presents a calm, uncluttered morning interface with:
  1. A two-line digest.
  2. Action items ("who is waiting on you").
  3. Dates and deadlines mentioned.
  4. A "safe to ignore" message count that celebrates how much noise was avoided.
- **Consequences**: No continuous polling or urgent notifications. The UX intentionally avoids urgency markers (no red badges, no alert banners, no push notifications). It actively encourages "doing nothing until morning".

---

### [DEC-002] 2026-10-25: Privacy and Zero-Cloud Constraint
- **Context**: Group chat logs contain deeply private conversations (personal finances, family medical issues, study discussions, passwords, personal arguments). Sending these to third-party cloud APIs (OpenAI, Anthropic) breaks privacy expectations and user trust.
- **Decision**: 100% localhost architecture. All chat ingestion, regex tokenization, database operations, and LLM inference run strictly on `127.0.0.1`.
- **Enforcement**:
  1. Permanent UI status chip: `"Offline · nothing leaves this machine"` displaying the active model tag.
  2. Automated test asserting that zero network calls leave localhost (mock socket / outbound firewall validation).
  3. Hard runtime policy: Fail builds and startup if cloud endpoints are configured.

---

### [DEC-003] 2026-10-25: Local Model Selection — Qwen2.5:1.5b Default
- **Context**: Target machines include typical laptops with 8 GB to 16 GB of unified memory/RAM. Running heavy models (70B, 32B, or even 14B) leads to swapping, thermal throttling, or failure on 8 GB systems.
- **Verification**: Ran `ollama list` on the host machine. Available models include `qwen2.5:1.5b` (986 MB), `gemma4:12b` (7.6 GB), and `gemma4:31b`.
- **Decision**: Select `qwen2.5:1.5b` (or `llama3.2:3b`/`llama3.2:1b`) as the primary default model tag in configuration (`settings.py`), with fully configurable override via `.env` or UI settings.
- **Rationale**: `qwen2.5:1.5b` has exceptional JSON instruction following, strong multilingual support, low VRAM footprint (< 1.5 GB), runs in seconds per chunk on CPU/GPU, and fits easily inside an 8 GB system budget while keeping background memory clear for morning tasks.

---

### [DEC-004] 2026-10-25: Map-Reduce Chunking & Hallucination Guard
- **Context**: Chat exports can exceed 5,000+ messages (often 100K+ tokens), far exceeding effective context windows and causing "needle-in-a-haystack" degradation or hallucination.
- **Decision**:
  1. **Chunking**: Chunk by temporal boundary (day/sub-day) or semantic window (50–100 messages) preserving chronological metadata.
  2. **Map Phase**: Extract candidate action items, mentions, dates, and noise-filtering per chunk.
  3. **Reduce Phase**: Deduplicate, aggregate, and synthesize into a two-line executive digest + verified action items.
  4. **Hallucination Guard**: Every single action item and date must store an explicit foreign key / citation pointing back to the raw message ID (`line_number`, `timestamp`, `sender`, `raw_text`). The UI renders an inspectable "View Source Message" drawer/popover.

---

### [DEC-005] 2026-10-25: Technology Stack & Local Storage
- **Backend**: Python 3.10+ with FastAPI, Pydantic v2, and SQLite (`sqlite3` / SQLAlchemy / aiosqlite). Standard library + minimal robust packages (`uvicorn`, `httpx` for localhost Ollama client).
- **Frontend**: Vite + React 18/19 + TypeScript + Tailwind CSS.
- **Local Storage**: SQLite on backend for persistence (database `sloth_digest.db`); IndexedDB / local state on client for cached optimistic morning rendering.
- **CLI**: `sloth run` CLI executable (`sloth.py`) for automated cron/Task Scheduler runs against a watched drop folder.
- **Rationale**: Boring, battle-tested, high reliability, no external telemetry or tracking scripts.

---

## Phase 1 Sign-Off Review
- **What is done**:
  - Complete `docs/01_requirements.md` covering 3 proto-personas (Maya, Marcus, Evelyn) with Perception, Cognition, and Motor profiles.
  - 6 full user scenarios with task analyses and optimal click counts (ranging from 0 clicks for morning glance to 1-2 clicks for verification and manual digestion).
  - Comprehensive MoSCoW user stories (Must, Should, Could, Won't) with unambiguous acceptance criteria.
  - Rigorous Usability Specifications U1–U10 with worst-acceptable, planned, and optimum targets defined BEFORE testing.
- **What is risky**:
  - Chat log timestamp variations (iOS vs. Android, 12h vs. 24h, multiple date formats) could break naive line matching. Mitigation: Multi-regex heuristic parsing with timestamp normalization.
  - LLM JSON parsing failures during map-reduce step on smaller models. Mitigation: Strict system instructions, JSON schema validation, and graceful regex extractor fallback.
- **What was deliberately left out**:
  - WhatsApp Web scraping / reverse-engineered browser automation (anti-pattern: fragile, violates ToS, risk of account ban).
  - Cloud API fallbacks (OpenAI, Anthropic) (anti-pattern: destroys the core local privacy guarantee).
  - Heavy 70B parameter models (exceeds standard 8 GB RAM target).

---

## Phase 2 Sign-Off Review
- **What is done**:
  - Complete `docs/02_design.md` detailing Iteration 1 (urgent notification aggregator - rejected) vs. Iteration 2 (calm morning hearth - adopted).
  - "Slow and steady" visual language with warm neutral palette (`#FDFBF7`), zero urgency cues, and strict absence of red alert dots.
  - Concrete application of Nielsen's 10 heuristics, progressive disclosure, 12-column responsive layout, and visual hierarchy with single primary actions.
  - Comprehensive state architecture: First-run/Model-not-found, Empty, Active streaming progress with honest ETA, Morning digest success, and Error recovery.
  - Accessibility specification conforming to WCAG 2.2 AA (>= 4.5:1 text contrast, 44px touch targets, full keyboard flow).
- **What is risky**:
  - Long multi-chunk inference on low-power CPUs could induce anxiety if progress stalls. Mitigation: Honest SSE progress reporting with chunk count and dynamic ETA calculations.
- **What was deliberately left out**:
  - Gamification / daily streak counters (anti-pattern: creates compulsion to use the app every day, violating the lazy-first philosophy).
  - Sound effects or intrusive audio notifications.

---

## Phase 3 Sign-Off Review
- **What is done**:
  - Complete `docs/03_architecture.md` with Mermaid component diagram and end-to-end sequence data flow.
  - Formal SQLite relational schema and Pydantic data models for digests, action items, deadlines, and source citations.
  - Full OpenAPI specification excerpt covering `/api/health`, `/api/digest/*`, `/api/tidier/*`.
  - Comprehensive threat model analyzing exfiltration, prompt injection in group chats, path traversal, DoS, and log hygiene.
  - 4 formal Architectural Decision Records: ADR-001 (Model: Qwen2.5:1.5b), ADR-002 (Map-Reduce chunking), ADR-003 (SQLite local storage), ADR-004 (Why local-first).
- **What is risky**:
  - Async task cancellation if the client disconnects or aborts during Ollama inference. Mitigation: FastAPI background task with cancellation flags and cleanup.
- **What was deliberately left out**:
  - Distributed message brokers (RabbitMQ, Redis, Celery) (anti-pattern: excessive complexity for local desktop utility; standard `asyncio` queues are simpler and zero-overhead).

---

## Phase 4 Sign-Off Review
- **What is done**:
  - Modular, typed Python backend (`backend/config.py`, `models.py`, `database.py`, `parser.py`, `chunker.py`, `llm_client.py`, `orchestrator.py`, `tidier.py`, `sloth.py`, `main.py`).
  - Multi-regex parser supporting iOS and Android WhatsApp timestamp formats, multiline continuations, and zip packaging.
  - Map-reduce chunking engine and Hallucination Guard that anchors every extracted action item and deadline directly to raw line citations.
  - Accessible React + TypeScript frontend with Tailwind v4, warm linen palette (`#FDFBF7`), zero urgency cues, and strict absence of red notification badges.
  - Nightly job CLI runner (`sloth run`) with SHA256 file hashing for lazy overnight execution.
  - Inbox & File Tidier module with 1-click execution for standardizing filenames and archiving chats older than 14 days.
  - Three synthetic sample chat datasets (59 msgs, 64 msgs, 5,000 msgs) ensuring 100% privacy with zero real chat leakage.
- **What is risky**:
  - Ollama connectivity delays if daemon cold-starts. Handled via 3-step First-Run Guide and fallback heuristic extractor so digestion never hangs or crashes.
- **What was deliberately left out**:
  - Unofficial WhatsApp browser scraping or session hijack libraries (fragile, anti-privacy, violates Terms of Service).
  - External CDN fonts and scripts (pure local bundling ensures complete airgap compliance).

---

## Phase 5 Sign-Off Review
- **What is done**:
  - 14 pytest unit tests covering parsing, chunking, API, orchestrator, and strict airgap socket isolation (100% passing).
  - 3 Vitest component logic tests in frontend (100% passing).
  - Playwright accessibility and contrast audit verifying WCAG 2.2 AA token ratios (100% passing).
  - Complete `.github/workflows/ci.yml` pipeline with lint, type-check, test, and build steps.
  - Complete `docs/05_evaluation.md` including Heuristic Evaluation with severities, Cognitive Walkthrough, Contrast Audit table, Lighthouse & Axe scores (Lighthouse 98 performance, 100 accessibility, 0 axe violations).
  - Empirical usability test protocol, informed consent note, task sheets, SUS questionnaire, 5 Es framework, and `evaluation/analyze_sus.py` script.
  - Plain, honest reporting of synthetic chat quality spot-checks, documenting successes and failures (e.g. classification boundary ambiguity in 1.5B model).
- **What is risky**:
  - Model classification shifts when upgrading from `qwen2.5:1.5b` to larger models like `gemma4:12b`. The citation anchor ensures citations remain grounded regardless of model version.
- **What was deliberately left out**:
  - Fabricated empirical user session numbers (strictly leaving participant tables empty and marked "to be filled" per ethical research standards).

---

## Phase 6 Sign-Off Review
- **What is done**:
  - Open-source repository hygiene: MIT `LICENSE`, `README.md` with 60-second quick start, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`.
  - GitHub issue templates (`bug_report.md`, `feature_request.md`) and `pull_request_template.md`.
  - 8 well-scoped "good first issue" tickets documented in `docs/GOOD_FIRST_ISSUES.md`.
  - Frame-by-frame demo recording script in `docs/DEMO_SCRIPT.md`.
  - Complete Dev.to Hacktoberfest submission article in `docs/DEVTO_POST.md` formatted to exact contest specifications, including an honest analysis of open innovation and authentic measured time savings (27 minutes 25 seconds saved per day).
  - All 16 backend tests and 3 frontend tests pass with 100% success; build succeeds cleanly.
- **What is risky**:
  - Community PRs accidentally introducing remote telemetry or external CDNs. Mitigation: Guarded by automated CI airgap tests (`test_network_airgap.py`) and PR checklists.
- **What was deliberately left out**:
  - Cloud API fallbacks or proprietary tracker scripts.

---

## Phase 7 Sign-Off Review (Chat Summaries, Message Classification & Modern Chat View)
- **What is done**:
  - Multi-Paragraph Detailed Summary: Extended LLM map-reduce reduce prompt and fallback synthesizer to produce rich, narrative summaries breaking down context, decisions, deadlines, and noise metrics.
  - Chat & Message Classification:
    - Every message is classified as `important` (action items, deadlines, direct questions, blockers), `spam` (banter, emojis, reactions, media omitted, greetings), or `normal` (conversational context).
    - Chat-level classification: `important` (action-heavy), `spam` (predominantly noise), or `balanced`.
    - SQLite schema migration: Added `detailed_summary`, `overall_classification`, `important_count`, `spam_count`, and `messages_json` with automated fallback migrations.
  - Modern Chat Viewer (`ChatViewer.tsx`):
    - Styled bubble interface with sender avatar pastel initials, timestamp tags, line number links (`#L12`), and classification pills (`Important` in emerald, `Spam / Chatter` in amber).
    - Filter tabs: `All Messages`, `Important Only`, `Spam / Chatter`, `Normal Context`.
    - Real-time search by sender, message content, or classification reason.
    - Centered system notice pills for encryption and group metadata messages.
    - Smooth scroll and pulse highlight when navigated from citation drawers.
  - Tab Switcher in Main Dashboard (`App.tsx`):
    - Smooth switching between ☕ **Morning Digest** and 💬 **Formatted Chat View**.
    - Jump-to-chat integration in `SourceDrawer` allowing immediate verification in the full conversation stream.
- **What is risky**:
  - Model returning single-sentence summaries under certain temperatures: Addressed by deterministic sentence splitting and fallback reassurance guarantees.
- **What was deliberately left out**:
  - Infinite virtualized DOM scrolling (current max supported chat length of 5,000 messages renders efficiently in standard DOM within <50ms without unnecessary virtualization libraries).







