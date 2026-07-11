# Build Log

A chronological record of what was actually built and changed, with commit
hashes for traceability. This complements `BUILD_MAP.md` — that document is the
plan (the locked, up-front specification); this one is the history of execution
against it, plus the refinement work that came after the initial build.

Design decisions and their rationale live in the code and in each commit
message; this log is the map from "what changed" to "which commit." For the
locked spec and its own amendment log (v1.1–v1.9, covering the honesty-rule
evolution), see `BUILD_MAP.md`.

---

## Initial build — 2026-07-08

The app was built phase-by-phase against `BUILD_MAP.md`, starting from the
Streamlit template scaffold.

| Commit | Change |
|--------|--------|
| `a77e643` | Initial commit (scaffold) |
| `ad334da` | Replace Streamlit template scaffolding with the Ask Wil app |
| `2b4a218` | Add `streamlit_app.py` shim for Streamlit Cloud's fixed entry point |
| `8dc2859` | Add distilled voice guide as a VOICE section in the system prompt |
| `3ea5ada` | Style pass: Fidelity-green theme, refusal marker, streaming |
| `f8b570b` | Add 4 additive UX features: starters, opening message, fact citations, case-study page |
| `9bad56e` | Reorder starters: lead with strengths, rehire question last |
| `a60a53b` | Update question for Fidelity's LEAP role |
| `9f7c8d7`, `9bec5ee`, `3ab64ca` | Copy/label fixes on the starter buttons |
| `1e5fe94` | Refactor CSS styles and update color palette |
| `b3f69ac` | Rebrand to WilOS, category-based conversation starters |
| `2038873` | Merge refined WilOS style as canonical `style.py` |
| `6cbe9c3` | Change landing tagline to "Ready when you are." |
| `6c744c7` | Center landing page like a ChatGPT/Claude homepage |

## Refinement work — 2026-07-08 → 2026-07-09

Post-build iteration on facts accuracy, conversation UX, honesty behavior, and
visual design.

### Content

| Commit | Change |
|--------|--------|
| `9bd9b41` | Update FloorPlan facts to reflect the project's actual scope (decision-support app, OEE analysis, plant-leadership adoption) rather than a press-floor scheduler |

### Conversation UX & layout

| Commit | Change |
|--------|--------|
| `7aa4a6a` | Tighten hero layout: smaller title, shorter hero, narrower container |
| `bebdc5f` | Move chat input inline into the hero (ChatGPT-style), not pinned to the page bottom |
| `b9378cc` | Rerun after the first exchange to drop the hero immediately |
| `4c2c817` | Keep quick-action buttons in a persistent bottom bar; stop forcing a rerun |
| `a07582b` | Switch to chat mode immediately on submit, before the reply streams in (pending-input pattern) |
| `a45a0ef` | Refactor layout for a focused recruiter tool: minimal toolbar, styled sidebar nav, bordered chat panel |
| `3abf9d4` | Fix: render the bottom bar before the chat panel so the input appears during streaming, not after |

### Honesty behavior

| Commit | Change |
|--------|--------|
| `3944284` | Split casual off-topic small talk from unsupported-claim refusals — added rule 9 (cheeky redirect) while keeping the strict professional-claim refusals; eval grew from 20 → 24 cases (`BUILD_MAP.md` amendment v1.8) |
| `c96c213` | Vary rule 9's redirect across six approved styles (amendment v1.9) |

> **Deploy gate note:** the published eval-results block in `README.md`
> pre-dates rule 9 and reflects a 20-case run. `eval_honesty.py` is now a
> 24-case suite and must be run for real (it costs live API calls, run
> manually) to confirm 24/24 before go-live. The rule-9 additions are
> structurally verified (anchors present in the built prompt, unit tests pass)
> but not yet confirmed against the live model.

### Visual design / palette

| Commit | Change |
|--------|--------|
| `94c71a6` | Restore the original Fidelity green (`#3F7623`) after a prior refactor had drifted it to a generic Material green |
| `0ee15cd` | Swap the dark-olive green for a more vivid, higher-contrast green |
| `7171ae4` | Replace the green-heavy palette with a warm graphite / slate-blue / brass system |
| `5c25156` | Restyle to the Starbucks-inspired warm café design system: cream canvas, four-tier green, gold ceremony accent, full-pill buttons, whisper-soft card lift, tight tracking |
| `293523f` | Wrap "OS" in the wordmark span so the gold accent renders |

---

*This log is maintained alongside the code. New entries are appended in
chronological order; nothing is rewritten after the fact.*
