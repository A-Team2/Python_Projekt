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
    print("5. Zimmer buchen (US 4 + 5)") 
    print("6. Buchung stornieren (US 1.6)")
    print("7. Dynamischen Zimmerpreis berechnen (US 1.7)")

    print("0. Beenden")
    print("================================")

def run_user_story(choice):
    if choice == 1:
        print("\n🏨 Hotel in Stadt anzeigen (US 1.1)")
        from user_stories import Hotel_in_Stadt
        Hotel_in_Stadt.run(hotel_manager)
    elif choice == 2:
        print("\n🏨 Hotels in Stadt mit Mindeststerne anzeigen (US 1.2)")
        from user_stories import Hotel_in_Stadt_Sterne
        Hotel_in_Stadt_Sterne.run(hotel_manager)
    elif choice == 3:
        print("\n🏨 Hotels in Stadt mit Zimmern für Gästeanzahl anzeigen (US 1.3)")
        from user_stories import Hotel_in_Stadt_Zimmer_Gästeanzahl
        Hotel_in_Stadt_Zimmer_Gästeanzahl.run(hotel_manager)
    elif choice == 4:
        print("\n🏨 Hotel in Stadt suchen nach bestimmten Aufenthalt (US 1.4)")
        from user_stories import Hotel_in_Stadt_suchen_Aufenthalt
        Hotel_in_Stadt_suchen_Aufenthalt.run(hotel_manager)
    elif choice == 5:
        print("\n📅 Zimmer buchen (US 4 + 5)")
        from user_stories import zimmer_buchen
        zimmer_buchen.run()
    elif choice == 6:
        print("\n🗑️ Buchung stornieren (US 1.6)")
        from user_stories import booking_stornieren
        booking_stornieren.run()
    elif choice == 7:
       print("\n💰 Dynamischen Zimmerpreis berechnen (US 1.7)")
       from user_stories import dynamische_preise_berechnen
       dynamische_preise_berechnen.run()
    else:
        print("Ungültige Auswahl!")
        
# 4. Hauptprogramm
while True:
    show_menu()
    try:
        choice = input_helper.input_valid_int("Bitte wählen Sie eine Option (0-7): ", min_value=0, max_value=7)
        if choice == 0:
            print("\nProgramm wird beendet. Auf Wiedersehen!")
            break
        run_user_story(choice)
    except input_helper.EmptyInputError:
        print("\nProgramm wird beendet. Auf Wiedersehen!")
        break
    except ValueError as err:
        print("Fehler:", err)
