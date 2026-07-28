from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from prerequisites import evaluate_prereq, find_codes_in_string, get_necessary_missing, all_codes
import json

# Load all the scraped module data once
with open("modules.json", "r") as f:
    modules_data = json.load(f)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# --- Helper functions ---

def infer_last_year(passed_set):
    """Work out the student's last completed year by looking at the
    highest year digit among the modules they've ticked as passed."""
    max_year = 0
    for element in passed_set:
        if int(element[2]) > max_year:
            max_year = int(element[2])
    return str(max_year)


def filter_by_last_year(data, last_year, mode):
    """Filter a list of modules down to only the ones relevant to a
    student's last completed year. 'checklist' mode shows everything up
    to and including that year (for ticking what's passed). 'results'
    mode shows what opens up next."""

    if mode == "checklist":
        # Homepage checklist: show every module from Year 1 up to and
        # including the year the student just finished, so they can
        # tick what they've passed.
        if last_year in ["0", "1", "2", "3", "4", "5"]:
            return {code: value for code, value in data.items() if code[2] <= last_year}

    elif mode == "results":
        # Results page: show what becomes available NEXT, based on the
        # year just finished. Year 3/4 overlap because Honours students
        # can pick from both.
        if last_year == "0":
            return {code: value for code, value in data.items() if code[2] == "1"}
        elif last_year == "1":
            return {code: value for code, value in data.items() if code[2] == "2"}
        elif last_year == "2":
            return {code: value for code, value in data.items() if code[2] == "3"}
        elif last_year == "3":
            return {code: value for code, value in data.items() if code[2] in ["3", "4", "5"]}
        elif last_year == "4":
            return {code: value for code, value in data.items() if code[2] in ["4", "5"]}
        elif last_year == "5":
            # "All" - no filtering.
            return data

    # No last_year given at all - don't filter anything.
    return data


def get_module_status(code, details, passed_set, all_codes):
    """Work out whether a single module is eligible, not eligible,
    pending (blocked only by a same-year module), or unclear (the
    prerequisite text couldn't be parsed). Returns (status, missing_list)."""

    # Anti-requisites first: if the student has already passed something
    # that conflicts with this module, it's blocked no matter what the
    # prerequisites say.
    anti_req_string = details.get("anti_requisites", "None")
    if anti_req_string != "None":
        mentioned = find_codes_in_string(anti_req_string, all_codes)
        if not mentioned:
            # The anti-requisite mentions a module we don't have data on
            # (from another subject). Can't verify this.
            return "unclear", []
        if evaluate_prereq(anti_req_string, passed_set, all_codes):
            return "not_eligible", []

    # No prerequisites at all - automatically eligible.
    prereq_string = details["prerequisites"]
    if prereq_string == "None":
        return "eligible", []

    try:
        if evaluate_prereq(prereq_string, passed_set, all_codes):
            return "eligible", []

        # Not eligible yet. If the only thing missing
        # is a module from the same year, the student would take it in
        # Semester 1 of that year anyway - so it's not blocked,
        # just "pending" until they finish Semester 1.
        missing = get_necessary_missing(prereq_string, passed_set, all_codes)
        if missing and all(c[2] == code[2] for c in missing):
            return "pending", missing

        return "not_eligible", []

    except Exception:
        # The prerequisite text couldn't be parsed at all (it's a
        # grade requirement or mentions a module outside our data).
        return "unclear", []


# Routes

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, last_year: str = None, exam_percent: str = None, coursework_percent: str = None, exam_duration: str = None):
    """Homepage: show the checklist of modules a student can tick as passed."""

    filtered = modules_data
    exam_percent = int(exam_percent) if exam_percent else None
    coursework_percent = int(coursework_percent) if coursework_percent else None
    exam_duration = float(exam_duration) if exam_duration else None

    if exam_percent is not None:
        filtered = {code: details for code, details in filtered.items() if details["exam_percent"] == exam_percent}
    if coursework_percent is not None:
        filtered = {code: details for code, details in filtered.items() if details["coursework_percent"] == coursework_percent}
    if exam_duration is not None:
        filtered = {code: details for code, details in filtered.items() if details["exam_duration"] == exam_duration}

    filtered = filter_by_last_year(filtered, last_year, "checklist")

    return templates.TemplateResponse(request=request, name="index.html", context={"modules": filtered, "last_year": last_year, "exam_percent": exam_percent, "exam_duration": exam_duration})


@app.get("/check", response_class=HTMLResponse)
async def check_eligibility(request: Request, passed: list[str] = Query(default=[]), last_year: str = Query(default=None), exam_percent: str = None, coursework_percent: str = None, exam_duration: str = None):
    """Results page: work out eligibility for every module given what's been passed."""

    passed_set = set(passed)

    exam_percent = int(exam_percent) if exam_percent else None
    coursework_percent = int(coursework_percent) if coursework_percent else None
    exam_duration = float(exam_duration) if exam_duration else None

    # Special case: a brand new student hasn't passed anything yet, but
    # Year 1 modules are all compulsory and guaranteed by the programme
    # structure - so there's no real "eligibility" question here at all.
    if last_year == "0":
        results = {code: "eligible" for code, details in modules_data.items() if code[2] == "1"}
        return templates.TemplateResponse(request=request, name="check.html", context={"results": results, "passed": passed_set, "modules": modules_data, "pending_info": {}})

    # Normal case: work out the status of every single module one at a time.
    results = {}
    pending_info = {}
    for code, details in modules_data.items():
        if code in passed_set:
            results[code] = "already_passed"
            continue
        status, missing = get_module_status(code, details, passed_set, all_codes)
        results[code] = status
        if missing:
            # Remember which specific module is blocking a "pending" result,
            # so we can tell the user exactly what to complete first.
            pending_info[code] = missing

    # Only show the modules relevant to what's coming next.
    results = filter_by_last_year(results, last_year, "results")

    if exam_percent is not None:
        results = {code: status for code, status in results.items() if modules_data[code]["exam_percent"] == exam_percent}
    if coursework_percent is not None:
        results = {code: status for code, status in results.items() if modules_data[code]["coursework_percent"] == coursework_percent}
    if exam_duration is not None:
        results = {code: status for code, status in results.items() if modules_data[code]["exam_duration"] == exam_duration}

    return templates.TemplateResponse(request=request, name="check.html", context={"results": results, "passed": passed_set, "modules": modules_data, "pending_info": pending_info, "last_year": last_year})