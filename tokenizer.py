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

def filter_meaningful_tokens(tokens):
    # filter out filler words, keeping only module codes, AND, OR, and brackets
    meaningful_tokens = []
    for token in tokens:
        if is_module_code(token) or token in ["AND", "OR", "(", ")"]:  # keep only real logic
            meaningful_tokens.append(token)
    return meaningful_tokens


def evaluate_factor(tokens, position, passed_modules):
    current_token = tokens[position[0]]

    if current_token == "(":
        # skip (
        position[0] += 1
        # recurse into bracket contents
        result = evaluate_or(tokens, position, passed_modules)
        # skip )
        position[0] += 1
        return result
    else:
        # skip the code itself
        position[0] += 1
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


if __name__ == "__main__":
    raw = "BEFORE TAKING THIS MODULE YOU MUST PASS CS2002 AND ( PASS CS2101 OR PASS CS2001 )"
    tokens = filter_meaningful_tokens(tokenize(raw))
    print(tokens)

    print(evaluate_prereq_tokens(tokens, {"CS2002", "CS2101"}))  # True
    print(evaluate_prereq_tokens(tokens, {"CS2002"}))              # False
    print(evaluate_prereq_tokens(tokens, {"CS2002", "CS2001"}))  # True