import json

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

def has_ug_pgt_split(text):
    student = ""
    if "UG:" in text or "UNDERGRADUATE" in text:
        student += "UG"
        print("UG")
    if "PGT:" in text or "POSTGRADUATE" in text:
        student += "PGT"
        print("PGT")
    return student

# plain_string = "BEFORE TAKING THIS MODULE YOU MUST PASS CS1002"
# print(has_ug_pgt_split(plain_string))

# split_string = "UNDERGRADUATE - BEFORE TAKING THIS MODULE YOU MUST PASS CS2002 AND (PASS CS2001 OR PASS CS2101). PGT: CS5001 OR CS5002"
# print(has_ug_pgt_split(split_string))


def split_ug_pgt(text):
    if "UG:" in text or "UNDERGRADUATE" in text:
        ug_text = text.split("PGT:")[0]
        pgt_text = text.split("PGT:")[1]
        return ug_text, pgt_text
    else:
        return text, None
    
split_string = "UNDERGRADUATE - BEFORE TAKING THIS MODULE YOU MUST PASS CS2002 AND (PASS CS2001 OR PASS CS2101). PGT: CS5001 OR CS5002"
print(split_ug_pgt(split_string))

plain_string = "BEFORE TAKING THIS MODULE YOU MUST PASS CS1002"
print(split_ug_pgt(plain_string))