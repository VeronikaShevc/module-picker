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