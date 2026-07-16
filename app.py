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
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, semester: str = None):
    if semester:
        filtered = {code: details for code, details in modules_data.items() if details["semester"] == semester}
    else:
        filtered = modules_data
    return templates.TemplateResponse(request=request, name="index.html", context={"modules": filtered, "selected_semester": semester})