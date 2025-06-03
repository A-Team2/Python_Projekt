from ui import input_helper
from business_logic.hotel_manager import HotelManager

def run(hotel_manager: HotelManager):
    while True:
        city = None
        cancel = False

        # Eingabeaufforderung wiederholen, bis gültig oder abgebrochen
        while not city and not cancel:
            try:
                city = input_helper.input_valid_string("Stadtname eingeben ('Exit' für Abbruch): ", min_length=2)
                if city.strip().lower() == "exit":
                    print("Abbruch. Zurück zum Hauptmenü.")
                    return
            except input_helper.EmptyInputError:
                print("Fehler: Bitte geben Sie mindestens 2 Zeichen ein oder 'Exit' für Abbruch.")
            except ValueError as err:
                print("Fehler:", err)

        if city:
            hotels = hotel_manager.get_hotels_by_city(city)
            if hotels:
                print(f"\nGefundene Hotels in {city}:")
                for i, hotel in enumerate(hotels, start=1):
                    print(f" {i}. {hotel.name}")
                # Menü zur Hotelauswahl (nur noch Zahl, kein Abbruch)
                auswahl = None
                while auswahl is None:
                    try:
                        auswahl = input_helper.input_valid_int(f"\nNummer eines Hotels auswählen (1-{len(hotels)}): ", min_value=1, max_value=len(hotels))
                    except input_helper.EmptyInputError:
                        print("Fehler: Bitte geben Sie eine Zahl ein.")
                    except ValueError as err:
                        print("Fehler:", err)
                hotel = hotels[auswahl-1]
                print(f"\nDetails zu '{hotel.name}':")
                print(f"Adresse: {hotel.address.get_full_address()}")
                print(f"Sterne: {hotel.stars}")
                # Hier ggf. weitere Details ergänzen (z.B. Zimmer, Ausstattungen)
                return
            else:
                print(f"Keine Hotels in {city} gefunden. Bitte erneut versuchen oder 'Exit' für Abbruch.")
        else:
            print("Keine Stadt eingegeben - Vorgang abgebrochen.")
            return
