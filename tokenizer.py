def tokenize(text):
    text = text.replace("(", " ( ").replace(")", " ) ")
    tokens = text.split()
    return tokens

result3 = tokenize("BEFORE TAKING THIS MODULE YOU MUST PASS CS2002 AND ( PASS CS2101 OR PASS CS2001 )")
print(result3)

def is_module_code(token):
    if len(token) == 6 and token[:2].isupper() and token[2:6].isdigit():
        return True
    return False


print(is_module_code("CS2002"))  # should be True
print(is_module_code("AND"))     # should be False
print(is_module_code("("))       # should be False

def filter_meaningful_tokens(tokens):
    meaningful_tokens = []
    for token in tokens:
        if is_module_code(token) or token in ["AND", "OR", "(", ")"]:
            meaningful_tokens.append(token)
    return meaningful_tokens

tokens = tokenize("BEFORE TAKING THIS MODULE YOU MUST PASS CS2002 AND ( PASS CS2101 OR PASS CS2001 )")
result = filter_meaningful_tokens(tokens)
print(result)