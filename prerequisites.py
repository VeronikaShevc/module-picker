import json

with open("modules.json", "r") as f:
    modules_data = json.load(f)

all_codes = modules_data.keys()

def find_codes_in_string(text, all_know_codes):
    found = []
    for code in all_know_codes:
        if code in text: found.append(code)
    return found

def split_ug_pgt(text):
    if "PGT:" in text:
        ug_text = text.split("PGT:")[0]
        pgt_text = text.split("PGT:")[1]
        return ug_text, pgt_text
    elif "POSTGRADUATE" in text:
        ug_text = text.split("POSTGRADUATE")[0]
        pgt_text = text.split("POSTGRADUATE")[1]
        return ug_text, pgt_text
    else:
        return text, None


def substitute_booleans(text, passed_modules, all_codes):
    for code in all_codes:
        if code in passed_modules:
            text = text.replace(code, "True")
        else:
            text = text.replace(code, "False")
    return text


def clean_prereq_string(text, all_codes):
    words = text.replace("(", " ( ").replace(")", " ) ").split()
    keep = []
    for word in words:
        if word in all_codes or word in ["AND", "OR", "(", ")"]:
            keep.append(word)
    return " ".join(keep)

def evaluate_prereq(text, passed_modules, all_codes):
    ug_text, pgt_text = split_ug_pgt(text)
    
    cleaned = clean_prereq_string(ug_text, all_codes)
    substituted = substitute_booleans(cleaned, passed_modules, all_codes)
    substituted = substituted.replace("AND", "and").replace("OR", "or")
    result = eval(substituted)
    return result