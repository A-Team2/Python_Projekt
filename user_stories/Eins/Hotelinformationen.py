from ui import input_helper

def run(hotel_manager):
    city = None
    cancel = False

    # Stadtname eingeben
    while not city and not cancel:
        try:
            city = input_helper.input_valid_string("Stadtname eingeben: ", min_length=2)
        except input_helper.EmptyInputError:
            cancel = True
        except ValueError as err:
            print("Fehler:", err)

    # Hotels anzeigen
    if city:
        hotels = hotel_manager.get_hotels_by_city(city)

        if hotels:
            print(f"\nHotels in {city}:")
            for i, hotel in enumerate(hotels, start=1):
                print(f" {i}. {hotel.name}, {hotel.address.get_full_address()} ({hotel.stars} Sterne)")
        else:
            print("Keine Hotels in dieser Stadt gefunden.")
    else:
        print("Vorgang abgebrochen.")