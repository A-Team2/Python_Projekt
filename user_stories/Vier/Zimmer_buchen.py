from ui import input_helper
from business_logic.guest_manager   import GuestManager
from business_logic.hotel_manager   import HotelManager
from business_logic.booking_manager import BookingManager
from data_access.address_data_access import AddressDataAccess
from model.address import Address
from model.guest import Guest
from datetime import datetime
import re
from ui.validation_helper import is_valid_email

def run(hotel_manager: HotelManager):
    # Manager-Instanzen initialisieren
    gm = GuestManager()
    hm = hotel_manager
    bm = BookingManager()
    address_da = AddressDataAccess()

    # Strasse validieren (mind. ein Leerzeichen und am Ende eine Zahl)
    def valid_street(street):
        return re.match(r"^.+ \d+[a-zA-Z]?$", street)

    # 1) Gast per E-Mail suchen oder neu anlegen
    while True:
        email = input_helper.input_valid_string("Ihre E-Mail: ", min_length=5)
        if not is_valid_email(email):
            print("Bitte geben Sie eine gültige E-Mail-Adresse ein!")
            continue
        break
    guest = gm.read_guest_by_email(email)
    if guest is None:
        print("Neu bei uns? Bitte geben Sie Ihren Namen und Ihre Adresse ein.")
        first = input_helper.input_valid_string("Vorname: ", min_length=1)
        last  = input_helper.input_valid_string("Nachname: ", min_length=1)
        while True:
            street = input_helper.input_valid_string("Straße (mit Hausnummer): ", min_length=2)
            if not valid_street(street):
                print("Bitte geben Sie Straße und Hausnummer an (z.B. 'Musterstrasse 5')!")
                continue
            break
        city = input_helper.input_valid_string("Stadt: ", min_length=2)
        zip_code = input_helper.input_valid_string("PLZ: ", min_length=2)
        # Adresse anlegen und erst dann Address-Objekt mit echter ID erzeugen
        address_id = address_da.create_address(Address(0, street, city, zip_code))
        address = Address(address_id, street, city, zip_code)
        guest = gm.create_guest(first, last, email, address)
        print(f"👍 Gast erfolgreich angelegt: {first} {last} ({email})")
    else:
        print(f"👋 Willkommen zurück, {guest.first_name}!")

    # Stelle sicher, dass guest ein echtes Guest-Objekt ist
    if not isinstance(guest, Guest):
        print("Fehler: Die Gastdaten konnten nicht korrekt geladen werden. Bitte versuchen Sie es erneut.")
        return

    # 2) Stadt abfragen und Hotel auswählen
    while True:
        city = input_helper.input_valid_string("In welcher Stadt möchten Sie ein Hotel buchen? ", min_length=2)
        hotels = hm.get_hotels_by_city(city)
        if not hotels:
            print(f"In {city} sind derzeit keine Hotels verfügbar. Bitte geben Sie eine andere Stadt ein.")
            continue
        print(f"\nHotels in {city}:")
        for i, h in enumerate(hotels, start=1):
            print(f" {i}. {h.name} — {h.address.get_full_address()} ({h.stars} Sterne)")
        idx = input_helper.input_valid_int(
            "Wählen Sie ein Hotel (Nummer): ",
            min_value=1, max_value=len(hotels)
        )
        hotel = hotels[idx-1]
        break

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
    print(f"\n🎉 Buchung erfolgreich!\n" \
          f"Hotel: {hotel.name}\n" \
          f"Zimmer: {room.room_number}\n" \
          f"Zeitraum: {check_in} bis {check_out}\n" \
          f"Gast: {guest.first_name} {guest.last_name} ({guest.email})\n")