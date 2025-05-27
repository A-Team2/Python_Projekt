import ui.input_helper as input_helper
from business_logic.hotel_manager import HotelManager
from business_logic.pricing_manager import PricingManager
from datetime import datetime

def run(hotel_manager: HotelManager):
    # Stadt abfragen
    city = None
    cancel = False
    while not city and not cancel:
        try:
            city = input_helper.input_valid_string("City: ", min_length=2)
        except input_helper.EmptyInputError:
            cancel = True
        except ValueError as err:
            print("Fehler:", err)
    if cancel or not city:
        print("Vorgang abgebrochen.")
        return

    # Hotels in der Stadt holen
    hotels = hotel_manager.get_hotels_by_city(city)
    if not hotels:
        print(f"Keine Hotels in {city} gefunden.")
        return

    # Hotel auswählen
    for i, h in enumerate(hotels, start=1):
        print(f" {i}. {h.name} ({h.stars} Sterne)")
    choice = input_helper.input_valid_int(
        f"Wählen Sie ein Hotel (1–{len(hotels)}): ",
        min_value=1,
        max_value=len(hotels)
    )
    hotel = hotels[choice - 1]

    # Check‐in und Check‐out abfragen
    check_in = None
    while not check_in and not cancel:
        try:
            s = input_helper.input_valid_string("Check-in (YYYY-MM-DD): ", min_length=10)
            check_in = datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError:
            print("Ungültiges Datum.")
        except input_helper.EmptyInputError:
            cancel = True
    if cancel or not check_in:
        print("Vorgang abgebrochen.")
        return

    check_out = None
    while not check_out and not cancel:
        try:
            s = input_helper.input_valid_string("Check-out (YYYY-MM-DD): ", min_length=10)
            check_out = datetime.strptime(s, "%Y-%m-%d").date()
            if check_out <= check_in:
                print("Check-out muss nach Check-in liegen.")
                check_out = None
        except ValueError:
            print("Ungültiges Datum.")
        except input_helper.EmptyInputError:
            cancel = True
    if cancel or not check_out:
        print("Vorgang abgebrochen.")
        return

    # Verfügbare Zimmer holen
    rooms = hotel_manager.get_available_rooms(hotel.hotel_id, check_in, check_out)
    if not rooms:
        print("Keine Zimmer für diesen Zeitraum verfügbar.")
        return

    # Zimmer auswählen
    for i, r in enumerate(rooms, start=1):
        print(f" {i}. Zimmer {r.room_number} – {r.price_per_night:.2f} CHF/Nacht")
    choice = input_helper.input_valid_int(
        f"Wählen Sie ein Zimmer (1–{len(rooms)}): ",
        min_value=1,
        max_value=len(rooms)
    )
    room = rooms[choice - 1]

    # Preis berechnen
    total = PricingManager().calculate_price(
        room.room_id,
        check_in,
        check_out
    )
    nights = (check_out - check_in).days
    print(f"\nGesamtpreis für {nights} Nacht(en) in Zimmer {room.room_number}: {total:.2f} CHF")