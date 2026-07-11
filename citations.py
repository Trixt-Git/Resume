import re

SOURCE_TAG_PATTERN = re.compile(r"\[\[SOURCES:\s*(.*?)\]\]\s*$", re.DOTALL)

VALID_KEYS = {
    "identity", "career_narrative", "current_role", "education", "career_target",
    "skills", "projects", "work_history", "personal", "sensitive_topics",
}


def parse_citation(reply: str) -> tuple[str, list[str] | None]:
    """Splits a raw model reply into (display_text, source_keys).

    On a well-formed [[SOURCES: ...]] tag, returns the reply with the tag
    stripped and a (possibly empty, for "none") list of valid keys.
    On any parsing failure (missing tag, malformed tag, unknown key),
    returns the original reply unmodified and None — callers should
    render the answer with no citation line rather than error.
    """
    match = SOURCE_TAG_PATTERN.search(reply)
    if not match:
        return reply, None

    raw_keys = [k.strip() for k in match.group(1).split(",") if k.strip()]
    if not raw_keys:
        return reply, None

    if raw_keys == ["none"]:
        keys: list[str] = []
    else:
        if not all(k in VALID_KEYS for k in raw_keys):
            return reply, None
        keys = raw_keys

    display_text = reply[: match.start()].rstrip()
    return display_text, keys


class CitationStreamFilter:
    """Wraps a raw text-chunk stream: yields chunks safe to display live,
    withholding a trailing '[[' onward until the stream ends (it might be
    the start of a [[SOURCES: ...]] tag). Once exhausted, any withheld
    text that turns out NOT to be a valid tag is flushed as a final
    chunk, so nothing is silently dropped — the raw tag itself is never
    displayed either way. After iteration, .raw_text holds the full
    original text and .keys holds the parsed source keys (or None)."""

    def __init__(self, chunks):
        self._chunks = chunks
        self.raw_text = ""
        self.keys: list[str] | None = None

    def __iter__(self):
        buffer = ""
        for chunk in self._chunks:
            buffer += chunk
            self.raw_text += chunk
            idx = buffer.rfind("[[")
            if idx == -1:
                safe, buffer = buffer, ""
            else:
                safe, buffer = buffer[:idx], buffer[idx:]
            if safe:
                yield safe

        display_text, keys = parse_citation(self.raw_text)
        self.keys = keys
        already_emitted_len = len(self.raw_text) - len(buffer)
        leftover_visible = display_text[already_emitted_len:]
        if leftover_visible:
            yield leftover_visible
