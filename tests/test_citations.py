from citations import parse_citation


def test_well_formed_tag_is_parsed_and_stripped():
    reply = "FloorPlan is my scheduling tool for the RRD press floor.\n[[SOURCES: projects]]"
    display_text, keys = parse_citation(reply)
    assert display_text == "FloorPlan is my scheduling tool for the RRD press floor."
    assert keys == ["projects"]


def test_well_formed_multi_key_tag():
    reply = "I work at RRD while finishing my MS.\n[[SOURCES: current_role, education]]"
    display_text, keys = parse_citation(reply)
    assert display_text == "I work at RRD while finishing my MS."
    assert keys == ["current_role", "education"]


def test_well_formed_none_tag_yields_empty_keys():
    reply = "I haven't worked with that, so I won't claim it.\n[[SOURCES: none]]"
    display_text, keys = parse_citation(reply)
    assert display_text == "I haven't worked with that, so I won't claim it."
    assert keys == []


def test_malformed_tag_with_invalid_key_falls_back_to_raw_text():
    reply = "No — I haven't used that, and I don't claim it.\n[[SOURCES: skillz]]"
    display_text, keys = parse_citation(reply)
    assert display_text == reply
    assert keys is None


def test_malformed_tag_with_broken_syntax_falls_back_to_raw_text():
    reply = "Some answer text.\n[[SOURCES skills]]"
    display_text, keys = parse_citation(reply)
    assert display_text == reply
    assert keys is None


def test_missing_delimiter_falls_back_to_raw_text():
    reply = "Just a plain reply with no citation tag at all."
    display_text, keys = parse_citation(reply)
    assert display_text == reply
    assert keys is None
