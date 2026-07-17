import json
import re

from pyparsing import line

with open("modules.json", "r") as f:
    modules_data = json.load(f)

all_codes = modules_data.keys()

def find_codes_in_string(text, all_know_codes):
    found = []
    for code in all_know_codes:
        if code in text: found.append(code)
    return found




# test_string = "UNDERGRADUATE - BEFORE TAKING THIS MODULE YOU MUST PASS " \
# "CS2002 AND (PASS CS2001 OR PASS CS2101). PGT: CS5001 OR CS5002"
# print(find_codes_in_string(test_string, all_codes))

# def has_ug_pgt_split(text):
#     student = ""
#     if "UG:" in text or "UNDERGRADUATE" in text:
#         student += "UG"
#         print("UG")
#     if "PGT:" in text or "POSTGRADUATE" in text:
#         student += "PGT"
#         print("PGT")
#     return student

# plain_string = "BEFORE TAKING THIS MODULE YOU MUST PASS CS1002"
# print(has_ug_pgt_split(plain_string))

# split_string = "UNDERGRADUATE - BEFORE TAKING THIS MODULE YOU MUST PASS CS2002 AND (PASS CS2001 OR PASS CS2101). PGT: CS5001 OR CS5002"
# print(has_ug_pgt_split(split_string))


# def split_ug_pgt(text):
#     if "UG:" in text or "UNDERGRADUATE" in text:
#         ug_text = text.split("PGT:")[0]
#         pgt_text = text.split("PGT:" or "POSTGRADUATE")[1]
#         return ug_text, pgt_text
#     else:
#         return text, None
    
# split_string = "UNDERGRADUATE - BEFORE TAKING THIS MODULE YOU MUST PASS CS2002 AND (PASS CS2001 OR PASS CS2101). PGT: CS5001 OR CS5002"
# print(split_ug_pgt(split_string))

# plain_string = "BEFORE TAKING THIS MODULE YOU MUST PASS CS1002"
# print(split_ug_pgt(plain_string))


#I want to build a parser to do AND/OR/brackets parsing 
# of the prerequisites text. I want to be able to parse 
# the text and return a list of lists of module codes, where 
# each list represents a group of modules that can be taken together. 
# For example, the text "BEFORE TAKING THIS MODULE YOU MUST 
# PASS CS1002 AND (PASS CS2001 OR PASS CS2101)" should return
#  [["CS1002"], ["CS2001", "CS2101"]].

# string = "UNDERGRADUATE - BEFORE TAKING THIS MODULE YOU MUST PASS CS2002 AND (PASS CS2001 OR PASS CS2101). PGT: CS5001 OR CS5002"

# fields = re.split(r'\s*(AND|OR|\(|\))\s*', string)
# for field in fields:
#     print(field)


def substitute_booleans(text, passed_modules, all_codes):
    for code in all_codes:
        if code in passed_modules:
            text = text.replace(code, "True")
        else:
            text = text.replace(code, "False")
    return text

prereq = "CS2002 AND ( CS2101 OR CS2001 )"
passed = {"CS2002", "CS2001"}
result = substitute_booleans(prereq, passed, all_codes)
print(result)


def clean_prereq_string(text, all_codes):
    words = text.replace("(", " ( ").replace(")", " ) ").split()
    keep = []
    for word in words:
        if word in all_codes or word in ["AND", "OR", "(", ")"]:
            keep.append(word)
    return " ".join(keep)




def evaluate_prereq(text, passed_modules, all_codes):
    cleaned = clean_prereq_string(text, all_codes)
    substituted = substitute_booleans(cleaned, passed_modules, all_codes)
    substituted = substituted.replace("AND", "and").replace("OR", "or")
    result = eval(substituted)
    return result




prereq = "CS2002 AND ( CS2101 OR CS2001 )"
passed = {"CS2002", "CS2001"}
print(evaluate_prereq(prereq, passed, all_codes))


passed = {"CS2002"}
print(evaluate_prereq(prereq, passed, all_codes))


real_prereq = modules_data["CS3050"]["prerequisites"]
print(real_prereq)
print(evaluate_prereq(real_prereq, {"CS2002", "CS2001"}, all_codes))


real_prereq = modules_data["CS3050"]["prerequisites"]
cleaned = clean_prereq_string(real_prereq, all_codes)
print(cleaned)


