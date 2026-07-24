from prerequisites import evaluate_prereq

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