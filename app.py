from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from prerequisites import evaluate_prereq, find_codes_in_string, get_necessary_missing, all_codes
import json

with open("modules.json", "r") as f:
    modules_data = json.load(f)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def filter_by_last_year(data, last_year, mode):
    """Filter a list of modules down to only the ones relevant to a
    student's last completed year. 'checklist' mode shows everything up
    to and including that year (for ticking what's passed). 'results'
    mode shows what opens up next."""
    if mode == "checklist":
        if last_year in ["0", "1", "2", "3", "4", "5"]:
            return {code: value for code, value in data.items() if code[2] <= last_year}
    elif mode == "results":
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
            return data
    return data


def get_module_status(code, details, passed_set, all_codes):
    """Work out whether a single module is eligible, not eligible,
    pending (blocked only by a same-year module), or unclear (the
    prerequisite text couldn't be parsed). Returns (status, missing_list)."""

    anti_req_string = details.get("anti_requisites", "None")
    if anti_req_string != "None":
        mentioned = find_codes_in_string(anti_req_string, all_codes)
        if mentioned and evaluate_prereq(anti_req_string, passed_set, all_codes):
            return "not_eligible", []

    prereq_string = details["prerequisites"]
    if prereq_string == "None":
        return "eligible", []

    try:
        if evaluate_prereq(prereq_string, passed_set, all_codes):
            return "eligible", []

        missing = get_necessary_missing(prereq_string, passed_set, all_codes)
        if missing and all(c[2] == code[2] for c in missing):
            return "pending", missing
        return "not_eligible", []
    except Exception:
        return "unclear", []


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, semester: str = None, year: str = None, last_year: str = None):
    """Homepage: show the checklist of modules a student can tick as passed."""
    filtered = modules_data
    if semester:
        filtered = {code: details for code, details in filtered.items() if details["semester"] == semester}
    if year:
        filtered = {code: details for code, details in filtered.items() if code[2] == year}
    filtered = filter_by_last_year(filtered, last_year, "checklist")
    return templates.TemplateResponse(request=request, name="index.html", context={"modules": filtered, "last_year": last_year})


@app.get("/check", response_class=HTMLResponse)
async def check_eligibility(request: Request, passed: list[str] = Query(default=[]), last_year: str = Query(default=None)):
    """Results page: work out eligibility for every module given what's been passed."""
    passed_set = set(passed)

    if last_year == "0":
        results = {code: "eligible" for code, details in modules_data.items() if code[2] == "1"}
        return templates.TemplateResponse(request=request, name="check.html", context={"results": results, "passed": passed_set, "modules": modules_data, "pending_info": {}})

    results = {}
    pending_info = {}
    for code, details in modules_data.items():
        status, missing = get_module_status(code, details, passed_set, all_codes)
        results[code] = status
        if missing:
            pending_info[code] = missing

    results = filter_by_last_year(results, last_year, "results")
    return templates.TemplateResponse(request=request, name="check.html", context={"results": results, "passed": passed_set, "modules": modules_data, "pending_info": pending_info})