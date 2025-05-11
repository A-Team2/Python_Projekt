import sys
from enum import Enum

# Enum for Yes/No input
class YesOrNo(Enum):
    YES = 1
    NO = 0

# Custom exception for empty input
class EmptyInputError(ValueError):
    pass

# Custom exception for values outside the allowed range
class OutOfRangeError(ValueError):
    def __init__(self, value, min_value, max_value):
        super().__init__(f"Input {value} is out of range ({min_value} to {max_value}).")
        self.value = value
        self.min_value = min_value
        self.max_value = max_value

# Custom exception for string length violations
class StringLengthError(ValueError):
    def __init__(self, value, min_length, max_length):
        super().__init__(f"Input '{value}' must be between {min_length} and {max_length} characters long.")
        self.value = value
        self.min_length = min_length
        self.max_length = max_length

# Validates string input with length constraints
def input_valid_string(prompt: str, min_length: int = 0, max_length: int = sys.maxsize) -> str:
    user_input = input(prompt).strip()
    if not (min_length <= len(user_input) <= max_length):
        raise StringLengthError(user_input, min_length, max_length)
    return user_input

# Validates integer input with optional default value
def input_valid_int(prompt: str, min_value: int = -sys.maxsize, max_value: int = sys.maxsize,
                    default: int = None) -> int:
    user_input = input(prompt).strip()
    if user_input == "":
        if default is None:
            raise EmptyInputError("Input cannot be empty.")
        return default

    try:
        value = int(user_input)
    except ValueError as err:
        raise ValueError("Invalid input. Please enter a valid number.") from err

    if value < min_value or value > max_value:
        raise OutOfRangeError(value, min_value, max_value)

    return value

# Validates float input with optional default value
def input_valid_float(prompt: str,
                      min_value: float = -float('inf'),
                      max_value: float = float('inf'),
                      default: float = None) -> float:
    user_input = input(prompt).strip()
    if user_input == "":
        if default is None:
            raise EmptyInputError("Input cannot be empty.")
        return default

    try:
        value = float(user_input)
    except ValueError as err:
        raise ValueError("Invalid input. Please enter a valid float number.") from err

    if value < min_value or value > max_value:
        raise OutOfRangeError(value, min_value, max_value)

    return value

# Handles yes/no input with optional default
def input_y_n(prompt: str, default: YesOrNo = None) -> bool:
    y = ['y', 'yes']
    n = ['n', 'no']

    user_input = input(prompt).strip().lower()
    if user_input in y:
        return True
    elif user_input in n:
        return False
    elif user_input == "" and default is not None:
        return bool(default.value)
    else:
        raise ValueError("Invalid input. Please enter 'y' or 'n'.")