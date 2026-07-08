# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"Ask Wil" — a Streamlit chat app that answers questions about Wil's professional background in first person, using only a verified `facts.json` file, and refuses anything outside it. The full build specification (locked architecture decisions, phase-by-phase build plan, and an amendment log of every change made and why) lives in `SPEC.md` — read it before making non-trivial changes. `README.md` documents the shipped product for an external reader.

## Commands

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

streamlit run app.py                 # run the app locally
pytest                                # fast, free unit tests
pytest tests/test_citations.py -v    # single test file
python eval_honesty.py               # adversarial honesty eval — costs real API calls, run manually only
```

`ANTHROPIC_API_KEY` resolves from `.streamlit/secrets.toml` (gitignored, never commit it) for `app.py`, or from the env var first / that same file second for `eval_honesty.py`.

## Architecture

**No RAG, no vector DB.** The entire contents of `facts.json` are compiled into the system prompt once at startup (`prompt_builder.py`), not retrieved per-message. The corpus is one person's background (~2-4k tokens) — small enough that full injection is simpler and more reliable than retrieval.

**Single LLM seam.** `llm_client.py` is the *only* file that imports `anthropic`. Everything else — `app.py`, `eval_honesty.py` — calls `get_reply()` or `get_reply_stream()`. Model is `claude-haiku-4-5-20251001` at `temperature=0.2, max_tokens=400`.

**System prompt structure** (`prompt_builder.py`): a fixed template with 8 numbered "ABSOLUTE RULES", a VOICE section (tone/style, explicitly subordinate to the rules), and a CITATION FORMAT section instructing the model to append `[[SOURCES: key1, key2]]` after every reply. The template is built with `.replace("{NAME}", ...)` / `.replace("{FACTS_JSON}", ...)` — **never** f-strings or `.format()`, since the JSON content contains literal `{`/`}` that would collapse them.

Several rules are anchored to an exact, locked sentence (not open-ended phrasing) specifically because early testing showed the adversarial eval could miss a *behaviorally correct* refusal that was worded differently than expected. Rule 1 (unknown topic), rule 3 (unclaimed skill), rule 5 (persona/injection defense), and rule 8 (false-premise correction) each have one fixed required sentence. Don't loosen these back to open-ended instructions.

**Citations** (`citations.py`): `parse_citation()` strips the trailing `[[SOURCES: ...]]` tag and returns the visible text plus a list of facts.json top-level keys (or `None` on any malformed/missing tag — never raises). `CitationStreamFilter` wraps the live token stream so the raw tag is never displayed even mid-stream — it withholds a trailing `"[["` until the stream ends before deciding whether it was a real tag.

**Guardrails** (`app.py`): 60-message / 30-exchange session cap, 1,000-character input cap, both checked before any API call. Conversation history is `st.session_state["messages"]`; only the last 12 messages (trimmed to start on a user turn) are sent per call.

**Testing is split deliberately**: `pytest` (`tests/`) checks structure — facts schema shape, and that the system prompt actually contains the locked anchor sentences — so a mis-copied prompt fails a free test before costing an API call. `eval_honesty.py` is a standalone script (not pytest) that sends 20 fixed adversarial prompts through the real API and asserts against a locked case table (`expect_any`/`forbid` substring matches, case-insensitive). It must hit 20/20 before any deploy; the case table itself is treated as locked — a failure means the facts, the prompt, or the model is wrong, not the test.

## Known gotchas

- `pages/1_How_I_Built_This.py` and `app.py` share CSS from `style.py` — don't import from `app.py` directly in another page module, since that would re-execute its top-level Streamlit calls.
- Deployed instance mirrors this repo into `trixt-git/resume-app`, which needs a `streamlit_app.py` shim (`exec(open("app.py").read())`) because Streamlit Community Cloud's main-file setting for that app is fixed and not editable — the shim is deploy-platform plumbing, not part of the actual app logic.
- Prompt caching (`cache_control: {"type": "ephemeral"}` on the system block) is wired up but was empirically found to not be engaging at the current system prompt's token count — verify with `client.messages.count_tokens(...)` and check `usage.cache_read_input_tokens` on a real call before trusting the cost estimates in `README.md`.
