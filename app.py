from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

with open("modules.json", "r") as f:
    modules_data = json.load(f)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, semester: str = None, year: str = None):
    filtered = modules_data
    if semester:
        filtered = {code: details for code, details in filtered.items() if details["semester"] == semester}
    if year:
        filtered = {code: details for code, details in filtered.items() if code[2] == year}
    return templates.TemplateResponse(request=request, name="index.html", context={"modules": filtered})


from fastapi import Query

@app.get("/check", response_class=HTMLResponse)
async def check_eligibility(request: Request, passed: list[str] = Query(default=[])):
    from prerequisites import evaluate_prereq, all_codes
    passed_set = set(passed)
    results = {}
    for code, details in modules_data.items():
        prereq_string = details["prerequisites"]
        if prereq_string == "None": results[code] = "eligible"
        else:
            # if code == "CS1003":
            #     print("DEBUG - prereq string:", prereq_string)
            #     print("DEBUG - passed set:", passed_set)
            try:
                is_eligible = evaluate_prereq(prereq_string, passed_set, all_codes)
                if is_eligible: results[code] = "eligible"
                else: results[code] = "not_eligible"
            except Exception as e: results[code] = "unclear"
    return templates.TemplateResponse(request=request, name="check.html", context={"results": results, "passed": passed_set, "modules": modules_data})