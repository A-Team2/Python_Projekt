from ui import input_helper
from business_logic.hotel_manager import HotelManager

def run(hotel_manager: HotelManager):
    city = None
    min_stars = None
    cancel = False

    # 1. Stadt eingeben
    while not city and not cancel:
        try:
            city = input_helper.input_valid_string("Stadtname eingeben: ", min_length=2)
        except input_helper.EmptyInputError:
            cancel = True
        except ValueError as err:
            print("Fehler:", err)

    # 2. Mindeststerne eingeben
    if not cancel:
        while min_stars is None and not cancel:
            try:
                min_stars = input_helper.input_valid_int("Minimale Anzahl Sterne (1–5): ", min_value=1, max_value=5)
            except input_helper.EmptyInputError:
                cancel = True
            except ValueError as err:
                print("Fehler:", err)

    # 3. Wenn Eingabe gültig: Hotels suchen
    if city and min_stars is not None:
        hotels = hotel_manager.get_hotels_by_city_and_min_stars(city, min_stars)

        if hotels:
            print(f"\nHotels in {city} mit mindestens {min_stars} Stern(en):")
            for i, hotel in enumerate(hotels, start=1):
                print(f" {i}. {hotel.name}, {hotel.address.get_full_address()} ({hotel.stars} Sterne)")
        else:
            print(f"Keine Hotels in {city} mit mindestens {min_stars} Stern(en) gefunden.")
    else:
        print("Vorgang abgebrochen.")