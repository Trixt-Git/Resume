import json


def load_facts():
    with open("facts.json") as f:
        return json.load(f)


def test_facts_json_parses():
    facts = load_facts()
    assert isinstance(facts, dict)


def test_top_level_keys_present():
    facts = load_facts()
    expected_keys = {
        "identity",
        "current_role",
        "education",
        "career_target",
        "skills",
        "projects",
        "work_history",
        "sensitive_topics",
    }
    assert expected_keys.issubset(facts.keys())


def test_skills_confirmed_is_nonempty_list_of_strings():
    facts = load_facts()
    confirmed = facts["skills"]["confirmed"]
    assert isinstance(confirmed, list)
    assert len(confirmed) > 0
    assert all(isinstance(s, str) for s in confirmed)


def test_projects_have_all_five_keys():
    facts = load_facts()
    expected_keys = {"name", "one_liner", "stack", "details", "outcomes"}
    for project in facts["projects"]:
        assert expected_keys.issubset(project.keys())


def test_sensitive_topics_values_are_strings():
    facts = load_facts()
    for key, value in facts["sensitive_topics"].items():
        assert isinstance(value, str)
        if value == "":
            print(f"WARNING: sensitive_topics.{key} is empty")
