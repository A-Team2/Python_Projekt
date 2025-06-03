import sys
from enum import Enum
from datetime import datetime, date

# Hilfsfunktionen für Benutzereingaben
# Enum für Ja/Nein Eingaben
class YesOrNo(Enum):
    YES = 1
    NO = 0

# Eigene Ausnahme für leere Eingaben
class EmptyInputError(ValueError):
    def __init__(self, message="Eingabe darf nicht leer sein."):
        super().__init__(message)

# Eigene Ausnahme für Werte außerhalb des zulässigen Bereichs
class OutOfRangeError(ValueError):
    def __init__(self, value, min_value, max_value):
        super().__init__(f"Fehler: Eingabe {value} ist ungültig. Bitte einen Wert zwischen {min_value} und {max_value} eingeben.")
        self.value = value
        self.min_value = min_value
        self.max_value = max_value

# Eigene Ausnahme für ungültige Zeichenkettenlängen
class StringLengthError(ValueError):
    def __init__(self, value, min_length, max_length):
        super().__init__(f"Eingabe zu kurz. Bitte mindestens {min_length} Zeichen eingeben.")
        self.value = value
        self.min_length = min_length
        self.max_length = max_length

# Validiert die Zeichenketteneingabe anhand vorgegebener Längenbeschränkungen
def input_valid_string(prompt: str, min_length: int = 0, max_length: int = sys.maxsize, normalize_func=None) -> str:
    user_input = input(prompt).strip()
    if not (min_length <= len(user_input) <= max_length):
        raise StringLengthError(user_input, min_length, max_length)
    if normalize_func:
        user_input = normalize_func(user_input)
    return user_input

# Validiert die Ganzzahl-Eingabe mit optionalem Standardwert
def input_valid_int(prompt: str, min_value: int = -sys.maxsize, max_value: int = sys.maxsize,
                    default: int = None) -> int:
    user_input = input(prompt).strip()
    if user_input == "":
        if default is None:
            raise EmptyInputError("Eingabe darf nicht leer sein.")
        return default

    try:
        value = int(user_input)
    except ValueError as err:
        raise ValueError("Fehler: Ungültige Eingabe. Bitte eine gültige Zahl eingeben.") from err

    if value < min_value or value > max_value:
        raise OutOfRangeError(value, min_value, max_value)

    return value

# Validiert die Float-Eingabe mit optionalem Standardwert
def input_valid_float(prompt: str,
                      min_value: float = -float('inf'),
                      max_value: float = float('inf'),
                      default: float = None) -> float:
    user_input = input(prompt).strip()
    if user_input == "":
        if default is None:
            raise EmptyInputError("Eingabe darf nicht leer sein.")
        return default

    try:
        value = float(user_input)
    except ValueError as err:
        raise ValueError("Fehler: Ungültige Eingabe. Bitte eine gültige Kommazahl eingeben.") from err

    if value < min_value or value > max_value:
        raise OutOfRangeError(value, min_value, max_value)

    return value

# Verarbeitet Ja-/Nein-Eingaben mit optionalem Standardwert
def input_y_n(prompt: str, default: YesOrNo = None) -> bool:
    y = ['y', 'yes', 'j', 'ja']
    n = ['n', 'no', 'nein']

    user_input = input(prompt).strip().lower()
    if user_input in y:
        return True
    elif user_input in n:
        return False
    elif user_input == "" and default is not None:
        return bool(default.value)
    else:
        raise ValueError("Fehler: Ungültige Eingabe. Bitte 'ja' oder 'nein' eingeben.")

def input_valid_date(prompt: str, min_date: date = None, max_date: date = None, compare_date: date = None, compare_type: str = None) -> date:
    while True:
        user_input = input(prompt).strip()
        try:
            parsed_date = datetime.strptime(user_input, "%Y-%m-%d").date()
            if min_date and parsed_date < min_date:
                print(f"Datum muss nach {min_date} liegen.")
                continue
            if max_date and parsed_date > max_date:
                print(f"Datum muss vor {max_date} liegen.")
                continue
            if compare_date and compare_type:
                if compare_type == 'gt' and not (parsed_date > compare_date):
                    print(f"Datum muss nach {compare_date} liegen.")
                    continue
                if compare_type == 'ge' and not (parsed_date >= compare_date):
                    print(f"Datum muss am oder nach {compare_date} liegen.")
                    continue
                if compare_type == 'lt' and not (parsed_date < compare_date):
                    print(f"Datum muss vor {compare_date} liegen.")
                    continue
                if compare_type == 'le' and not (parsed_date <= compare_date):
                    print(f"Datum muss am oder vor {compare_date} liegen.")
                    continue
            return parsed_date
        except ValueError:
            print("Fehler: Ungültiges Datum. Bitte im Format JJJJ-MM-TT eingeben.")