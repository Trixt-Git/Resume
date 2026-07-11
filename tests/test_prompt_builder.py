from prompt_builder import load_facts, build_system_prompt


def test_build_system_prompt_contains_fallback_sentence():
    facts = load_facts()
    prompt = build_system_prompt(facts)
    assert "I haven't worked with that, so I won't claim it." in prompt


def test_build_system_prompt_contains_rule5_anchor():
    facts = load_facts()
    prompt = build_system_prompt(facts)
    assert "I can't do that — I only answer from" in prompt


def test_build_system_prompt_contains_rule8_anchor():
    facts = load_facts()
    prompt = build_system_prompt(facts)
    assert "That's not accurate — I haven't done that" in prompt


def test_build_system_prompt_contains_rule9_anchors():
    facts = load_facts()
    prompt = build_system_prompt(facts)
    assert "more C-3PO than" in prompt
    assert "only useful within my programming" in prompt
    assert "loaded me with career facts" in prompt
    assert "not the right machine for that one" in prompt
    assert "still working out the kinks" in prompt
    assert "should not be trusted with" in prompt
    assert "weirdly useful in a very narrow lane" in prompt


def test_build_system_prompt_contains_name():
    facts = load_facts()
    prompt = build_system_prompt(facts)
    assert facts["identity"]["name"] in prompt


def test_build_system_prompt_contains_skills():
    facts = load_facts()
    prompt = build_system_prompt(facts)
    assert "skills" in prompt


def test_build_system_prompt_has_no_placeholder():
    facts = load_facts()
    prompt = build_system_prompt(facts)
    assert "{FACTS_JSON}" not in prompt
