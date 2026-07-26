from prerequisites import evaluate_prereq, get_necessary_missing
import pytest


def test_and_or_logic_satisfied():
    # basic AND/OR, should pass
    prereq = "CS2002 AND ( CS2101 OR CS2001 )"
    passed = {"CS2002", "CS2001"}
    all_codes = ["CS2002", "CS2001", "CS2101"]
    assert evaluate_prereq(prereq, passed, all_codes) == True


def test_and_or_logic_not_satisfied():
    # same as above but missing the OR part - should fail
    prereq = "CS2002 AND ( CS2101 OR CS2001 )"
    passed = {"CS2002"}
    all_codes = ["CS2002", "CS2001", "CS2101"]
    assert evaluate_prereq(prereq, passed, all_codes) == False


def test_ug_side_used_when_period_touches_module_code():
    # found this bug by accident - period right after a code broke parsing
    prereq = "UNDERGRADUATE - BEFORE TAKING THIS MODULE YOU MUST PASS CS2002. PGT: CS5001 OR CS5002"
    passed = {"CS2002"}
    all_codes = ["CS2002", "CS5001", "CS5002"]
    assert evaluate_prereq(prereq, passed, all_codes) == True


def test_same_year_dependency_detected_as_missing():
    # checks get_necessary_missing actually finds the missing code
    prereq = "CS2002 AND PASS CS3050"
    passed = {"CS2002"}
    all_codes = ["CS2002", "CS3050"]
    missing = get_necessary_missing(prereq, passed, all_codes)
    assert missing == ["CS3050"]


def test_real_world_cs5044_ug_pgt_split():
    # actual prereq text from CS5044, not made up
    prereq = "UNDERGRADUATE - BEFORE TAKING THIS MODULE YOU MUST PASS CS2002 AND (PASS CS2001 OR PASS CS2101). PGT: CS5001 OR CS5002"
    passed = {"CS2002", "CS2001"}
    all_codes = ["CS2002", "CS2001", "CS2101", "CS5001", "CS5002"]
    assert evaluate_prereq(prereq, passed, all_codes) == True


def test_anti_requisite_conflict_detected():
    # passed a module you're not allowed to combine with this one
    anti_req = "YOU CANNOT TAKE THIS MODULE IF YOU TAKE CS3099"
    passed = {"CS3099"}
    all_codes = ["CS3099"]
    assert evaluate_prereq(anti_req, passed, all_codes) == True


def test_comma_separated_and_logic():
    # CS5033 uses a comma instead of "AND" between clauses - had to fix this
    prereq = "PASS CS3099,PASS CS5030"
    passed = {"CS3099", "CS5030"}
    all_codes = ["CS3099", "CS5030"]
    assert evaluate_prereq(prereq, passed, all_codes) == True


def test_ambiguous_missing_brackets_uses_and_before_or_precedence():
    # CS5030 has no brackets at all - relying on normal and/or precedence
    prereq = "CS2002 AND CS2001 OR CS2101"
    passed = {"CS2101"}
    all_codes = ["CS2002", "CS2001", "CS2101"]
    assert evaluate_prereq(prereq, passed, all_codes) == True


def test_external_module_in_prerequisite_raises():
    # VP3135 isn't in our data - this crashes on purpose, app.py catches it
    prereq = "PASS CS3099 OR PASS VP3135"
    passed = set()
    all_codes = ["CS3099"]
    with pytest.raises(SyntaxError):
        evaluate_prereq(prereq, passed, all_codes)


def test_whole_year_module_no_semester_prereq_still_works():
    # whole-year modules don't need special handling here
    prereq = "BEFORE TAKING THIS MODULE YOU MUST PASS CS2002 AND ( PASS CS2101 OR PASS CS2001 )"
    passed = {"CS2002", "CS2101"}
    all_codes = ["CS2002", "CS2101", "CS2001"]
    assert evaluate_prereq(prereq, passed, all_codes) == True


def test_no_missing_when_everything_passed():
    # nothing missing if you've passed it all
    prereq = "CS2002 AND CS3050"
    passed = {"CS2002", "CS3050"}
    all_codes = ["CS2002", "CS3050"]
    missing = get_necessary_missing(prereq, passed, all_codes)
    assert missing == []


def test_cs5052_postgraduate_wording_real_data():
    # uses "POSTGRADUATE" not "PGT:" - different wording, same idea
    prereq = "UNDERGRADUATE STUDENTS MUST HAVE PASSED CS2002 AND (CS2001 OR CS2101). POSTGRADUATE STUDENTS MUST PASS CS5001 BEFORE TAKING THIS MODULE"
    passed = {"CS2002", "CS2001"}
    all_codes = ["CS2002", "CS2001", "CS2101", "CS5001"]
    assert evaluate_prereq(prereq, passed, all_codes) == True


def test_cs3102_take_or_audit_clause():
    # weird one - "TAKE" and "AUDIT" instead of "PASS", plus a subjective bit
    # about "satisfaction of Honours Adviser". Still parses fine somehow.
    prereq = "BEFORE TAKING THIS MODULE YOU MUST PASS CS2002 AND (PASS CS2101 OR PASS CS2001) AND (TAKE CS2003 OR AUDIT CS2003 AND DEMONSTRATE ENGAGING WITH RELEVANT CS2003 MATERIAL TO THE SATISFACTION OF HONOURS ADVISER)"
    passed = {"CS2002", "CS2001", "CS2003"}
    all_codes = ["CS2002", "CS2001", "CS2101", "CS2003"]
    assert evaluate_prereq(prereq, passed, all_codes) == True


def test_cs3102_fails_correctly_without_cs2003():
    # same as above but without CS2003 - should fail this time
    prereq = "BEFORE TAKING THIS MODULE YOU MUST PASS CS2002 AND (PASS CS2101 OR PASS CS2001) AND (TAKE CS2003 OR AUDIT CS2003 AND DEMONSTRATE ENGAGING WITH RELEVANT CS2003 MATERIAL TO THE SATISFACTION OF HONOURS ADVISER)"
    passed = {"CS2002", "CS2001"}
    all_codes = ["CS2002", "CS2001", "CS2101", "CS2003"]
    assert evaluate_prereq(prereq, passed, all_codes) == False