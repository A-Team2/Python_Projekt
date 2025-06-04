# run.py
import os
import shutil

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

def show_menu():
    print("\n=== Hotel Reservierungssystem ===")
    print("1. Hotel in Stadt anzeigen (US 1.1)")
    print("2. Hotels in Stadt mit Mindeststerne anzeigen (US 1.2)")
    print("3. Hotels in Stadt mit Zimmern für Gästeanzahl anzeigen (US 1.3)")
    print("4. Hotel in Stadt suchen Aufenthalt (US 1.4)")
    print("5. Wünsche kombinieren (US 1.5)")
    print("6. Hotelinformationen anzeigen (US 1.6)")
    print("7. Zimmertypen eines Hotels anzeigen (US 2.1)")
    print("8. Verfügbare Zimmer nach Zeitraum anzeigen (US 2.2)")
    print("9. Hotel hinzufügen (US 3.1)")
    print("10. Hotel entfernen (US 3.2)")
    print("11. Hotel aktualisieren (US 3.3)")
    print("12. Zimmer buchen (US 4)")
    print("13. Rechnung nach Aufenthalt erstellen (US 5)")
    print("14. Buchung stornieren (US 6)")
    print("15. Dynamischen Zimmerpreis berechnen (US 7)")
    print("16. Alle Buchungen anzeigen (US 8)")
    print("17. Zimmer mit Ausstattung anzeigen (US 9)")
    print("18. Stammdaten verwalten (US 10)")
    print("19. Alle Hotels anzeigen")
    print("20. Alle Gäste und Buchungen anzeigen")
    print("0. Beenden")
    print("================================")

def run_user_story(choice):
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
        print("\n🏨 Hotel hinzufügen (US 3.1)")
        from user_stories.Drei.Hotel_hinzufügen import run
        run(hotel_manager)
    elif choice == 10:
        print("\n🏨 Hotel entfernen (US 3.2)")
        from user_stories.Drei.Hotel_entfernen import run
        run(hotel_manager)
    elif choice == 11:
        print("\n🏨 Hotel aktualisieren (US 3.3)")
        from user_stories.Drei.Hotel_aktualisieren import run
        run(hotel_manager)
    elif choice == 12:
        print("\n🏨 Zimmer buchen (US 4)")
        from user_stories.Vier.Zimmer_buchen import run
        run(hotel_manager)
    elif choice == 13:
        print("\n🧾 Rechnung nach Aufenthalt erstellen (US 5)")
        from user_stories.Fünf.Rechnung_erhalten import run
        run(hotel_manager)
    elif choice == 14:
        print("\n🗑️ Buchung stornieren (US 6)")
        from user_stories.Sechs.Buchung_stornieren import run
        run()
    elif choice == 15:
        print("\n💰 Dynamischen Zimmerpreis berechnen (US 7)")
        from user_stories.Sieben.dynamische_Preise import run
        run(hotel_manager)
    elif choice == 16:
        print("\n🔎 Alle Buchungen anzeigen (US 8)")
        from user_stories.Acht.Alle_Buchungen import run
        run(hotel_manager)
    elif choice == 17:
        print("\n🏨 Zimmer mit Ausstattung anzeigen (US 9)")
        from user_stories.Neun.Zimmer_mit_Ausstatung import run
        run(hotel_manager)
    elif choice == 18:
        print("\n⚙️ Stammdaten verwalten (US 10)")
        from user_stories.Zehn.Stammdaten_verwalten import run
        run(hotel_manager)
    elif choice == 19:
        print("\n🏨 Alle Hotels anzeigen")
        from user_stories.Alle_Hotels_anzeigen import run
        run(hotel_manager)
    elif choice == 20:
        print("\n👤 Alle Gäste und Buchungen anzeigen")
        from user_stories.Alle_Gaeste_und_Buchungen_anzeigen import run
        run()
    else:
        print("Ungültige Auswahl!")
        
# 4. Hauptprogramm
while True:
    show_menu()
    try:
        choice = input_helper.input_valid_int("Bitte wählen Sie eine Option (0-20): ", min_value=0, max_value=20)
        if choice == 0:
            print("\nProgramm wird beendet. Auf Wiedersehen!")
            break
        run_user_story(choice)
    except input_helper.EmptyInputError:
        print("\nProgramm wird beendet. Auf Wiedersehen!")
        break
    except ValueError as err:
        print("Fehler:", err)
