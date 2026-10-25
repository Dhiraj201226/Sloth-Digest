# Sloth Digest — Phase 2: Design & Interaction Specification

**Project**: Sloth Digest  
**Theme**: Dev.to Hacktoberfest Open-Source AI Challenge — Week 3: "Slow and Steady" (Rewarding Laziness)  
**Role**: Senior Software Engineer & HCI Practitioner  
**Status**: Completed  
**Last Updated**: 2026-10-25  

---

## 1. Design Evolution: Iteration 1 vs. Iteration 2

To create an interface that truly rewards laziness and eliminates communication anxiety, the design underwent two full conceptual iterations.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ ITERATION 1: The "Notification Aggregator" (Rejected)                                 │
│ ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ 🔴 [5 Urgent Messages]  ⚠️ [3 Deadlines Approaching]  🔔 [Live Activity Feed]       │ │
│ │ ┌─────────────┐ ┌─────────────┐ ┌────────────────────────────────────────────────┐ │ │
│ │ │ Group A (12)│ │ Group B (4) │ │ Chat stream: real-time updates polling every 5s │ │ │
│ │ └─────────────┘ └─────────────┘ └────────────────────────────────────────────────┘ │ │
│ └────────────────────────────────────────────────────────────────────────────────────┘ │
│ Why Replaced: Reintroduced the exact same anxiety it sought to cure. Flashing badges, │
│ unread counts, and real-time feeds induced panic and FOMO rather than restful calm.   │
└────────────────────────────────────────────────────────────────────────────────────────┘

                                         ▼

┌────────────────────────────────────────────────────────────────────────────────────────┐
│ ITERATION 2: The "Calm Morning Hearth" (Adopted)                                       │
│ ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ 🦥 Sloth Digest   [Offline · nothing leaves this machine · qwen2.5:1.5b]           │ │
│ │ "Good morning. While you were resting, 384 messages were safely ignored."          │ │
│ │                                                                                    │ │
│ │ ┌────────────────────────────────────────────────────────────────────────────────┐ │ │
│ │ │ ☕ Morning Digest (2 lines)                                                     │ │ │
│ │ │ The CS301 project team agreed on PostgreSQL schema; family dinner confirmed... │ │ │
│ │ └────────────────────────────────────────────────────────────────────────────────┘ │ │
│ │ ┌───────────────────────────────┐ ┌───────────────────────────────┐                │ │
│ │ │ 🎯 Who is Waiting on You (2)  │ │ 📅 Dates & Deadlines (3)      │                │ │
│ │ │ • Prof. Henderson: Lab report │ │ • Oct 28: Quiz 2 in CS301     │                │ │
│ │ │   [View Source Message]       │ │ • Nov 02: Sarah's birthday    │                │ │
│ │ └───────────────────────────────┘ └───────────────────────────────┘                │ │
│ └────────────────────────────────────────────────────────────────────────────────────┘ │
│ Rationale: Celebrates inaction. Replaces red urgency cues with warm earth tones.       │
│ Single primary action per screen. Deep sleep and wake-up reassurance.                  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Rationale for Iteration 2 Replacement
1. **Psychological Framing**: Iteration 1 framed unread communication as an emergency (red warning icons, unread counts). Iteration 2 reframes unread chatter as an achievement of restful laziness ("384 messages safely ignored").
2. **Visual Clutter & Cognitive Load**: Iteration 1 divided attention across multiple group chat tabs. Iteration 2 synthesizes all input into one cohesive executive digest.
3. **No Urgency Cues**: Abolished red notification dots, pulsing alarms, and simulated push notifications.
4. **Attribution Trust**: Iteration 2 introduces the Hallucination Guard ("View Source Message") directly on action cards, allowing instant verification without mental friction.

---

## 2. "Slow and Steady" Visual Language & Design Tokens

The visual language communicates relaxation, grounded stability, and peaceful morning coffee.

### 2.1 Color Palette (Warm Neutral & Grounded Earth)
- **Canvas / Background**:
  - Light mode: `#FDFBF7` (Soft Linen / Warm Paper)
  - Dark mode: `#1A1918` (Warm Charcoal / Roasted Coffee)
- **Card Surfaces**:
  - Light mode: `#FFFFFF` with warm border `#EBE6DF`
  - Dark mode: `#242220` with subtle border `#383430`
- **Primary Accent (Calm Moss / Sage)**:
  - Base: `#4A6B53` (Sage Forest, 5.8:1 contrast on `#FDFBF7`)
  - Hover: `#3A5441`
  - Soft surface: `#EBF2ED`
- **Secondary Accent (Amber Honey / Clay)**:
  - Base: `#9C6528` (Warm Honey/Terracotta, 4.9:1 contrast)
  - Soft surface: `#F8F2EA`
- **Neutral Text Hierarchy**:
  - Heading 1 & Titles: `#1E1D1B` (14.2:1 contrast against `#FDFBF7`)
  - Body Text: `#383531` (9.5:1 contrast against `#FDFBF7`)
  - Subdued / Secondary: `#6B665F` (4.8:1 contrast against `#FDFBF7`)
- **Strict Prohibition**: No bright neon reds (`#FF0000`), no pulsing alert banners, no rapid flashy spinners.

### 2.2 Typography
- **Headings**: Modern geometric serif/sans blend with warm personality (`Outfit` / `Inter`, system fallback `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto`).
- **Body & Digest**: High-legibility sans-serif (`Inter`, font-size: 16px minimum on mobile, 17px on desktop; line-height: 1.6).
- **Code & Citations**: Monospace (`ui-monospace`, `JetBrains Mono`, `Consolas`, font-size: 13px) for timestamps, raw chat lines, and model hashes.

### 2.3 Motion & Transitions
- Respects `prefers-reduced-motion: reduce`: All animations gracefully collapse to immediate 0ms opacity steps.
- Default easing: `cubic-bezier(0.16, 1, 0.3, 1)` (gentle spring-out, max duration 240ms).
- Progress indicator: Calm "breathing" progress bar rather than an erratic spinning wheel.

---

## 3. Application of HCI Principles & Nielsen's 10 Heuristics

| Heuristic | Application in Sloth Digest |
|:---|:---|
| **1. Visibility of system status** | Permanent offline status chip with model name (`Offline · nothing leaves this machine · qwen2.5:1.5b`). During inference, honest streaming progress: `"Chunk 3/5 · ~18s remaining"`. |
| **2. Match between system and real world** | Terminology mirrors natural morning routines ("Morning Digest", "Who is waiting on you", "Safe to ignore") rather than technical parsing terms ("Tokens parsed", "DAG execution"). |
| **3. User control and freedom** | Users can cancel active inference at any time with one click. Clear "Re-run Digest" and "Delete Stored Chat" controls with confirmation. Source message drawer closes via `Escape` key, backdrop click, or close button. |
| **4. Consistency and standards** | Follows established web interaction conventions. File dropzone conforms to drag-and-drop standards. Buttons, cards, and modal dialogs use standard focus rings and ARIA patterns. |
| **5. Error prevention** | File upload inspects extension (`.txt`, `.zip`) and pre-validates file header before calling inference. If file is invalid or empty, prevents submission with actionable guidance. |
| **6. Recognition over recall** | Active model, processed chat metadata (name, date range, message count), and cited sources are immediately visible without memorization or multi-level navigation. |
| **7. Flexibility and efficiency of use** | Novices drag and drop chat exports via UI. Advanced users leverage the `sloth run` CLI or watched folder for fully automated zero-click morning reads. Full keyboard navigation (`Tab`, `Enter`, `Esc`). |
| **8. Aesthetic and minimalist design** | 12-column grid with generous whitespace (padding: 2rem+). Every screen has exactly **one** primary call to action. No extraneous advertising, social sharing, or unnecessary clutter. |
| **9. Help users recognize, diagnose, and recover from errors** | Plain-English error messages with direct recovery buttons. If Ollama is not running: `"Cannot connect to Ollama on localhost:11434. Please start the Ollama desktop app, or run 'ollama serve' in your terminal."` with a `Retry Connection` button. |
| **10. Help and documentation** | "How it works" 3-step offline guide embedded on the first-run screen. Dedicated model setup guide with copyable terminal commands. |

---

## 4. Layout, 12-Column Grid & Progressive Disclosure

### 4.1 12-Column Responsive Layout
- **Mobile (< 768px)**: 1-column stacked card flow.
- **Desktop (>= 1024px)**:
  - Columns 1–12 (Full Width): Global Header & Status Chip.
  - Columns 1–12 (Full Width): Welcome & Noise Avoided Banner (`"384 messages safely ignored"`).
  - Columns 1–12 (Full Width): 2-Line Morning Digest Card.
  - Columns 1–6 (Left Half): "Who is Waiting on You" (Action Items Card Stack).
  - Columns 7–12 (Right Half): "Dates & Deadlines Mentioned" (Timeline Card Stack).
  - Columns 1–12 (Full Width): Secondary Tools (File Dropzone / Watched Folder status / Tidier).

### 4.2 Progressive Disclosure Pattern
- **Level 1 (Morning Glance - 5s)**: 2-line summary + badge of safe noise.
- **Level 2 (Scannable Cards - 15s)**: Action items and dates with sender name and time.
- **Level 3 (Source Verification - On Demand)**: Clicking "View Source Message" slides open the full context drawer showing original chat lines with the exact matched passage highlighted.

---

## 5. Explicit State Architecture

The user interface explicitly designs and handles five fundamental states:

```
┌────────────────────────────────────────────────────────────────────────┐
│ State 1: First-Run / Model Not Found                                  │
│ • Clear 3-step guide: (1) Install Ollama, (2) Pull Model, (3) Verify  │
│ • Copyable code snippet: `ollama pull qwen2.5:1.5b`                   │
│ • Live "Test Ollama Connection" button with instant ping              │
├────────────────────────────────────────────────────────────────────────┤
│ State 2: Empty State (Ready for Ingestion)                             │
│ • Calm dropzone illustration with friendly sloth motif                │
│ • Prompt: "Drop your WhatsApp chat export (.txt or .zip) here"        │
│ • Quick test with pre-bundled synthetic sample chats (1 click)         │
├────────────────────────────────────────────────────────────────────────┤
│ State 3: Active Inference (Streaming / Honest Progress)               │
│ • Permanent status: "Offline · reading privately..."                   │
│ • Calm breathing progress bar (e.g. 60% complete)                     │
│ • Honest feedback: "Chunk 3 of 5 · ~18s remaining"                   │
│ • Safe "Cancel" button to stop processing without leaving zombies      │
├────────────────────────────────────────────────────────────────────────┤
│ State 4: Morning Digest (Success / Completed State)                    │
│ • "384 messages safely ignored" celebration badge                      │
│ • 2-line executive digest                                              │
│ • Action items with 1-click "View Source" hallucination guard         │
│ • Dates & Deadlines chronological listing                             │
│ • Actionable controls: "Copy Digest", "Digest New Chat", "Tidier"      │
├────────────────────────────────────────────────────────────────────────┤
│ State 5: Error / Recovery State                                        │
│ • Non-blaming, plain language explanation                              │
│ • Diagnostic details collapsed behind "Technical Details" accordion   │
│ • Clear recovery options: "Retry Inference", "Choose Another File"     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Accessibility & Inclusivity Specification (WCAG 2.2 AA)

1. **Color Contrast**:
   - All normal body text has >= 4.8:1 contrast (exceeds WCAG AA 4.5:1).
   - Headings have >= 12:1 contrast.
   - Focus rings have >= 3:1 contrast against adjacent backgrounds.
2. **Touch & Click Targets**:
   - Every interactive element (buttons, upload zone, drawer triggers) has a minimum touch target bounding box of 44×44px.
3. **Full Keyboard Operability**:
   - Tab sequence is logical and sequential (Skip to content -> Header -> Digest -> Action items -> Upload).
   - Visible `:focus-visible` styling using a double ring (`ring-2 ring-emerald-700 ring-offset-2`).
   - Drawers and modals trap focus and support `Escape` dismissal.
4. **Semantic HTML & Screen Reader Labels**:
   - Semantic landmarks: `<header>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`.
   - Action item cards use `<article aria-labelledby="action-title-1">`.
   - All icon-only buttons include descriptive `aria-label` (e.g., `aria-label="View source message from David at 14:22"`).
5. **No Urgency-Induced Anxiety**:
   - Zero blinking text, zero red notification count badges, zero auto-dismissing toast notifications that expire before users can read them.

---

## 7. Phase 2 Sign-Off

- **Artefacts Completed**: `docs/02_design.md` (Design evolution, color tokens, Nielsen heuristics, 12-column grid, progressive disclosure, 5 explicit states, WCAG 2.2 AA specification).
- **Risks Identified**:
  - Long inference on slower CPUs without discrete GPU could take 30–60 seconds for large chats. Mitigation: Real-time chunk progress with reassuring calm copy and honest ETA prevents user frustration.
- **Deliberately Left Out of Phase 2**:
  - Dark/light mode theme toggling flash (enforce pure CSS media query `@media (prefers-color-scheme: dark)` or calm persistent theme class without layout thrashing).
  - Gamification badges or streak counters (anti-pattern: creates addictive pressure instead of peaceful laziness).
