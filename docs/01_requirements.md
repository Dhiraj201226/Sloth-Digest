# Sloth Digest — Phase 1: Requirements & Usability Specification

**Project**: Sloth Digest  
**Theme**: Dev.to Hacktoberfest Open-Source AI Challenge — Week 3: "Slow and Steady" (Rewarding Laziness)  
**Role**: Senior Software Engineer & Human-Computer Interaction (HCI) Practitioner  
**Status**: Completed  
**Last Updated**: 2026-10-25  

---

## 1. Executive Summary & Problem Framing

Modern communication tools (WhatsApp, Telegram, Signal, Discord, Slack) create an overwhelming cognitive tax. Users find themselves trapped in 10 to 30 active group chats—class cohorts, project squads, hobby clubs, and extended family circles. Over a single evening or workday, hundreds of unread messages accumulate: memes, banter, fragmented planning, and reaction emoji. 

Users face a painful dilemma:
1. **The Compulsive Catch-Up**: Spend 35–50 minutes scrolling through trivial banter out of fear of missing a critical deadline, a direct query ("who has the lab keys?"), or a family event.
2. **The Passive Neglect**: Mute all notifications, leading to missed assignments, broken commitments, and social friction.

**Sloth Digest** solves this through radical laziness. Instead of real-time vigilance, the user does nothing. Overnight, a local, open-weight language model (running completely offline on localhost via Ollama) processes chat exports from a watched folder or one-click drop. In the morning, the user opens a calm, zero-anxiety web interface that answers four simple questions:
1. *What happened while I was asleep?* (Two-line executive digest)
2. *Is anyone waiting on me?* (Action items explicitly directed at or concerning the user)
3. *What dates or deadlines were mentioned?* (Chronological commitments)
4. *How much noise did I safely ignore?* (Count of chatter messages bypassed, rewarding the user's laziness)

Zero data leaves the machine. No cloud subscriptions. No push notifications.

---

## 2. Proto-Personas (HCI Perception, Cognition & Motor Profiles)

To guide design choices and usability specifications, three proto-personas represent the core user spectrum.

### Persona 1: Maya Chen — The Overwhelmed CS Student
- **Role**: Second-year Computer Science student, team lead in a 48-hour hackathon, member of 14 active project and social groups.
- **Goals**: Stay on top of homework deadlines, project deliverables, and team questions without drowning in banter.
- **Frustrations**: Wakes up to 380 unread messages across 5 WhatsApp groups; fears someone asked for code review or API credentials while she slept.
- **HCI Profile**:
  - **Perception**: High visual scanning speed; prone to "banner blindness" when interfaces have redundant headers or colorful badge spam; irritated by low contrast or chaotic layouts.
  - **Cognition**: High working memory load; suffers from decision fatigue and context switching early in the morning; needs rapid answers with direct attribution (citations) to verify authenticity before acting.
  - **Motor**: Rapid keyboard navigator (uses `Tab`, `Enter`, vim-style shortcuts); operates laptop in dim light or one-handed on mobile while drinking coffee.

### Persona 2: Marcus O'Connor — The Multi-Group Class Representative
- **Role**: Academic representative for 180 engineering students; manages 6 course groups, faculty announcement channels, and student council discussions.
- **Goals**: Identify actionable requests ("Can we move Thursday's quiz?", "Where is the lab report template?"), collect student feedback, and track submission deadlines.
- **Frustrations**: Spends 1.5 hours daily manually scanning chat logs; frequently copies and pastes message snippets into spreadsheets to build action lists.
- **HCI Profile**:
  - **Perception**: Needs structured hierarchy, clear typography, and immediate visual categorization (dates vs. action items vs. chatter).
  - **Cognition**: High need for error prevention; cannot afford false positives or hallucinated deadlines; requires quick verification back to the original author and timestamp.
  - **Motor**: Primary desktop/laptop user with trackpad; relies on multi-tasking workflows, clipboard copy operations, and drag-and-drop file ingestion.

### Persona 3: Evelyn Davies — The Non-Technical Family Organizer
- **Role**: Retired teacher (age 68); coordinator of a 24-member extended family group, church volunteering committee, and neighborhood book club.
- **Goals**: Know when family members are visiting, track potluck deadlines, and see who needs a ride without reading 200 emoji reactions and arguments.
- **Frustrations**: Confused by technical jargon (API keys, localhost, command lines); overwhelmed by noisy notification dots; easily intimidated by multi-step configuration dialogs.
- **HCI Profile**:
  - **Perception**: Presbyopia (age-related visual accommodation decline); requires minimum 16px/18px body font, high contrast ratios (>= 4.5:1, preferably >= 7:1 for key headings), and generous spacing.
  - **Cognition**: Prefers recognition over recall; requires unambiguous plain-English copy (e.g., "Add Chat File" instead of "Ingest Payload"); gets anxious if a long process gives no feedback.
  - **Motor**: Mild hand tremor; requires minimum touch/click target sizes of 44×44px (WCAG 2.2 AAA Target Size preferred: 48×48px); prone to accidental double-clicks or missed dropdowns.

---

## 3. Scenarios & Task Analysis (with Optimal Click Counts)

### Scenario 1: The Zero-Touch Morning Glance (Watched Folder Mode)
- **User**: Maya Chen.
- **Context**: Maya set her WhatsApp desktop chat export to auto-save into `~/SlothWatched/` folder before sleeping. The nightly `sloth run` daemon processed it at 04:00 AM.
- **Task**: Check if anyone is waiting on her while brushing teeth.
- **Optimal Path**:
  1. Open browser bookmark / app page (`http://localhost:5173`). *(1 action)*
  2. The latest Morning Digest is immediately visible with the 2-line summary, 2 action items, and "342 messages safely ignored". *(0 clicks)*
- **Total Clicks**: **0 clicks** (Instant recognition).

### Scenario 2: Manual Drag-and-Drop Ingestion of an Exported Chat (.txt/.zip)
- **User**: Marcus O'Connor.
- **Context**: Just downloaded an exported WhatsApp chat `.txt` (or `.zip` with media ignored) from the Class Council group.
- **Task**: Ingest the chat and generate the morning digest.
- **Optimal Path**:
  1. Open Sloth Digest.
  2. Drag and drop `WhatsApp Chat - Class Council.txt` into the dropzone (or click "Browse File"). *(1 click / drag)*
  3. Click "Digest Chat". *(1 click)*
  4. Watch real-time streaming progress bar with honest ETA ("Processing chunk 2 of 4... ~15s left").
  5. Digest view renders automatically upon completion.
- **Total Clicks**: **2 clicks** (or 1 drag-and-drop).

### Scenario 3: Verifying an Action Item with Source Traceability (Hallucination Guard)
- **User**: Marcus O'Connor.
- **Context**: An action item says: *"Submit room reservation form to Dean's office by Friday 3 PM"*. Marcus wants to verify who said this and the exact context before emailing the Dean.
- **Task**: Inspect the raw source message for the action item.
- **Optimal Path**:
  1. Click "View Source" icon button on the action item card. *(1 click)*
  2. Source message drawer slides open, displaying original sender (`Prof. Henderson`), timestamp (`Yesterday 18:42`), and raw text with matching phrase highlighted.
  3. Click "Close Drawer" or press `Escape`. *(1 click or 1 keypress)*
- **Total Clicks**: **1 click** to verify.

### Scenario 4: Reviewing Dates and Deadlines Calendar View
- **User**: Evelyn Davies.
- **Context**: Evelyn wants to see all dates mentioned in the family chat for Thanksgiving coordination.
- **Task**: Check dates and copy them to her personal planner.
- **Optimal Path**:
  1. Click the "Dates & Deadlines" section tab/anchor. *(1 click)*
  2. Read chronological cards: each shows Date, Event ("Grandma arriving"), Sender ("David"), and a 1-click "Copy" button.
  3. Click "Copy to Clipboard". *(1 click)*
- **Total Clicks**: **2 clicks**.

### Scenario 5: First-Run Onboarding & Offline Model Verification
- **User**: Non-technical user or new developer setting up Sloth Digest.
- **Context**: Ollama is installed, but the user wants to ensure the model is loaded and the app is 100% offline.
- **Task**: Check system status chip and verify model readiness.
- **Optimal Path**:
  1. Open app. Status chip shows: `"Offline · nothing leaves this machine · qwen2.5:1.5b"`. *(0 clicks)*
  2. Click status chip to view the Health Modal with local host connectivity, model tag, VRAM usage estimate, and a "Run Diagnostic Test" button. *(1 click)*
- **Total Clicks**: **1 click**.

### Scenario 6: Inbox & File Tidier (Stretch Goal: Rewarding Laziness)
- **User**: Maya Chen.
- **Context**: Chat folder contains messy exports like `WhatsApp Chat - CS301 (1).txt`, `Chat_20261020.txt`, `archive.zip`.
- **Task**: Review tidy recommendations (standardized renaming, archiving old chats).
- **Optimal Path**:
  1. Click "Tidier" tab in header navigation. *(1 click)*
  2. Review list of 4 suggested clean-ups ("Rename to `CS301_Oct20.txt`", "Archive 3 files older than 30 days").
  3. Click "Apply All Suggestions (Lazy Mode)". *(1 click)*
- **Total Clicks**: **2 clicks**.

---

## 4. User Stories (MoSCoW Prioritization & Acceptance Criteria)

### Must Have (M)
- **US-M1 (Chat Ingestion & Parsing)**: As a user, I want to drop in a WhatsApp `.txt` or `.zip` export file, so that the system extracts messages without requiring manual cleanup.
  - *Acceptance Criteria*:
    - Supports iOS and Android WhatsApp date/time formats (e.g. `[DD/MM/YYYY, HH:MM:SS]`, `M/D/YY, H:MM AM/PM - Sender: Text`).
    - Strips non-text system messages (e.g., "Messages and calls are end-to-end encrypted").
    - Rejects invalid files with an informative, polite error message.
- **US-M2 (Local-First LLM Summarization)**: As a privacy-conscious user, I want summarization to run entirely on my local machine via Ollama, so that my personal conversations never touch the cloud.
  - *Acceptance Criteria*:
    - Calls `http://localhost:11434/api/generate` (or chat endpoint) with `qwen2.5:1.5b` (or configured tag).
    - Hard failure/test check if any socket connection attempts an outbound IP outside localhost.
- **US-M3 (Morning Digest View: 4 Core Pillars)**: As a lazy user, I want to open a morning dashboard that displays:
    1. A concise two-line summary.
    2. Action items ("Who is waiting on you").
    3. Dates and deadlines mentioned.
    4. A "Safe to ignore" message counter.
  - *Acceptance Criteria*:
    - Renders all 4 components above the fold or smoothly scrollable on mobile and desktop.
    - Safe-to-ignore count displays total messages processed minus action/date items.
- **US-M4 (Hallucination Guard / Source Attribution)**: As a user, I want every extracted action item and deadline to cite the original chat message, so that I can verify facts before taking action.
  - *Acceptance Criteria*:
    - Every action item card contains a clickable link or button to view the source message (`sender`, `timestamp`, `raw_text`).
    - Source drawer highlights the exact sentence/snippet.
- **US-M5 (Permanent Offline Status Chip)**: As a user, I want a permanent visual indicator that the app is offline and private, so that I have peace of mind.
  - *Acceptance Criteria*:
    - Fixed or header-anchored chip: `"Offline · nothing leaves this machine · <model-tag>"`.
    - WCAG AA contrast compliant.

### Should Have (S)
- **US-S1 (Nightly Job & Watched Folder CLI)**: As a busy user, I want a background runner (`sloth run`) that checks a folder for new chats overnight, so that the morning digest is ready before I wake up.
  - *Acceptance Criteria*:
    - `python -m sloth run` processes unread files in `watched/` and caches results into SQLite.
- **US-S2 (Progress & Honest Time Estimation)**: As a user processing a large chat (1,000–5,000 messages), I want to see streaming progress with honest chunk-based progress and estimated remaining time, so that I know the system hasn't frozen.
  - *Acceptance Criteria*:
    - Server-Sent Events (SSE) or streaming status endpoint (`/api/digest/progress/{task_id}`).
    - Reports: current chunk / total chunks, elapsed time, estimated time remaining based on moving average.
- **US-S3 (Model Not Installed / First-Run Helper)**: As a user without Ollama or the required model, I want a clear 3-step setup guide, so that I can get running in under 2 minutes.
  - *Acceptance Criteria*:
    - If Ollama unreachable or model missing, shows:
      1. Step 1: Install Ollama (`ollama.com`).
      2. Step 2: Run `ollama pull qwen2.5:1.5b`.
      3. Step 3: Refresh or click "Check Connection".

### Could Have (C)
- **US-C1 (Inbox/File Tidier Module)**: As a lazy user with messy chat archives, I want recommendations to rename, organize, and archive stale chat exports, so that my desktop stays clean.
  - *Acceptance Criteria*:
    - Scans directory, surfaces suggested cleanups, provides 1-click execution.
- **US-C2 (Export / Copy Digest)**: As a user, I want to copy the morning digest to markdown or clipboard in one click, so that I can paste it into my notes or todo list.

### Won't Have (W) (Deliberately Out of Scope)
- No user accounts, passwords, or cloud sync (anti-pattern for local-first privacy).
- No direct connection to WhatsApp web scraping / unofficial API bots (violates WhatsApp ToS and introduces fragile session hacks; relies strictly on standard user-initiated exports).
- No heavy models requiring > 8 GB RAM (e.g. 70B parameters).

---

## 5. Usability Specification (U1–U10)

These ten measurable usability criteria are established **prior to testing or evaluation**. Each specification includes a Worst-Acceptable Level, a Planned Target, and an Optimum Target.

| ID | Usability Attribute | Metric / Operation | Worst-Acceptable Level | Planned Target | Optimum Target |
|:---|:---|:---|:---|:---|:---|
| **U1** | **Learnability (First-Time Ingestion)** | Time taken for a novice user to upload a chat file and initiate summarization from cold start. | <= 45 seconds | <= 20 seconds | <= 10 seconds (drag & drop) |
| **U2** | **Cognitive Efficiency (Morning Scan)** | Time required to absorb the two-line digest and identify pending action items. | <= 20 seconds | <= 8 seconds | <= 5 seconds |
| **U3** | **Traceability / Verification Efficiency** | Clicks and time required to reveal and verify the raw source text for an action item. | <= 2 clicks, <= 5s | 1 click, <= 2s | 1 click, instantaneous popover (< 300ms) |
| **U4** | **Error Rate (Invalid File Input)** | Graceful recovery when dropping an unsupported or corrupted file (e.g., .pdf or empty text). | Clear error message within 2s; app remains usable without crash. | Clear error with suggested fix ("Please upload WhatsApp .txt or .zip"); zero console errors. | Automatic file type detection, polite feedback, and dropzone reset. |
| **U5** | **System Visibility & Status Clarity** | Feedback delay when inference starts; user awareness of background progress. | Status shown within 2s; chunk progress updated every 10s. | Status shown in < 200ms; progress bar with chunk count & ETA updated continuously. | Real-time streaming tokens or sub-second SSE updates with calm visual breathing pulse. |
| **U6** | **Accessibility (WCAG 2.2 AA Compliance)** | Automated axe-core violations + manual keyboard tab flow navigation. | 0 critical / serious violations; full keyboard reachability. | 0 violations across all severity levels; visible focus ring (`:focus-visible`); 44×44px touch targets. | Full WCAG 2.2 AAA on color contrast (>= 7:1) and touch targets (>= 48×48px). |
| **U7** | **Subjective Satisfaction (System Usability Scale - SUS)** | Post-test SUS score (10-item standardized questionnaire). | SUS >= 72 (Above average) | SUS >= 85 (Grade A / Excellent) | SUS >= 92 (Best-in-class) |
| **U8** | **First-Screen Performance Budget** | Time to First Contentful Paint (FCP) and Time to Interactive (TTI) on a standard mid-range laptop. | FCP <= 2.5s, TTI <= 3.5s | FCP <= 1.2s, TTI <= 1.8s | FCP < 800ms, TTI < 1.2s |
| **U9** | **Throughput / Unattended Inference** | Processing 5,000-message chat export on 8 GB RAM local machine without crashing or memory leak. | Successfully completes in <= 6 minutes without OOM. | Completes in <= 3 minutes with map-reduce chunking; memory delta <= 250 MB. | Completes in <= 90 seconds on GPU/Metal acceleration. |
| **U10** | **Motion & Cognitive Calmness** | Adherence to `prefers-reduced-motion` and absence of high-arousal urgency cues (red dots, notification bells). | Zero involuntary flashing/blinking; reduced-motion query honored. | All transitions <= 200ms ease-out; warm neutral palette; zero red badges. | Subtle micro-interactions only; celebratory calm feeling of safe noise avoided. |

---

## 6. Phase 1 Sign-Off

- **Artefacts Completed**: `docs/01_requirements.md` (Personas, 6 Scenarios, Task Analysis, MoSCoW User Stories, Usability Specifications U1–U10), `docs/DECISIONS.md` (DEC-001 through DEC-005).
- **Risks Identified**:
  1. WhatsApp export formats vary significantly across iOS (bracketed timestamps) and Android (hyphen-separated timestamps) and localized languages (AM/PM vs. 24h, DD/MM vs. MM/DD). Parser must have robust multi-pattern regex.
  2. Local LLM may generate inconsistent JSON if prompts are loose. Parser must enforce strict JSON schemas and fallback regex parsing.
- **Deliberately Left Out of Phase 1**:
  - Live socket scraping of WhatsApp Web (rejected due to instability, fragility, and ToS risks).
  - Cloud LLM fallback keys (rejected to uphold 100% offline privacy contract).
