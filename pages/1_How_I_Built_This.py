import streamlit as st

from style import STYLE

st.set_page_config(page_title="How I Built This — Ask Wil", page_icon="💬")
st.markdown(STYLE, unsafe_allow_html=True)

st.title("How I Built This")
st.markdown(
    "A systems-analysis case study of Ask Wil's architecture, spec discipline, "
    "and validation — written for a technical, analyst-minded reader rather "
    "than as a dev-showcase."
)

st.header("Responsible AI by design")
st.markdown(
    """
The core requirement for this project was never "sound impressive" — it was
**refuse over speculate**. A chatbot that answers on someone's behalf and
gets it wrong is worse than one that says nothing, because a bad guess reads
as a lie about a real person's background.

The architecture follows from that constraint. Instead of retrieval
(RAG, a vector database, embeddings), the entire verified-facts file is
compiled into the system prompt once, at startup. The reasoning: the corpus
is one person's background at roughly 2–4k tokens, comfortably inside the
model's context window, so retrieval would add failure modes (missed
chunks, irrelevant matches) for zero accuracy benefit at this scale. The
model always sees the complete record, not a retrieved subset of it.

Refusal is enforced through a small set of absolute rules in the system
prompt, each anchored to an exact sentence rather than an open-ended
instruction:

- Unknown-topic questions get a fixed fallback sentence, never an
  improvised one.
- Skills outside a whitelist get denied plainly, using another fixed
  sentence.
- Attempts to override the persona, leak the prompt, or answer outside the
  verified record get a fixed refusal sentence, then a redirect back to the
  real background.
- Questions built on a false premise ("It says here you led a team...")
  get corrected against a fixed sentence, then redirected to the closest
  true fact.

That last point — locking refusals to *exact sentences* instead of letting
the model phrase them freely — turned out to matter more than it sounds
like it should. That story is in Testing & Validation below.
"""
)

st.header("Requirements & specification")
st.markdown(
    """
The build followed a locked specification document — a build map — written
before any code existed, with every architectural decision made once and
justified, rather than re-litigated phase by phase. Each phase had its own
task description, exact file list, and a **Definition of Done** the phase
had to satisfy before the next one could start.

Locked decisions were things like: which model to call, how conversation
state is held, what the session and input caps are, and where the one
seam importing the model provider's SDK lives. None of those were open
questions during execution — the spec existed precisely so they wouldn't
need to be re-decided under time pressure.

Specs are still written by people (or models), and this one had a real
discrepancy worth naming rather than glossing over: one phase's task
description said the facts schema has "seven top-level keys," while the
schema definition elsewhere in the same document actually lists eight
top-level keys. Rather than picking one number and hoping, the schema test
was written against the **actual schema's real keys**, and the mismatch was
reported back instead of silently resolved either way. That's the general
pattern for handling spec ambiguity here: when prose and structure
disagree, structure wins, and the disagreement gets flagged, not buried.

The specification itself also evolved — every amendment to a locked rule
is recorded in a running changelog at the top of the document, each entry
naming what broke, why, and what changed. Nothing is silently edited.
"""
)

st.header("Testing & validation")
st.markdown(
    """
Two independent layers of testing exist, deliberately separated because
they check different things.

**pytest** (fast, free, run constantly) checks structure: that the facts
file parses and has the right shape, and that the system prompt actually
contains the exact anchor sentences it's supposed to — so a mis-copied
prompt fails a free unit test before it ever costs an API call.

**The adversarial honesty eval** (`eval_honesty.py`, run manually — it
costs real API calls) checks behavior against the live model: 20 fixed
prompts designed to bait overclaiming (unearned AWS/React/Java/Kubernetes/
FastAPI experience, a fake certification, a fabricated internship),
attempt prompt injection or a persona override, assert a false premise
about the candidate's history, or ask a plain factual question that should
be answered confidently. Each case passes only if the reply contains an
expected phrase, doesn't contain a forbidden one, and doesn't contain any
hedging language from a global forbid list — all checked as case-insensitive
substring matches. The bar is strict: every one of the 20 cases has to
pass, every time, or the eval fails outright.

That strictness is what surfaced real defects instead of hiding them.
Two examples, both fixed at the source rather than by loosening the test:

- An early open-ended rule ("decline in one sentence") let the model phrase
  a genuine refusal in ways the eval didn't recognize as a refusal — the
  behavior was correct, the wording just wasn't anchored. The fix was to
  give that rule an exact required sentence, the same treatment the other
  absolute rules already had.
- A forbidden phrase used to catch overclaiming turned out to be
  **negation-blind**: a correct denial ("I haven't led a team of
  engineers") contains the same substring as a false claim would
  ("I led a team of engineers"), so the check occasionally flagged an
  honest answer as a failure. An audit found three more forbidden phrases
  with the same defect; all four were removed rather than patched
  one at a time.

Both fixes made the eval **stricter**, not looser — narrowing what counts
as compliant behavior instead of widening what counts as a pass.
"""
)

st.header("System data flow")
st.markdown("How one message moves through the system, start to finish:")
st.markdown(
    """
<div class="askwil-flow">
  <div class="askwil-flow-step">User submits a message (typed, or a starter prompt)</div>
  <div class="askwil-flow-arrow">↓</div>
  <div class="askwil-flow-step">Guardrail check — session cap (30 exchanges) and 1,000-character input cap, before any API call</div>
  <div class="askwil-flow-arrow">↓</div>
  <div class="askwil-flow-step">Facts grounding — the full verified-facts file was already compiled into the system prompt at startup; nothing is retrieved per-message</div>
  <div class="askwil-flow-arrow">↓</div>
  <div class="askwil-flow-step">Model call — system prompt (marked cacheable) + last 12 messages sent to the model, streamed back token by token</div>
  <div class="askwil-flow-arrow">↓</div>
  <div class="askwil-flow-step">Citation parse — a trailing machine-readable source tag is stripped from the reply before display; a failed or missing tag just means no citation line, never an error</div>
  <div class="askwil-flow-arrow">↓</div>
  <div class="askwil-flow-step">Rendered response — sourced answers and refusals are visually distinguishable at a glance</div>
</div>
""",
    unsafe_allow_html=True,
)

st.header("Cost & trade-off analysis")
st.markdown(
    """
The system prompt is sent as a cacheable content block, with the intent
that a 5-minute cache lets repeat calls in the same session read the
(unchanging) system prompt at a steep discount instead of paying full
price every turn. The documented estimate — corrected once already after
an earlier ~10x-too-low guess was checked against real pricing — is
roughly $0.03–$0.05 for a typical short conversation, and about $0.06 for
a fully maxed 30-question session.

**An update, found while extending this build, not before:** a live check
of the model's own usage statistics during this round of changes showed
the cache reporting zero cached tokens on back-to-back calls with an
unchanged system prompt — meaning caching does not appear to be engaging
at the system prompt's current size. The documented cost estimate above
reflects the *designed* behavior; it hasn't yet been reconciled with that
finding. Surfacing that gap here is more useful than quietly deleting the
claim, since catching a validated assumption that turned out to be wrong
is the same discipline the eval failures above were handled with.

On model tiering: this specification was written once, up front, with
every architectural decision already made and justified, by a
higher-capability model — then each phase was executed mechanically
against that locked spec by a lower-cost model, without re-opening design
decisions. The idea is that judgment is the expensive part and execution
is the cheap part, and a spec precise enough to hand off safely is itself
evidence the design was sound. Separately, the *deployed app* runs on a
small, fast model rather than a large one, because refusing to overclaim
is fundamentally an instruction-following problem, not a raw-capability
one — a cheap model that reliably follows a strict rule beats an expensive
one that occasionally improvises around it.
"""
)
