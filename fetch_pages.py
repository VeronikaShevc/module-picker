import requests
import time

# # Semester numbers are hardcoded here because we need them to build the
# correct fetch URL before we've downloaded the page. The actual semester
# used in the app's data comes from parse_pages.py, which scrapes it
# directly from each page's content.
modules = {
    # Semester 1
    "CS1002": 1, "CS1007": 1, "IS1901": 1,
    "CS2001": 1, "CS2003": 1, "CS2101": 1,
    "CS3050": 1, "CS3104": 1, "CS3105": 1, "CS3302": 1,
    "CS4102": 1, "CS4105": 1, "CS4201": 1, "CS4302": 1, "CS4402": 1,
    "CS5001": 1, "CS5002": 1, "CS5015": 1, "CS5020": 1, "CS5030": 1,
    "CS5032": 1, "CS5034": 1, "CS5040": 1, "CS5042": 1, "CS5063": 1, "CS5199": 1,

    # Semester 2
    "CS1003": 2, "CS1006": 2,
    "CS2002": 2, "CS2006": 2,
    "CS3052": 2, "CS3101": 2, "CS3102": 2, "CS3106": 2,
    "CS4052": 2, "CS4103": 2, "CS4202": 2, "CS4203": 2, "CS4204": 2, "CS4303": 2,
    "CS5003": 2, "CS5012": 2, "CS5014": 2, "CS5016": 2, "CS5033": 2, "CS5035": 2,
    "CS5041": 2, "CS5044": 2, "CS5052": 2, "CS5055": 2, "CS5201": 2, "ID5059": 2,
}

whole_year_modules = ["CS3099", "CS4098", "CS4099", "CS4796"]
for m in whole_year_modules:
    modules[m] = None  # no semester needed

for code, semester in modules.items():
    if code in whole_year_modules:
        url = f"https://www.st-andrews.ac.uk/subjects/modules/catalogue/?meta_modulecode={code}&meta_ayrs_sand=2026/7"
    else:
        url = f"https://www.st-andrews.ac.uk/subjects/modules/catalogue/?meta_modulecode={code}&meta_ayrs_sand=2026/7&meta_semester_sand={semester}"

    response = requests.get(url)
    with open(f"pages/{code}.html", "w") as f:
        f.write(response.text)
    print(f"Saved {code}")
    time.sleep(1)  # be polite to the server