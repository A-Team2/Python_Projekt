from ui import input_helper
from business_logic.hotel_manager import HotelManager

def run(hotel_manager: HotelManager):
    city = None
    guest_count = None
    cancel = False

    # 1. Stadt eingeben
    while not city and not cancel:
        try:
            city = input_helper.input_valid_string("Stadtname eingeben: ", min_length=2)
        except input_helper.EmptyInputError:
            cancel = True
        except ValueError as err:
            print(err)

    # 2. Gästeanzahl eingeben
    if not cancel:
        while guest_count is None and not cancel:
            try:
                guest_count = input_helper.input_valid_int("Wie viele Gäste reisen mit (1–10)? ", min_value=1, max_value=10)
            except input_helper.EmptyInputError:
                cancel = True
            except ValueError as err:
                print(err)

    # 3. Hotels anzeigen, die passende Zimmer anbieten
    if city and guest_count is not None:
        hotels = hotel_manager.get_hotels_by_city_and_guests(city, guest_count)

        if hotels:
            print(f"\nHotels in {city} mit Zimmern für mindestens {guest_count} Gast/Gäste:")
            for i, hotel in enumerate(hotels, start=1):
                print(f" {i}. {hotel.name}, {hotel.address.get_full_address()} ({hotel.stars} Sterne)")
        else:
            print(f"Keine passenden Hotels in {city} gefunden.")
    else:
        print("Vorgang abgebrochen.")