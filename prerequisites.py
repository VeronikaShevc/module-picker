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

def tokenize(text):
    # separate brackets from words
    text = text.replace("(", " ( ").replace(")", " ) ")
    # split on whitespace, ignore extra spaces
    tokens = text.split()
    return tokens

def is_module_code(token):
    # 2 letters + 4 digits
    if len(token) == 6 and token[:2].isupper() and token[2:6].isdigit():
        return True
    return False

def filter_meaningful_tokens(tokens, all_codes):
    # filter out filler words, keeping only module codes, AND, OR, and brackets
    meaningful_tokens = []
    for token in tokens:
        cleaned_token = token.strip(".,")
        if token in ["AND", "OR", "(", ")"]:
            meaningful_tokens.append(token)
        elif is_module_code(cleaned_token):
            if cleaned_token not in all_codes:
                # raise an error if the module code is not in the known list
                raise NameError(f"name '{cleaned_token}' is not defined")
            meaningful_tokens.append(cleaned_token)
    return meaningful_tokens

def evaluate_factor(tokens, position, passed_modules):
    # evaluate a single factor, which can be a module code or a parenthesized expression
    if position[0] >= len(tokens):
        raise SyntaxError("Unexpected end of prerequisite text - missing a module code")

    current_token = tokens[position[0]]

    if current_token == "(":
        position[0] += 1  # skip (
        result = evaluate_or(tokens, position, passed_modules)  # recurse into bracket contents
        position[0] += 1  # skip )
        return result
    elif current_token in ["AND", "OR", ")"]:
        # ran into an operator or closing bracket where a module code was expected
        raise SyntaxError(f"Unexpected token '{current_token}' where a module code was expected")
    else:
        position[0] += 1  # skip the code itself
        return current_token in passed_modules

def evaluate_and(tokens, position, passed_modules):
    # evaluate the first factor
    result = evaluate_factor(tokens, position, passed_modules)

    # evaluate the rest of the AND chain
    while position[0] < len(tokens) and tokens[position[0]] == "AND":
        position[0] += 1  # skip "AND"
        next_result = evaluate_factor(tokens, position, passed_modules)
        result = result and next_result

    return result


def evaluate_or(tokens, position, passed_modules):
    result = evaluate_and(tokens, position, passed_modules)  # AND binds tighter, so start there

    while position[0] < len(tokens) and tokens[position[0]] == "OR":
        position[0] += 1  # skip "OR"
        next_result = evaluate_and(tokens, position, passed_modules)
        result = result or next_result

    return result


def evaluate_prereq_tokens(tokens, passed_modules):
    # evaluate the OR chain at the top level
    position = [0]
    return evaluate_or(tokens, position, passed_modules)


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
    """Evaluate whether a prerequisite string is satisfied, given a
    set of passed modules. This is the real parser (tokenize -> filter
    -> recursive evaluate) - no eval() involved anywhere."""
    ug_text, pgt_text = split_ug_pgt(text)
    tokens = tokenize(ug_text)
    meaningful_tokens = filter_meaningful_tokens(tokens, all_codes)
    return evaluate_prereq_tokens(meaningful_tokens, passed_modules)