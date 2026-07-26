from app import filter_by_last_year

def test_checklist_shows_up_to_and_including_year():
    data = {
        "CS1002": {}, "CS2001": {}, "CS3050": {}, "CS4099": {},
    }
    result = filter_by_last_year(data, "2", "checklist")
    assert set(result.keys()) == {"CS1002", "CS2001"}


def test_results_year0_shows_only_year1():
    data = {
        "CS1002": {}, "CS2001": {}, "CS3050": {}, "CS4099": {},
    }
    result = filter_by_last_year(data, "0", "results")
    assert set(result.keys()) == {"CS1002"}


def test_results_year3_shows_year3_4_and_5():
    data = {
        "CS3050": {}, "CS4099": {}, "CS5001": {}, "CS2001": {},
    }
    result = filter_by_last_year(data, "3", "results")
    assert set(result.keys()) == {"CS3050", "CS4099", "CS5001"}


def test_results_year5_shows_everything():
    data = {"CS1002": {}, "CS3050": {}, "CS5001": {}}
    result = filter_by_last_year(data, "5", "results")
    assert result == data


def test_no_last_year_returns_everything_unfiltered():
    data = {"CS1002": {}, "CS3050": {}}
    result = filter_by_last_year(data, None, "results")
    assert result == data