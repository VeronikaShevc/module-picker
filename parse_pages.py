import os
from bs4 import BeautifulSoup

all_modules = {}

for filename in os.listdir("pages"):
    with open(f"pages/{filename}", "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    title = soup.find("h1")
    code = filename.replace(".html", "")
    name = title.text.strip()[title.text.strip().find(" "):].strip()
    credits = soup.find("h3", string="SCOTCAT credits").find_next("p").text.strip()
    assessment = soup.find("h2", id="assessment").find_next("p").text.strip()
    prereq_tag = soup.find("p", id="prerequisites")
    prerequisites = prereq_tag.text.strip() if prereq_tag else "None"

    print(code, "-", name, "-", credits, "-", assessment, "-", prerequisites)

    all_modules[code] = {
        "name": name,
        "credits": credits,
        "assessment": assessment,
        "prerequisites": prerequisites
    }

import json

with open("modules.json", "w") as f:
    json.dump(all_modules, f, indent=2)

print("Saved to modules.json")