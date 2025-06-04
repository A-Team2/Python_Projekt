import re

def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def is_valid_name(name: str, min_length: int = 2) -> bool:
    return isinstance(name, str) and len(name.strip()) >= min_length

def valid_street(street: str) -> bool:
    return re.match(r"^.+ \d+[a-zA-Z]?$", street) is not None

