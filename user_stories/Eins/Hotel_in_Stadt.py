from ui import input_helper
from business_logic.hotel_manager import HotelManager

def run(hotel_manager: HotelManager):
    city = None
    cancel = False

    # Eingabeaufforderung wiederholen, bis gültig oder abgebrochen
    while not city and not cancel:
        try:
            city = input_helper.input_valid_string("Stadtname eingeben: ", min_length=2)
        except input_helper.EmptyInputError:
            cancel = True
        except ValueError as err:
            print("Fehler:", err)

    if city:
        hotels = hotel_manager.get_hotels_by_city(city)
        if hotels:
            print(f"\nGefundene Hotels in {city}:")
            for i, hotel in enumerate(hotels, start=1):
                print(f" {i}. {hotel.name}")
            # Menü zur Hotelauswahl
            auswahl = None
            while auswahl is None:
                try:
                    auswahl = input_helper.input_valid_int(f"\nNummer eines Hotels auswählen (1-{len(hotels)}): ", min_value=1, max_value=len(hotels))
                except input_helper.EmptyInputError:
                    print("Abbruch.")
                    return
                except ValueError as err:
                    print("Fehler:", err)
            hotel = hotels[auswahl-1]
            print(f"\nDetails zu '{hotel.name}':")
            print(f"Adresse: {hotel.address.get_full_address()}")
            print(f"Sterne: {hotel.stars}")
            # Hier ggf. weitere Details ergänzen (z.B. Zimmer, Ausstattungen)
        else:
            print(f"Keine Hotels in {city} gefunden.")
    else:
        print("Keine Stadt eingegeben - Vorgang abgebrochen.")
