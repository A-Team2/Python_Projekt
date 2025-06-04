# run.py
import os
import shutil
import time

# 1. Umgebung vorbereiten
source = "database/hotel_reservation_sample.db"
db_file = "database/working_hotel.db"
shutil.copyfile(source, db_file)  # immer mit frischer Kopie starten
os.environ["DB_FILE"] = db_file   # Pfad für BaseDataAccess

# 2. Module importieren
import model
import data_access
import business_logic
import ui.input_helper as input_helper

# 3. Manager initialisieren
from business_logic.hotel_manager import HotelManager

hotel_manager = HotelManager()

# andere Manager bei Bedarf...

# ANSI-Farbcodes
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
BOLD = '\033[1m'
RESET = '\033[0m'

HOTEL_ASCII = [
    f"{YELLOW}        ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄        {RESET}",
    f"{YELLOW}       ████████████████       {RESET}",
    f"{YELLOW}      ███  {CYAN}HOTEL{YELLOW}  ███      {RESET}",
    f"{YELLOW}     ██████████████████     {RESET}",
    f"{YELLOW}    ██  █  █  █  █  ██    {RESET}",
    f"{YELLOW}   ████████████████████   {RESET}",
    f"{YELLOW}  ██  █  █  █  █  █  ██  {RESET}",
    f"{YELLOW} ██████████████████████ {RESET}",
    f"{YELLOW}██  █  █  █  █  █  █  ██{RESET}",
    f"{YELLOW}████████████████████████{RESET}",
    f"{BLUE}   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   {RESET}",
    f"{GREEN}   ░░░░░░░░░░░░░░░░░   {RESET}"
]

SAD_FACE = [
    f"{RED}      .-''''-.      {RESET}",
    f"{RED}    .'        '.    {RESET}",
    f"{RED}   /   O    O   \   {RESET}",
    f"{RED}  :             |  {RESET}",
    f"{RED}  |   .------.  |  {RESET}",
    f"{RED}  :  |      |  :  {RESET}",
    f"{RED}   \  '----'  /   {RESET}",
    f"{RED}    '.____.'    {RESET}"
]

def animated_hotel():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{CYAN}{'═'*40}")
    print(f"{CYAN}   🏨 {BOLD}HOTEL RESERVIERUNGSSYSTEM{RESET}{CYAN}")
    print(f"{'═'*40}{RESET}")
    print(f"{YELLOW}Das Hotel wird aufgebaut ...{RESET}\n")
    hotel_lines = []
    for line in reversed(HOTEL_ASCII):
        hotel_lines.insert(0, line)
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"\n{CYAN}{'═'*40}")
        print(f"{CYAN}   🏨 {BOLD}HOTEL RESERVIERUNGSSYSTEM{RESET}{CYAN}")
        print(f"{'═'*40}{RESET}")
        print(f"{YELLOW}Das Hotel wird aufgebaut ...{RESET}\n")
        for l in hotel_lines:
            print(l)
        time.sleep(0.25)
    time.sleep(0.7)
    print(f"\n{GREEN}{BOLD}Fertig! Willkommen!{RESET}")
    time.sleep(1.2)
    os.system('clear' if os.name == 'posix' else 'cls')

def animated_welcome():
    print(f"\n{CYAN}{'═'*40}")
    print(f"{CYAN}   🏨 {BOLD}HOTEL RESERVIERUNGSSYSTEM{RESET}{CYAN}")
    print(f"{'═'*40}{RESET}")
    print(f"{YELLOW}Willkommen! Das System wird geladen", end='', flush=True)
    for _ in range(5):
        print('.', end='', flush=True)
        time.sleep(0.3)
    print(f"{RESET}\n")

def show_main_menu():
    print(f"\n{CYAN}{'═'*40}")
    print(f"{CYAN}   🏨 {BOLD}HOTEL RESERVIERUNGSSYSTEM{RESET}{CYAN}")
    print(f"{'═'*40}{RESET}")
    print(f"{YELLOW}1.{RESET}  Gast-User Stories")
    print(f"{YELLOW}2.{RESET}  Admin-User Stories")
    print(f"{YELLOW}3.{RESET}  KontrolleMolle (Test-Stories)")
    print(f"{YELLOW}0.{RESET}  Beenden")
    print(f"{CYAN}{'═'*40}{RESET}")

def show_guest_menu():
    print(f"\n{GREEN}{'─'*36}")
    print(f"{GREEN} {BOLD}GAST-USER STORIES{RESET}{GREEN}")
    print(f"{'─'*36}{RESET}")
    print(f"{YELLOW}1.{RESET} Hotel in Stadt anzeigen (US 1.1)")
    print(f"{YELLOW}2.{RESET} Hotels in Stadt mit Mindeststerne anzeigen (US 1.2)")
    print(f"{YELLOW}3.{RESET} Hotels in Stadt mit Zimmern für Gästeanzahl anzeigen (US 1.3)")
    print(f"{YELLOW}4.{RESET} Hotel in Stadt suchen Aufenthalt (US 1.4)")
    print(f"{YELLOW}5.{RESET} Wünsche kombinieren (US 1.5)")
    print(f"{YELLOW}6.{RESET} Hotelinformationen anzeigen (US 1.6)")
    print(f"{YELLOW}7.{RESET} Zimmertypen eines Hotels anzeigen (US 2.1)")
    print(f"{YELLOW}8.{RESET} Verfügbare Zimmer nach Zeitraum anzeigen (US 2.2)")
    print(f"{YELLOW}9.{RESET} Zimmer buchen (US 4)")
    print(f"{YELLOW}10.{RESET} Rechnung nach Aufenthalt erstellen (US 5)")
    print(f"{YELLOW}11.{RESET} Buchung stornieren (US 6)")
    print(f"{YELLOW}12.{RESET} Dynamischen Zimmerpreis berechnen (US 7)")
    print(f"{YELLOW}0.{RESET} Zurück zum Hauptmenü")
    print(f"{GREEN}{'─'*36}{RESET}")

def show_admin_menu():
    print(f"\n{MAGENTA}{'═'*36}")
    print(f"{MAGENTA} {BOLD}ADMIN-USER STORIES{RESET}{MAGENTA}")
    print(f"{'═'*36}{RESET}")
    print(f"{YELLOW}1.{RESET} Hotel hinzufügen (US 3.1)")
    print(f"{YELLOW}2.{RESET} Hotel entfernen (US 3.2)")
    print(f"{YELLOW}3.{RESET} Hotel aktualisieren (US 3.3)")
    print(f"{YELLOW}4.{RESET} Alle Buchungen anzeigen (US 8)")
    print(f"{YELLOW}5.{RESET} Zimmer mit Ausstattung anzeigen (US 9)")
    print(f"{YELLOW}6.{RESET} Stammdaten verwalten (US 10)")
    print(f"{YELLOW}0.{RESET} Zurück zum Hauptmenü")
    print(f"{MAGENTA}{'═'*36}{RESET}")

def show_kontrolle_menu():
    print(f"\n{BLUE}{'─'*44}")
    print(f"{BLUE} {BOLD}KONTROLLEMOLLE (TEST-STORIES){RESET}{BLUE}")
    print(f"{'─'*44}{RESET}")
    print(f"{YELLOW}1.{RESET} Alle Hotels anzeigen")
    print(f"{YELLOW}2.{RESET} Alle Gäste und Buchungen anzeigen")
    print(f"{YELLOW}3.{RESET} Zimmer zu Hotel hinzufügen")
    print(f"{YELLOW}0.{RESET} Zurück zum Hauptmenü")
    print(f"{BLUE}{'─'*44}{RESET}")

def run_guest_story(choice):
    if choice == 1:
        print("\n🏨 Hotel in Stadt anzeigen (US 1.1)")
        from user_stories.Eins.Hotel_in_Stadt import run
        run(hotel_manager)
    elif choice == 2:
        print("\n🏨 Hotels in Stadt mit Mindeststerne anzeigen (US 1.2)")
        from user_stories.Eins.Hotel_in_Stadt_Sterne import run
        run(hotel_manager)
    elif choice == 3:
        print("\n🏨 Hotels in Stadt mit Zimmern für Gästeanzahl anzeigen (US 1.3)")
        from user_stories.Eins.Hotel_in_Stadt_Zimmer_Gästeanzahl import run
        run(hotel_manager)
    elif choice == 4:
        print("\n🏨 Hotel in Stadt suchen nach bestimmten Aufenthalt (US 1.4)")
        from user_stories.Eins.Hotel_in_Stadt_suchen_Aufenthalt import run
        run(hotel_manager)
    elif choice == 5:
        print("\n🏨 Wünsche kombinieren (US 1.5)")
        from user_stories.Eins.Wünsche_kombiniert import run
        run(hotel_manager)
    elif choice == 6:
        print("\n🏨 Hotelinformationen anzeigen (US 1.6)")
        from user_stories.Eins.Hotelinformationen import run
        run(hotel_manager)
    elif choice == 7:
        print("\n🏨 Zimmertypen eines Hotels anzeigen (US 2.1)")
        from user_stories.Zwei.Zimmerypen_Hotel import run
        run(hotel_manager)
    elif choice == 8:
        print("\n🏨 Verfügbare Zimmer nach Zeitraum anzeigen (US 2.2)")
        from user_stories.Zwei.Zimmer_sehen import run
        run(hotel_manager)
    elif choice == 9:
        print("\n🏨 Zimmer buchen (US 4)")
        from user_stories.Vier.Zimmer_buchen import run
        run(hotel_manager)
    elif choice == 10:
        print("\n🧾 Rechnung nach Aufenthalt erstellen (US 5)")
        from user_stories.Fünf.Rechnung_erhalten import run
        run(hotel_manager)
    elif choice == 11:
        print("\n🗑️ Buchung stornieren (US 6)")
        from user_stories.Sechs.Buchung_stornieren import run
        run()
    elif choice == 12:
        print("\n💰 Dynamischen Zimmerpreis berechnen (US 7)")
        from user_stories.Sieben.dynamische_Preise import run
        run(hotel_manager)
    else:
        print("Ungültige Auswahl!")

def run_admin_story(choice):
    if choice == 1:
        print("\n🏨 Hotel hinzufügen (US 3.1)")
        from user_stories.Drei.Hotel_hinzufügen import run
        run(hotel_manager)
    elif choice == 2:
        print("\n🏨 Hotel entfernen (US 3.2)")
        from user_stories.Drei.Hotel_entfernen import run
        run(hotel_manager)
    elif choice == 3:
        print("\n🏨 Hotel aktualisieren (US 3.3)")
        from user_stories.Drei.Hotel_aktualisieren import run
        run(hotel_manager)
    elif choice == 4:
        print("\n🔎 Alle Buchungen anzeigen (US 8)")
        from user_stories.Acht.Alle_Buchungen import run
        run(hotel_manager)
    elif choice == 5:
        print("\n🏨 Zimmer mit Ausstattung anzeigen (US 9)")
        from user_stories.Neun.Zimmer_mit_Ausstatung import run
        run(hotel_manager)
    elif choice == 6:
        print("\n⚙️ Stammdaten verwalten (US 10)")
        from user_stories.Zehn.Stammdaten_verwalten import run
        run(hotel_manager)
    else:
        print("Ungültige Auswahl!")

def run_kontrolle_story(choice):
    if choice == 1:
        print("\n🏨 Alle Hotels anzeigen (KontrolleMolle)")
        from user_stories.Alle_Hotels_anzeigen import run
        run(hotel_manager)
    elif choice == 2:
        print("\n👤 Alle Gäste und Buchungen anzeigen (KontrolleMolle)")
        from user_stories.Alle_Gaeste_und_Buchungen_anzeigen import run
        run()
    elif choice == 3:
        print("\n➕ Zimmer zu Hotel hinzufügen (KontrolleMolle)")
        from user_stories.Hotel_Zimmer_hinzufuegen import run
        run(hotel_manager)
    else:
        print("Ungültige Auswahl!")

def sad_password_animation():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{RED}{'═'*40}")
    print(f"{RED}{BOLD}Falsches Passwort!{RESET}{RED}")
    print(f"{'═'*40}{RESET}")
    print(f"{RED}Admin-Zugang verweigert!{RESET}\n")
    face_lines = []
    for line in SAD_FACE:
        face_lines.append(line)
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"\n{RED}{'═'*40}")
        print(f"{RED}{BOLD}Falsches Passwort!{RESET}{RED}")
        print(f"{'═'*40}{RESET}")
        print(f"{RED}Admin-Zugang verweigert!{RESET}\n")
        for l in face_lines:
            print(l)
        time.sleep(0.18)
    print(f"\n{RED}Bitte versuche es erneut...{RESET}")
    time.sleep(1.5)
    os.system('clear' if os.name == 'posix' else 'cls')

def animated_goodbye():
    import sys
    import time
    os.system('clear' if os.name == 'posix' else 'cls')
    msg = f"{GREEN}{BOLD}Auf Wiedersehen! {RESET}"
    print("\n")
    for c in msg:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.08)
    print("\n")
    time.sleep(1.2)

# Hauptprogramm
if __name__ == "__main__":
    animated_hotel()
    while True:
        show_main_menu()
        try:
            main_choice = input_helper.input_valid_int("Bitte wählen Sie einen Bereich (0-3): ", min_value=0, max_value=3)
            if main_choice == 0:
                animated_goodbye()
                break
            elif main_choice == 1:
                # Gast-User Stories
                while True:
                    show_guest_menu()
                    try:
                        guest_choice = input_helper.input_valid_int("Bitte wählen Sie eine Option (0-12): ", min_value=0, max_value=12)
                        if guest_choice == 0:
                            break
                        run_guest_story(guest_choice)
                    except Exception as err:
                        print(f"{RED}Fehler: {err}{RESET}")
            elif main_choice == 2:
                # Admin-User Stories (mit Passwort)
                pw = input("Bitte Admin-Passwort eingeben: ")
                if pw != "1234":
                    sad_password_animation()
                    continue
                while True:
                    show_admin_menu()
                    try:
                        admin_choice = input_helper.input_valid_int("Bitte wählen Sie eine Option (0-6): ", min_value=0, max_value=6)
                        if admin_choice == 0:
                            break
                        run_admin_story(admin_choice)
                    except Exception as err:
                        print(f"{RED}Fehler: {err}{RESET}")
            elif main_choice == 3:
                # KontrolleMolle
                while True:
                    show_kontrolle_menu()
                    try:
                        kontrolle_choice = input_helper.input_valid_int("Bitte wählen Sie eine Option (0-3): ", min_value=0, max_value=3)
                        if kontrolle_choice == 0:
                            break
                        run_kontrolle_story(kontrolle_choice)
                    except Exception as err:
                        print(f"{RED}Fehler: {err}{RESET}")
        except input_helper.EmptyInputError:
            animated_goodbye()
            break
        except ValueError as err:
            print(f"{RED}Fehler: {err}{RESET}")
