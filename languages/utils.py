import re


CODE_re = re.compile(r'^[a-z]{3}$')

def code_is_valid(code):
    return CODE_re.match(code)
