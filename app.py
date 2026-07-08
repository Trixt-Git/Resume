import streamlit as st

from llm_client import get_reply_stream
from prompt_builder import build_system_prompt, load_facts

st.set_page_config(page_title="Ask Wil", page_icon="💬")

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Fraunces:opsz,wght@9..144,500&display=swap');

:root {
  --bg: #FAFBF9;
  --surface: #FFFFFF;
  --ink: #14251A;
  --muted: #55665C;
  --line: #E1E8E2;
  --accent: #3F7623;
  --refusal: #B4842A;
}

html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--bg);
  color: var(--ink);
  font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif;
}

.block-container {
  max-width: 720px;
  padding-top: 2rem;
}

h1 {
  font-family: 'Fraunces', Georgia, serif;
  font-weight: 500;
  color: var(--ink);
}

.askwil-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 2px;
}

.askwil-marker {
  font-size: 0.75rem;
  margin-top: 6px;
  padding-left: 10px;
  border-left: 3px solid var(--line);
}

.askwil-marker--source {
  border-left-color: var(--accent);
  color: var(--muted);
}

.askwil-marker--refusal {
  border-left-color: var(--refusal);
  color: var(--refusal);
  font-weight: 600;
}

.stButton button {
  border-radius: 10px !important;
  border: 1px solid var(--line) !important;
  min-height: 44px;
}

.stButton button:focus-visible,
textarea:focus-visible,
input:focus-visible {
  outline: 2px solid var(--accent) !important;
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
</style>
"""
st.markdown(STYLE, unsafe_allow_html=True)

st.title("Ask Wil")
st.caption(
    "An AI assistant answering from Wil's verified background — one of his "
    "projects. It will tell you when it doesn't know."
)

api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
if not api_key:
    st.error("API key not configured — see README.")
    st.stop()

if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = build_system_prompt(load_facts())
if "messages" not in st.session_state:
    st.session_state["messages"] = []

REFUSAL_MARKERS = [
    "haven't worked with", "haven't used", "don't claim",
    "won't claim", "can't claim", "haven't done",
    "can't do that", "verified background",
]


def is_refusal(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in REFUSAL_MARKERS)


def render_marker(text: str) -> None:
    if is_refusal(text):
        st.markdown(
            '<div class="askwil-marker askwil-marker--refusal">outside verified facts</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="askwil-marker askwil-marker--source">from verified facts</div>',
            unsafe_allow_html=True,
        )


for message in st.session_state["messages"]:
    if message["role"] == "assistant":
        with st.chat_message("assistant", avatar="💬"):
            st.markdown('<div class="askwil-label">Wil</div>', unsafe_allow_html=True)
            st.write(message["content"])
            render_marker(message["content"])
    else:
        with st.chat_message("user"):
            st.write(message["content"])

user_input = st.chat_input("Ask about Wil's background, skills, or projects")
if not st.session_state["messages"]:
    c1, c2, c3 = st.columns(3)
    if c1.button("What's FloorPlan?"):
        user_input = "What's FloorPlan?"
    if c2.button("Why Fidelity's LEAP Program?"):
        user_input = "Why Fidelity's LEAP Program?"
    if c3.button("Walk me through your Python experience."):
        user_input = "Walk me through your Python experience."

if user_input:
    if len(st.session_state["messages"]) >= 60:
        st.warning(
            "This session has hit its message limit — feel free to refresh "
            "to start a new one, or reach Wil directly via the links in his "
            "resume."
        )
    elif len(user_input) > 1000:
        st.warning("That message is too long for this bot — could you shorten it?")
    else:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        last_12_messages = st.session_state["messages"][-12:]
        if last_12_messages and last_12_messages[0]["role"] != "user":
            last_12_messages = last_12_messages[1:]

        with st.chat_message("assistant", avatar="💬"):
            st.markdown('<div class="askwil-label">Wil</div>', unsafe_allow_html=True)
            reply = st.write_stream(
                get_reply_stream(api_key, st.session_state["system_prompt"], last_12_messages)
            )
            render_marker(reply)
        st.session_state["messages"].append({"role": "assistant", "content": reply})
