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
                print(f" {i}. {hotel.name}, {hotel.address.get_full_address()} ({hotel.stars} Sterne)")
        else:
            print(f"Keine Hotels in {city} gefunden.")
    else:
        print("Keine Stadt eingegeben - Vorgang abgebrochen.")
