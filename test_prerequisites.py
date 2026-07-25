import pytest
from prerequisites import evaluate_prereq, get_necessary_missing


def test_and_or_logic_satisfied():
    prereq = "CS2002 AND ( CS2101 OR CS2001 )"
    passed = {"CS2002", "CS2001"}
    all_codes = ["CS2002", "CS2001", "CS2101"]
    assert evaluate_prereq(prereq, passed, all_codes) == True


def test_and_or_logic_not_satisfied():
    prereq = "CS2002 AND ( CS2101 OR CS2001 )"
    passed = {"CS2002"}
    all_codes = ["CS2002", "CS2001", "CS2101"]
    assert evaluate_prereq(prereq, passed, all_codes) == False


def test_ug_side_used_when_period_touches_module_code():
    # Edge case: a period directly after a module code, before the
    # UG/PGT split marker.
    prereq = "UNDERGRADUATE - BEFORE TAKING THIS MODULE YOU MUST PASS CS2002. PGT: CS5001 OR CS5002"
    passed = {"CS2002"}
    all_codes = ["CS2002", "CS5001", "CS5002"]
    assert evaluate_prereq(prereq, passed, all_codes) == True


def test_same_year_dependency_detected_as_missing():
    prereq = "CS2002 AND PASS CS3050"
    passed = {"CS2002"}
    all_codes = ["CS2002", "CS3050"]
    missing = get_necessary_missing(prereq, passed, all_codes)
    assert missing == ["CS3050"]


def test_real_world_cs5044_ug_pgt_split():
    prereq = "UNDERGRADUATE - BEFORE TAKING THIS MODULE YOU MUST PASS CS2002 AND (PASS CS2001 OR PASS CS2101). PGT: CS5001 OR CS5002"
    passed = {"CS2002", "CS2001"}
    all_codes = ["CS2002", "CS2001", "CS2101", "CS5001", "CS5002"]
    assert evaluate_prereq(prereq, passed, all_codes) == True

def test_anti_requisite_conflict_detected():
    anti_req = "YOU CANNOT TAKE THIS MODULE IF YOU TAKE CS3099"
    passed = {"CS3099"}
    all_codes = ["CS3099"]
    assert evaluate_prereq(anti_req, passed, all_codes) == True

def test_comma_separated_and_logic():
    # CS5033-style: two "must pass" clauses joined by a comma instead
    # of the word AND. Commas are treated the same as AND.
    prereq = "PASS CS3099,PASS CS5030"
    passed = {"CS3099", "CS5030"}
    all_codes = ["CS3099", "CS5030"]
    assert evaluate_prereq(prereq, passed, all_codes) == True

def test_ambiguous_missing_brackets_uses_and_before_or_precedence():
    # CS5030-style: "A AND B OR C" with no brackets at all. Python's
    # own and/or precedence applies: (A AND B) OR C.
    prereq = "CS2002 AND CS2001 OR CS2101"
    passed = {"CS2101"}  # only the OR branch is satisfied
    all_codes = ["CS2002", "CS2001", "CS2101"]
    assert evaluate_prereq(prereq, passed, all_codes) == True

def test_external_module_in_prerequisite_raises():
    # VP3135-style: a prerequisite mentions a module outside our
    # dataset entirely. This crashes at the evaluate_prereq level -
    # app.py catches this and converts it to "unclear" status
    prereq = "PASS CS3099 OR PASS VP3135"
    passed = set()
    all_codes = ["CS3099"]
    with pytest.raises(SyntaxError):
        evaluate_prereq(prereq, passed, all_codes)

def test_whole_year_module_no_semester_prereq_still_works():
    # CS3099 is a whole-year module with no semester field relevant to
    # prerequisite logic - the parser doesn't care about semester at all.
    prereq = "BEFORE TAKING THIS MODULE YOU MUST PASS CS2002 AND ( PASS CS2101 OR PASS CS2001 )"
    passed = {"CS2002", "CS2101"}
    all_codes = ["CS2002", "CS2101", "CS2001"]
    assert evaluate_prereq(prereq, passed, all_codes) == True


def test_no_missing_when_everything_passed():
    from prerequisites import get_necessary_missing
    prereq = "CS2002 AND CS3050"
    passed = {"CS2002", "CS3050"}
    all_codes = ["CS2002", "CS3050"]
    missing = get_necessary_missing(prereq, passed, all_codes)
    assert missing == []