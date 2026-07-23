import json

with open("modules.json", "r") as f:
    modules_data = json.load(f)

all_codes = modules_data.keys()

def find_codes_in_string(text, all_known_codes):
    """Return every known module code that appears somewhere 
    in the given text."""
    found = []
    for each_code in all_known_codes:
        if each_code in text: found.append(each_code)
    return found

def split_ug_pgt(text):
    """Split a prerequisite string into its undergraduate and 
    postgraduate parts, if both exist."""
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
    """Replace every module code in the text with True or False, 
    depending on whether it's been passed."""
    mentioned = find_codes_in_string(text, all_codes)
    for code in mentioned:
        if code in passed_modules:
            text = text.replace(code, "True")
        else:
            text = text.replace(code, "False")
    return text


def clean_prereq_string(text, all_codes):
    """Strip out filler English words, 
    keeping only module codes, AND, OR, and brackets."""
    words = text.replace("(", " ( ").replace(")", " ) ").split()
    keep = []
    for word in words:
        if word in all_codes or word in ["AND", "OR", "(", ")"]:
            keep.append(word)
    return " ".join(keep)

def get_necessary_missing(text, passed_modules, all_codes):
    """Return only the missing module codes 
    that would actually change the result if passed, 
    ignoring codes already covered by a satisfied OR clause."""
    mentioned = find_codes_in_string(text, all_codes)
    necessary = []
    for code in mentioned:
        if code in passed_modules:
            continue
        trial = set(passed_modules) | {code}
        if evaluate_prereq(text, trial, all_codes):
            necessary.append(code)
    return necessary

def evaluate_prereq(text, passed_modules, all_codes):
    """Evaluate whether a prerequisite string is satisfied, given a set of passed modules."""
    ug_text, pgt_text = split_ug_pgt(text)
    cleaned = clean_prereq_string(ug_text, all_codes)
    substituted = substitute_booleans(cleaned, passed_modules, all_codes)
    substituted = substituted.replace("AND", "and").replace("OR", "or")
    result = eval(substituted)
    return result