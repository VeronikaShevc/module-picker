from app import filter_by_last_year, infer_last_year, get_module_status, filter_by_assessment, modules_data
import pytest

def test_checklist_shows_up_to_and_including_year():
    # finished Year 2 -> checklist shows Year 1 and Year 2 only
    data = {
        "CS1002": {}, "CS2001": {}, "CS3050": {}, "CS4099": {},
    }
    result = filter_by_last_year(data, "2", "checklist")
    assert set(result.keys()) == {"CS1002", "CS2001"}


def test_results_year0_shows_only_year1():
    # brand new student -> only Year 1 modules count as "next"
    data = {
        "CS1002": {}, "CS2001": {}, "CS3050": {}, "CS4099": {},
    }
    result = filter_by_last_year(data, "0", "results")
    assert set(result.keys()) == {"CS1002"}


def test_results_year3_shows_year3_4_and_5():
    # finished Year 3 -> Year 3/4/5 all show up, since Honours
    # students can pick from any of these
    data = {
        "CS3050": {}, "CS4099": {}, "CS5001": {}, "CS2001": {},
    }
    result = filter_by_last_year(data, "3", "results")
    assert set(result.keys()) == {"CS3050", "CS4099", "CS5001"}


def test_results_year5_shows_everything():
    # "5" means "All" - no filtering at all
    data = {"CS1002": {}, "CS3050": {}, "CS5001": {}}
    result = filter_by_last_year(data, "5", "results")
    assert result == data


def test_no_last_year_returns_everything_unfiltered():
    # nothing selected yet - shouldn't filter anything out
    data = {"CS1002": {}, "CS3050": {}}
    result = filter_by_last_year(data, None, "results")
    assert result == data


def test_invalid_last_year_returns_everything_unfiltered():
    # garbage value instead of a real year - should fail safe, not crash
    data = {"CS1002": {}, "CS3050": {}}
    result = filter_by_last_year(data, "invalid", "results")
    assert result == data


def test_invalid_mode_returns_everything_unfiltered():
    # mode isn't "checklist" or "results" at all - should fail safe too
    data = {"CS1002": {}, "CS3050": {}}
    result = filter_by_last_year(data, "2", "invalid_mode")
    assert result == data


def test_checklist_year0_shows_only_year0():
    # Note: no real module code has "0" as its year digit, so this
    # is a made-up scenario just to check the mechanics work. In
    # real use, checklist mode for Year 0 always comes back empty,
    # since new arrivals haven't passed anything yet.
    data = {
        "CS0001": {}, "CS1002": {}, "CS2001": {}, "CS3050": {},
    }
    result = filter_by_last_year(data, "0", "checklist")
    assert set(result.keys()) == {"CS0001"}


def test_checklist_year5_shows_everything():
    # "5" (All) in checklist mode too - should show every module
    data = {
        "CS1002": {}, "CS2001": {}, "CS3050": {}, "CS4099": {},
    }
    result = filter_by_last_year(data, "5", "checklist")
    assert result == data


def test_checklist_invalid_last_year_returns_everything_unfiltered():
    # same garbage-input check, but for checklist mode specifically
    data = {"CS1002": {}, "CS3050": {}}
    result = filter_by_last_year(data, "invalid", "checklist")
    assert result == data

#----------

def test_infer_last_year_returns_highest_year_digit():
    # given a set of passed modules, should return the highest year digit
    passed_set = {"CS1002", "CS2001", "CS3050"}
    result = infer_last_year(passed_set)
    assert result == "3"

def test_infer_last_year_with_empty_set_returns_zero():
    # if no modules have been passed, should return "0"
    passed_set = set()
    result = infer_last_year(passed_set)
    assert result == "0"

def test_infer_last_year_with_mixed_numeric_and_non_numeric():
    # if the year digit is mixed, it should return the highest numeric year
    passed_set = {"CS1A02", "CS2001", "CS3C50"}
    result = infer_last_year(passed_set)
    assert result == "3"

def test_infer_last_year_with_single_module():
    # if only one module is passed, it should return its year digit
    passed_set = {"CS2001"}
    result = infer_last_year(passed_set)
    assert result == "2"

def test_infer_last_year_with_non_numeric_year_digit():
    # if the year digit is non-numeric, it should raise a ValueError
    passed_set = {"CSX001"}
    with pytest.raises(ValueError):
        infer_last_year(passed_set)

#----------

def test_get_module_status_eligible():
    # module with no prerequisites should be eligible
    code = "CS1002"
    details = {"prerequisites": "None", "anti_requisites": "None"}
    passed_set = set()
    all_codes = {"CS1002"}
    status, missing = get_module_status(code, details, passed_set, all_codes)
    assert status == "eligible"
    assert missing == []


def test_get_module_status_not_eligible_due_to_prereq():
    # real CS3050-style prereq: needs CS2002 AND (CS2101 OR CS2001) -
    # student has passed neither, so should be blocked
    code = "CS3050"
    details = {
        "prerequisites": "BEFORE TAKING THIS MODULE YOU MUST PASS CS2002 AND ( PASS CS2101 OR PASS CS2001 )",
        "anti_requisites": "None"
    }
    passed_set = set()
    all_codes = {"CS2002", "CS2101", "CS2001", "CS3050"}
    status, missing = get_module_status(code, details, passed_set, all_codes)
    assert status == "not_eligible"
    assert missing == []


def test_get_module_status_pending_due_to_same_year_prereq():
    # real CS3052-style: needs CS2002 (already passed) AND CS3050 (a
    # same-year module not yet taken) - should be pending, not blocked
    code = "CS3052"
    details = {
        "prerequisites": "BEFORE TAKING THIS MODULE YOU MUST PASS CS2002 AND PASS CS3050",
        "anti_requisites": "None"
    }
    passed_set = {"CS2002"}
    all_codes = {"CS2002", "CS3050", "CS3052"}
    status, missing = get_module_status(code, details, passed_set, all_codes)
    assert status == "pending"
    assert missing == ["CS3050"]


def test_get_module_status_not_eligible_due_to_anti_requisite():
    # real CS5030-style: anti-requisite blocks it if CS3099 was passed,
    # even though there are no prerequisites at all to satisfy
    code = "CS5030"
    details = {
        "prerequisites": "None",
        "anti_requisites": "YOU CANNOT TAKE THIS MODULE IF YOU TAKE CS3099"
    }
    passed_set = {"CS3099"}
    all_codes = {"CS3099", "CS5030"}
    status, missing = get_module_status(code, details, passed_set, all_codes)
    assert status == "not_eligible"
    assert missing == []


def test_get_module_status_eligible_when_anti_requisite_not_passed():
    # same module as above, but the conflicting module was NOT passed -
    # should be eligible, since there's no real conflict
    code = "CS5030"
    details = {
        "prerequisites": "None",
        "anti_requisites": "YOU CANNOT TAKE THIS MODULE IF YOU TAKE CS3099"
    }
    passed_set = set()
    all_codes = {"CS3099", "CS5030"}
    status, missing = get_module_status(code, details, passed_set, all_codes)
    assert status == "eligible"
    assert missing == []


def test_get_module_status_unclear_when_anti_requisite_module_unknown():
    # real CS3050-style: anti-requisite mentions PY4612, a module from
    # a different subject we don't have data on - can't verify, so
    # should be unclear, not silently assumed fine
    code = "CS3050"
    details = {
        "prerequisites": "None",
        "anti_requisites": "YOU CANNOT TAKE THIS MODULE IF YOU TAKE PY4612"
    }
    passed_set = set()
    all_codes = {"CS3050"}  # PY4612 deliberately not included
    status, missing = get_module_status(code, details, passed_set, all_codes)
    assert status == "unclear"
    assert missing == []


def test_get_module_status_unclear_when_prereq_cannot_be_parsed():
    # real CS1002-style: prerequisite is a grade requirement, not a
    # module code at all - the boolean parser has nothing to work with
    code = "CS1002"
    details = {
        "prerequisites": "BEFORE TAKING THIS MODULE YOU MUST HAVE MATHEMATICS (EITHER HIGHER OR A-LEVEL AT GRADE A OR BETTER)",
        "anti_requisites": "None"
    }
    passed_set = set()
    all_codes = {"CS1002"}
    status, missing = get_module_status(code, details, passed_set, all_codes)
    assert status == "unclear"
    assert missing == []


def test_get_module_status_eligible_with_or_logic_satisfied():
    # real CS2002-style: needs CS2001 OR CS2101 - student has only
    # passed CS2101, which alone should be enough
    code = "CS2002"
    details = {
        "prerequisites": "BEFORE TAKING THIS MODULE YOU MUST PASS CS2001 OR PASS CS2101",
        "anti_requisites": "None"
    }
    passed_set = {"CS2101"}
    all_codes = {"CS2001", "CS2101", "CS2002"}
    status, missing = get_module_status(code, details, passed_set, all_codes)
    assert status == "eligible"
    assert missing == []

#----------

def test_filter_by_assessment_filters_correctly():
    # given a set of modules, should filter by the specified assessment criteria
    data = {
        "CS1002": {}, "CS2001": {}, "CS3050": {}, "CS4099": {},
    }
    # Assume modules_data has been defined in app.py with appropriate values
    result = filter_by_assessment(data, exam_percent=60, coursework_percent=None, exam_duration=None)
    # Check that only modules with exam_percent == 50 are included
    for code in result.keys():
        assert modules_data[code]["exam_percent"] == 60

def test_filter_by_assessment_no_filters_returns_all():
    # if no assessment criteria are specified, should return all modules unfiltered
    data = {
        "CS1002": {}, "CS2001": {}, "CS3050": {}, "CS4099": {},
    }
    result = filter_by_assessment(data, exam_percent=None, coursework_percent=None, exam_duration=None)
    assert result == data

def test_filter_by_assessment_multiple_filters():
    # should filter by multiple criteria simultaneously - using a real
    # combination that actually exists in the data (60/40 split, 2.5hr exam)
    data = {
        "CS1002": {}, "CS2001": {}, "CS3050": {}, "CS4099": {},
    }
    result = filter_by_assessment(data, exam_percent=60, coursework_percent=40, exam_duration=2.5)
    assert len(result) > 0  # make sure the loop below actually has something to check
    for code in result.keys():
        assert modules_data[code]["exam_percent"] == 60
        assert modules_data[code]["coursework_percent"] == 40
        assert modules_data[code]["exam_duration"] == 2.5
    
def test_filter_by_assessment_no_matching_modules():
    # if no modules match the specified criteria, should return an empty dict
    data = {
        "CS1002": {}, "CS2001": {}, "CS3050": {}, "CS4099": {},
    }
    result = filter_by_assessment(data, exam_percent=99, coursework_percent=99, exam_duration=99)
    assert result == {}
