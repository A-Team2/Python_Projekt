from ui import input_helper
from datetime import datetime

def run(hotel_manager):
    city = None
    check_in = None
    check_out = None
    cancel = False

    # 1. Stadt eingeben
    while not city and not cancel:
        try:
            city = input_helper.input_valid_string("Stadtname eingeben: ", min_length=2, normalize_func=lambda s: s.strip().capitalize())
        except input_helper.EmptyInputError:
            cancel = True
        except ValueError as err:
            print(err)

    # 2. Check-in-Datum
    if not cancel:
        try:
            check_in = input_helper.input_valid_date("Check-in-Datum (YYYY-MM-DD): ")
        except Exception:
            print("Ungültiges Datum.")
            cancel = True

    # 3. Check-out-Datum
    if check_in and not cancel:
        try:
            check_out = input_helper.input_valid_date("Check-out-Datum (YYYY-MM-DD): ", compare_date=check_in, compare_type='gt')
        except Exception:
            print("Ungültiges Datum.")
            cancel = True

    # 4. Suche ausführen
    if city and check_in and check_out:
        hotels = hotel_manager.get_hotels_by_city_and_availability(city, check_in, check_out)

        if hotels:
            print(f"\nHotels in {city} mit freien Zimmern vom {check_in} bis {check_out}:")
            for i, hotel in enumerate(hotels, start=1):
                print(f" {i}. {hotel.name}, {hotel.address.get_full_address()} ({hotel.stars} Sterne)")
        else:
            print("Keine verfügbaren Hotels im gewählten Zeitraum gefunden.")
    else:
        print("Vorgang abgebrochen.")