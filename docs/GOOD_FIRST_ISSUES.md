# Sloth Digest — 8 Curated "Good First Issue" Tickets (Hacktoberfest 2026)

These issues are designed for new contributors, with clear scopes, reproduction steps, acceptance criteria, and relevant file pointers.

---

### Issue 1: [Parser] Add Telegram Desktop Export JSON (`result.json`) Parser
- **Difficulty**: Good First Issue (Beginner / Intermediate)
- **Labels**: `hacktoberfest`, `good-first-issue`, `parser`
- **Context**: While WhatsApp `.txt` is our primary format, Telegram Desktop exports conversations as a structured `result.json` file.
- **Task**: Implement `parse_telegram_json(raw_json: str) -> List[ParsedMessage]` in `backend/parser.py`.
- **Files to Modify**: `backend/parser.py`, `tests/test_parser.py`.
- **Acceptance Criteria**:
  - Successfully parses Telegram message JSON arrays (`date`, `from`, `text`).
  - Passes all existing pytest suites.
  - Zero cloud dependencies.

---

### Issue 2: [Parser] Support European WhatsApp Date Formats with Slash vs. Dot (`DD.MM.YY`)
- **Difficulty**: Good First Issue (Beginner)
- **Labels**: `hacktoberfest`, `good-first-issue`, `regex`
- **Context**: German and Austrian WhatsApp exports frequently format timestamps with periods: `[24.10.26, 14:02:10]`.
- **Task**: Extend regex in `backend/parser.py` to match dot-separated date delimiters seamlessly.
- **Files to Modify**: `backend/parser.py`, `tests/test_parser.py`.
- **Acceptance Criteria**:
  - `[24.10.2026, 14:00:00]` parses cleanly without dropping lines.
  - Unit test added in `tests/test_parser.py`.

---

### Issue 3: [Frontend] Add Keyboard Shortcut (`/` or `Cmd/Ctrl + K`) to Focus Search & Triage
- **Difficulty**: Good First Issue (Beginner)
- **Labels**: `hacktoberfest`, `good-first-issue`, `a11y`, `frontend`
- **Context**: Power users navigating their morning digest prefer keyboard-first workflows.
- **Task**: Add a global hotkey listener in `App.tsx` where pressing `Cmd+K` or `Ctrl+K` focuses the file upload or opens the Tidier modal.
- **Files to Modify**: `frontend/src/App.tsx`.
- **Acceptance Criteria**:
  - Follows standard accessible keyboard focus conventions.
  - Ignored when typing inside an input field.

---

### Issue 4: [Feature] 1-Click "Export to .ics Calendar" for Extracted Deadlines
- **Difficulty**: Good First Issue (Intermediate)
- **Labels**: `hacktoberfest`, `good-first-issue`, `feature`
- **Context**: Users want to drop deadlines directly into Google Calendar, Apple Calendar, or Outlook.
- **Task**: Add an "Add to Calendar (.ics)" button on the `DatesTimeline` component that generates a standard local `.ics` iCalendar file blob.
- **Files to Modify**: `frontend/src/components/DatesTimeline.tsx`.
- **Acceptance Criteria**:
  - Generates valid `.ics` format in pure client-side TypeScript.
  - Zero external network requests.

---

### Issue 5: [Frontend] Add UI Settings Modal for Swapping Ollama Model Tag
- **Difficulty**: Good First Issue (Intermediate)
- **Labels**: `hacktoberfest`, `good-first-issue`, `ui`
- **Context**: Users with 16 GB+ RAM may want to switch from `qwen2.5:1.5b` to `llama3.2:3b` or `gemma4:12b` without editing `.env`.
- **Task**: In `StatusChip.tsx` or Header, add a dropdown selector populated with `health.available_models` to select the active model for subsequent digests.
- **Files to Modify**: `frontend/src/components/StatusChip.tsx`, `backend/main.py`.
- **Acceptance Criteria**:
  - Saves chosen model to localStorage.
  - Passes selected model in the upload payload.

---

### Issue 6: [Tidier] Add "Delete Chat After Ingestion" Checkbox Option
- **Difficulty**: Good First Issue (Beginner)
- **Labels**: `hacktoberfest`, `good-first-issue`, `backend`
- **Context**: Privacy-conscious users may want the temporary export file deleted immediately once processed into SQLite.
- **Task**: Add an optional boolean `delete_source_after_digest` to `sloth run` and UI upload form.
- **Files to Modify**: `backend/sloth.py`, `backend/main.py`.
- **Acceptance Criteria**:
  - Defaults to `False` (safe default).
  - When `True`, securely removes the file once `save_digest` completes.

---

### Issue 7: [A11y] Add Skip to Content Link and Visible ARIA Announcement on Digest Ready
- **Difficulty**: Good First Issue (Beginner)
- **Labels**: `hacktoberfest`, `good-first-issue`, `a11y`
- **Context**: Screen reader users need an assertive announcement when long background inference finishes.
- **Task**: Add `<div aria-live="assertive" className="sr-only">` announcing *"Morning digest ready: X messages safely bypassed."* upon completion.
- **Files to Modify**: `frontend/src/App.tsx`.
- **Acceptance Criteria**:
  - Announces status to assistive tech without visual interruption.
  - Axe-core audit remains 0 violations.

---

### Issue 8: [CLI] Add `--json` Output Flag to `sloth run` CLI
- **Difficulty**: Good First Issue (Beginner)
- **Labels**: `hacktoberfest`, `good-first-issue`, `cli`
- **Context**: Unix users want to pipe `sloth run --json` into `jq` or notification daemons.
- **Task**: Add `--json` argument to `backend/sloth.py` that emits clean JSON on stdout instead of human terminal text.
- **Files to Modify**: `backend/sloth.py`.
- **Acceptance Criteria**:
  - Emits valid JSON payload when flag is present.
  - Preserves standard error stream for warnings.
