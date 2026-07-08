import streamlit as st

from llm_client import get_reply
from prompt_builder import build_system_prompt, load_facts

st.set_page_config(page_title="Ask Wil", page_icon="💬")
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

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
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

        reply = get_reply(api_key, st.session_state["system_prompt"], last_12_messages)
        st.session_state["messages"].append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)
