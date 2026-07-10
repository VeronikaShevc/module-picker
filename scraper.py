import requests
from bs4 import BeautifulSoup

url = "https://www.st-andrews.ac.uk/subjects/modules/catalogue/?meta_modulecode=CS1002&meta_ayrs_sand=2026/7&meta_semester_sand=1"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

title = soup.find("h1")
print(title.text.strip()[:title.text.strip().find(" ")])
print("------------------------------")

code = soup.find("h1")
print(code.text.strip()[code.text.strip().find(" "):].strip())
print("------------------------------")

credits = soup.find("h3", string="SCOTCAT credits")
print(credits.find_next("p").text.strip())
print("------------------------------")


assessment = soup.find("h2", id="assessment")


coursework_percentage = assessment.find_next("p").text.strip().split("=")[1].strip()
print(coursework_percentage)
print("------------------------------")

# exam_percentage = assessment.find_next("h3", string="Exam")
# print(exam_percentage.find_next("p").text.strip().split("=")[1].strip())
# print("------------------------------")