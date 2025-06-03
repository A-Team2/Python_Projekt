from ui import input_helper
from business_logic.hotel_manager import HotelManager
from datetime import datetime

def run(hotel_manager: HotelManager):
    # 1) Stadt abfragen und Hotel auswählen
    while True:
        try:
            city = input_helper.input_valid_string("In welcher Stadt möchten Sie ein Hotel suchen? ", min_length=3)
        except input_helper.StringLengthError as err:
            print(f"Fehler: {err}")
            continue
        hotels = hotel_manager.get_hotels_by_city(city)
        if not hotels:
            print(f"In {city} sind derzeit keine Hotels verfügbar. Bitte geben Sie eine andere Stadt ein.")
            continue
        print(f"\nHotels in {city}:")
        for i, h in enumerate(hotels, start=1):
            print(f" {i}. {h.name} — {h.address.get_full_address()} ({h.stars} Sterne)")
        idx = None
        while idx is None:
            try:
                idx = input_helper.input_valid_int(
                    "Wählen Sie ein Hotel (Nummer): ",
                    min_value=1, max_value=len(hotels)
                )
            except input_helper.EmptyInputError:
                print("Fehler: Bitte geben Sie eine Zahl ein.")
            except ValueError as err:
                print(err)
        hotel = hotels[idx-1]
        break

    # 2) Zeitraum abfragen
    while True:
        try:
            ci_str = input_helper.input_valid_string("Check-in (YYYY-MM-DD): ",  min_length=10, max_length=10)
            co_str = input_helper.input_valid_string("Check-out (YYYY-MM-DD): ", min_length=10, max_length=10)
            check_in  = datetime.strptime(ci_str, "%Y-%m-%d").date()
            check_out = datetime.strptime(co_str, "%Y-%m-%d").date()
            if check_out <= check_in:
                print("Check-out muss nach Check-in liegen.")
                continue
            break
        except ValueError:
            print("Fehler: Bitte geben Sie die Daten im Format JJJJ-MM-TT ein.")

    # 3) Verfügbare Zimmer filtern
    available_rooms = [room for room in hotel.rooms if room.is_available(check_in, check_out)]
    if not available_rooms:
        print("Für den gewählten Zeitraum sind keine Zimmer verfügbar.")
        return

    print(f"\nVerfügbare Zimmer im Hotel «{hotel.name}» von {check_in} bis {check_out}:")
    for i, room in enumerate(available_rooms, start=1):
        rt = room.room_type
        facilities = ", ".join([f.facility_name for f in getattr(room, 'facilities', [])])
        print(f" {i}. Typ: {rt.description} | Max. Gäste: {rt.max_guests} | Beschreibung: {rt.description} | Preis: {room.price_per_night:.2f} CHF/Nacht | Ausstattung: {facilities}")
