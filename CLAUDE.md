# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"WilOS" (formerly "Ask Wil") — a Streamlit chat app that answers questions about Wil's professional background in first person, using only a verified `facts.json` file, and refuses anything outside it. The full build specification (locked architecture decisions, phase-by-phase build plan, and an amendment log of every change made and why) lives in `BUILD_MAP.md` — read it before making non-trivial changes. `BUILD_LOG.md` is the companion execution history (what actually got built, mapped to commits). `README.md` documents the shipped product for an external reader.

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

**System prompt structure** (`prompt_builder.py`): a fixed template with 9 numbered "ABSOLUTE RULES", a VOICE section (tone/style, explicitly subordinate to the rules), and a CITATION FORMAT section instructing the model to append `[[SOURCES: key1, key2]]` after every reply. The template is built with `.replace("{NAME}", ...)` / `.replace("{FACTS_JSON}", ...)` — **never** f-strings or `.format()`, since the JSON content contains literal `{`/`}` that would collapse them.

Several rules are anchored to an exact, locked sentence (not open-ended phrasing) specifically because testing showed the adversarial eval could miss a *behaviorally correct* refusal that was worded differently than expected. Rule 1 (unknown topic), rule 3 (unclaimed skill), rule 5 (persona/injection defense), and rule 8 (false-premise correction) each have one fixed required sentence. Rule 9 (casual off-topic small talk, added so "What's for dinner?" gets a light redirect instead of the stiff unsupported-claim refusal) offers six approved redirect variants instead of one fixed sentence — the model is meant to vary which it picks, but each of the six is itself locked verbatim apart from filling in a bracketed slot. Don't loosen any of these back to fully open-ended instructions, and don't introduce a redirect variant containing a word from `eval_honesty.py`'s `GLOBAL_FORBID` list (a past redirect line containing "probably" collided with that list and failed the eval deterministically, every time the model picked it — fixed by rewording, not by editing the forbid list).

**Citations** (`citations.py`): `parse_citation()` strips the trailing `[[SOURCES: ...]]` tag and returns the visible text plus a list of facts.json top-level keys (or `None` on any malformed/missing tag — never raises). `CitationStreamFilter` wraps the live token stream so the raw tag is never displayed even mid-stream — it withholds a trailing `"[["` until the stream ends before deciding whether it was a real tag.

**Guardrails** (`app.py`): 60-message / 30-exchange session cap, 1,000-character input cap, both checked before any API call. Conversation history is `st.session_state["messages"]`; only the last 12 messages (trimmed to start on a user turn) are sent per call.

**Testing is split deliberately**: `pytest` (`tests/`) checks structure — facts schema shape, and that the system prompt actually contains the locked anchor sentences — so a mis-copied prompt fails a free test before costing an API call. `eval_honesty.py` is a standalone script (not pytest) that sends 24 fixed adversarial prompts through the real API and asserts against a locked case table (`expect_any`/`forbid` substring matches, case-insensitive). It must hit 24/24 before any deploy; the case table itself is treated as locked — a failure means the facts, the prompt, or the model is wrong, not the test. Only re-run this eval when a change touches `prompt_builder.py`, `facts.json`, `llm_client.py`, or `citations.py` — it costs real money, so don't run it for pure UI/style changes.

A forbid string is only valid in the case table if it cannot plausibly appear inside a *correct* denial (substring matching can't tell "I led a team" from "I haven't led a team" apart) — several forbid strings have been removed after tripping on exactly that, most recently `skills_pos`'s react/fastapi/java/aws list, which a correct answer can honestly name in the same breath as what it doesn't claim.

## Known gotchas

- `pages/1_How_I_Built_This.py` and `app.py` share CSS from `style.py` — don't import from `app.py` directly in another page module, since that would re-execute its top-level Streamlit calls.
- Deployed instance mirrors this repo into `trixt-git/resume-app`, which needs a `streamlit_app.py` shim (`exec(open("app.py").read())`) because Streamlit Community Cloud's main-file setting for that app is fixed and not editable — the shim is deploy-platform plumbing, not part of the actual app logic.
- Prompt caching (`cache_control: {"type": "ephemeral"}` on the system block) needs the system prompt above roughly 4,096–4,600 tokens to actually engage for this model — verify with `client.messages.count_tokens(...)` and check `usage.cache_read_input_tokens` on a real call rather than assume the cost estimates in `README.md` are current; the threshold was crossed once already by `facts.json` growing with real content, not by design.
- This repo and the deploy mirror (`trixt-git/resume-app`) have both had direct edits happen independently more than once — before assuming either repo is behind, `git fetch` and diff both, not just the one you're sitting in.
