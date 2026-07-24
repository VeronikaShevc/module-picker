import os
import json
import re
from bs4 import BeautifulSoup
all_modules = {}

def parse_assessment(text):
    """Extract exam duration (hours), exam percent, and coursework
    percent from a raw assessment string. Handles decimals in duration
    and different word orders (exam-first or coursework-first)."""

    duration_match = re.search(r'(\d+\.?\d*)-?\s*[Hh]our', text)
    exam_duration = float(duration_match.group(1)) if duration_match else None

    exam_match = re.search(r'[Ee]xam\w*[\s\-=]+(\d+)%', text)
    exam_percent = int(exam_match.group(1)) if exam_match else 0

    coursework_match = re.search(r'[Cc]oursework[\s\-=]+(\d+)%', text)
    coursework_percent = int(coursework_match.group(1)) if coursework_match else 0

    return exam_duration, exam_percent, coursework_percent


for filename in os.listdir("pages"):
    with open(f"pages/{filename}", "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    title = soup.find("h1")
    code = filename.replace(".html", "")
    name = title.text.strip()[title.text.strip().find(" "):].strip()
    credits = soup.find("h3", string="SCOTCAT credits").find_next("p").text.strip()
    semester = soup.find("p", class_="font-scale-3").text.strip().split("Semester ")[1] if "Semester " in soup.find("p", class_="font-scale-3").text.strip() else "Whole Year"

    prereq_tag = soup.find("p", id="prerequisites")
    prerequisites = prereq_tag.text.strip() if prereq_tag else "None"
    antireq_heading = soup.find("h3", string="Anti-requisites")
    anti_requisites = antireq_heading.find_next("p").text.strip() if antireq_heading else "None"

    assessment = soup.find("h2", id="assessment").find_next("p").text.strip()
    exam_duration, exam_percent, coursework_percent = parse_assessment(assessment)

    # print(code, "-", name, "-", credits, "-", assessment, "-", prerequisites, "-", semester)


    all_modules[code] = {
        "name": name,
        "credits": credits,
        "assessment": assessment,
        "exam_duration": exam_duration,
        "exam_percent": exam_percent,
        "coursework_percent": coursework_percent,
        "prerequisites": prerequisites,
        "semester": semester,
        "anti_requisites": anti_requisites
    }

with open("modules.json", "w") as f:
    json.dump(all_modules, f, indent=2)

# print("Saved to modules.json")