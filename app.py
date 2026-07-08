import streamlit as st

from citations import CitationStreamFilter
from llm_client import get_reply_stream
from prompt_builder import build_system_prompt, load_facts
from style import STYLE

st.set_page_config(page_title="WilOS", page_icon="💬")
st.markdown(STYLE, unsafe_allow_html=True)

st.title("WilOS")
st.markdown("Ready when you are.")

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


def render_marker(text: str, keys) -> None:
    if is_refusal(text):
        st.markdown(
            '<div class="askwil-marker askwil-marker--refusal">outside verified facts</div>',
            unsafe_allow_html=True,
        )
    elif keys:
        label = "Source: " + ", ".join(k.replace("_", " ") for k in keys)
        st.markdown(
            f'<div class="askwil-marker askwil-marker--source">{label}</div>',
            unsafe_allow_html=True,
        )
    elif keys == []:
        st.markdown(
            '<div class="askwil-marker askwil-marker--source">from verified facts</div>',
            unsafe_allow_html=True,
        )
    # keys is None (citation parsing failed): no citation line, per spec —
    # the answer still displays normally, it just has no source caption.


for message in st.session_state["messages"]:
    if message["role"] == "assistant":
        with st.chat_message("assistant", avatar="💬"):
            st.markdown('<div class="askwil-label">Wil</div>', unsafe_allow_html=True)
            st.write(message["content"])
            render_marker(message["content"], message.get("sources"))
    else:
        with st.chat_message("user"):
            st.write(message["content"])

user_input = st.chat_input("Ask about Wil's background, skills, or projects")
if not st.session_state["messages"]:
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("Experience"):
        user_input = "Walk me through your work experience."
    if c2.button("Projects"):
        user_input = "Tell me about your projects."
    if c3.button("Systems"):
        user_input = "How do you approach building systems and tools?"
    if c4.button("Role Fit"):
        user_input = "Why are you a fit for a systems analyst role?"

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

        last_12_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state["messages"][-12:]
        ]
        if last_12_messages and last_12_messages[0]["role"] != "user":
            last_12_messages = last_12_messages[1:]

        with st.chat_message("assistant", avatar="💬"):
            st.markdown('<div class="askwil-label">Wil</div>', unsafe_allow_html=True)
            citation_filter = CitationStreamFilter(
                get_reply_stream(api_key, st.session_state["system_prompt"], last_12_messages)
            )
            display_text = st.write_stream(citation_filter)
            render_marker(display_text, citation_filter.keys)
        st.session_state["messages"].append(
            {"role": "assistant", "content": display_text, "sources": citation_filter.keys}
        )
