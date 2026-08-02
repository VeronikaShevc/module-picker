from app import filter_by_last_year


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