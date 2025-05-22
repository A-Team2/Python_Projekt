from ui import input_helper
from business_logic.guest_manager   import GuestManager
from business_logic.hotel_manager   import HotelManager
from business_logic.booking_manager import BookingManager
from datetime import datetime

def run(hotel_manager: HotelManager):
    # Manager-Instanzen initialisieren
    gm = GuestManager()
    hm = hotel_manager
    bm = BookingManager()

    # 1) Gast per E-Mail suchen oder neu anlegen
    email = input_helper.input_valid_string("Ihre E-Mail: ", min_length=5)
    guest = gm.read_guest_by_email(email)
    if guest is None:
        print("Neu bei uns? Bitte geben Sie Ihren Namen ein.")
        first = input_helper.input_valid_string("Vorname: ", min_length=1)
        last  = input_helper.input_valid_string("Nachname: ", min_length=1)
        guest = gm.create_guest(first, last, email)
        print(f"👍 Gast angelegt: {guest}")
    else:
        print(f"👋 Willkommen zurück, {guest.first_name}!")

    # 2) Stadt abfragen und Hotel auswählen
    city   = input_helper.input_valid_string("Stadt: ", min_length=2)
    hotels = hm.get_hotels_by_city(city)
    print(f"\nHotels in {city}:")
    for i, h in enumerate(hotels, start=1):
        print(f" {i}. {h.name} — {h.address.get_full_address()} ({h.stars} Sterne)")
    idx   = input_helper.input_valid_int(
        "Wählen Sie ein Hotel (Nummer): ",
        min_value=1, max_value=len(hotels)
    )
    hotel = hotels[idx-1]

    # 3) Zimmer im gewählten Hotel auflisten und auswählen
    rooms = hotel.rooms
    print(f"\nZimmer im Hotel «{hotel.name}»:")
    for i, r in enumerate(rooms, start=1):
        print(f" {i}. Zimmer {r.room_number} — {r.price_per_night:.2f} CHF/Nacht")
    idx  = input_helper.input_valid_int(
        "Wählen Sie ein Zimmer (Nummer): ",
        min_value=1, max_value=len(rooms)
    )
    room = rooms[idx-1]

    # 4) Check-in und Check-out eingeben
    ci_str = input_helper.input_valid_string("Check-in (YYYY-MM-DD): ",  min_length=10, max_length=10)
    co_str = input_helper.input_valid_string("Check-out (YYYY-MM-DD): ", min_length=10, max_length=10)
    check_in  = datetime.strptime(ci_str, "%Y-%m-%d").date()
    check_out = datetime.strptime(co_str, "%Y-%m-%d").date()

    # 6) Buchung anlegen
    booking = bm.create_booking(guest, room, check_in, check_out)
    print(f"\n🎉 Buchung erfolgreich: {booking}")