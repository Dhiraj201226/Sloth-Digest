# Contributing to Sloth Digest 🦥

Thank you for considering contributing to Sloth Digest! We are participating in **Hacktoberfest 2026** and welcome community contributions that respect our core design philosophy: **calm, offline, accessible, and lazy-first**.

---

## Code of Conduct

All contributors are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Core Guidelines & Invariants

1. **Strict Offline Privacy**: Sloth Digest must never send user chat logs or metadata over the internet. Zero external cloud APIs. Every PR must pass `tests/test_network_airgap.py`.
2. **"Slow & Steady" Visual Language**:
   - No high-arousal notification badges (no red alert dots, no urgent banners).
   - Generous spacing and warm earth/linen palette (`#FDFBF7`, `#4A6B53`).
   - Adherence to `prefers-reduced-motion`.
3. **Accessibility (WCAG 2.2 AA)**:
   - Minimum 4.5:1 text contrast.
   - Minimum 44×44px interactive touch targets.
   - Visible keyboard focus rings (`:focus-visible`).
4. **Hallucination Guard**:
   - Any new feature that extracts data from chats must link back to source message line numbers and citations.

---

## Development Workflow

### 1. Fork & Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Run Tests Before Submitting
```bash
# Backend pytest suite (must include airgap isolation)
python -m pytest -v tests/

# Frontend component tests
cd frontend && npm test && npm run build && cd ..
```

### 3. Submitting a Pull Request
- Reference any open issue in the PR description.
- Fill out the PR template completely.

---

## Good First Issues

Looking for somewhere to start? Check our curated list of 8 starter tasks in [`docs/GOOD_FIRST_ISSUES.md`](docs/GOOD_FIRST_ISSUES.md).
