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