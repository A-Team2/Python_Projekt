from ui import input_helper

def run(hotel_manager):
    city = None
    min_stars = None
    guest_count = None
    check_in = None
    check_out = None
    cancel = False

    # Stadtname eingeben
    while not city and not cancel:
        try:
            city = input_helper.input_valid_string("Stadtname: ", min_length=2, normalize_func=lambda s: s.strip().capitalize())
        except input_helper.EmptyInputError:
            cancel = True
        except ValueError as err:
            print(err)

    # Sternefilter
    if not cancel:
        while min_stars is None and not cancel:
            try:
                min_stars = input_helper.input_valid_int("Minimale Sterne (1-5): ", min_value=1, max_value=5)
            except input_helper.EmptyInputError:
                cancel = True
            except ValueError as err:
                print(err)

    # Gästeanzahl
    if not cancel:
        while guest_count is None and not cancel:
            try:
                guest_count = input_helper.input_valid_int("Wie viele Gäste (1-10)? ", min_value=1, max_value=10)
            except input_helper.EmptyInputError:
                cancel = True
            except ValueError as err:
                print(err)

    # Check-in-Datum
    if not cancel:
        try:
            check_in = input_helper.input_valid_date("Check-in (YYYY-MM-DD): ")
        except input_helper.EmptyInputError:
            cancel = True
        except ValueError:
            print("Ungültiges Datum.")

    # Check-out-Datum
    if check_in and not cancel:
        try:
            check_out = input_helper.input_valid_date("Check-out (YYYY-MM-DD): ", compare_date=check_in, compare_type='gt')
        except input_helper.EmptyInputError:
            cancel = True
        except ValueError:
            print("Ungültiges Datum oder Check-out liegt nicht nach Check-in.")

    # Suche starten
    if city and min_stars is not None and guest_count is not None and check_in and check_out:
        hotels = hotel_manager.get_hotels_by_all_criteria(city, min_stars, guest_count, check_in, check_out)

        if hotels:
            print(f"\nHotels in {city} mit mindestens {min_stars} Stern(en), Zimmern für {guest_count} Person(en) und verfügbar vom {check_in} bis {check_out}:")
            for i, hotel in enumerate(hotels, start=1):
                print(f" {i}. {hotel.name}, {hotel.address.get_full_address()} ({hotel.stars} Sterne)")
        else:
            print("Keine passenden Hotels gefunden.")
    else:
        print("Vorgang abgebrochen.")