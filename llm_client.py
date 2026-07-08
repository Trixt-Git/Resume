import anthropic

MODEL = "claude-haiku-4-5-20251001"


def get_reply(api_key: str, system_prompt: str, messages: list[dict]) -> str:
    """messages: [{"role": "user"|"assistant", "content": str}, ...]
    Returns assistant text, or the LOCKED error string on any exception."""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL,
            max_tokens=400,
            temperature=0.2,
            system=[{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}],
            messages=messages,
        )
        return response.content[0].text
    except Exception as e:
        print(f"[llm_client] {type(e).__name__}: {e}")
        return "Something went wrong on my end — please try that question again in a moment."
