from ui import input_helper
from business_logic.guest_manager   import GuestManager
from business_logic.hotel_manager   import HotelManager
from business_logic.booking_manager import BookingManager
from data_access.address_data_access import AddressDataAccess
from model.address import Address
from model.guest import Guest
from datetime import datetime
import re
from ui.validation_helper import is_valid_email, valid_street

def run(hotel_manager: HotelManager):
    # Manager-Instanzen initialisieren
    gm = GuestManager()
    hm = hotel_manager
    bm = BookingManager()
    address_da = AddressDataAccess()

    def calculate_total_price(room, check_in, check_out):
        nights = (check_out - check_in).days
        return room.price_per_night * nights

    def show_booking_summary(hotel, room, guest, check_in, check_out, total_price):
        print("\n=== Buchungsübersicht ===")
        print(f"Hotel: {hotel.name}")
        print(f"Zimmer: {room.room_number}")
        print(f"Check-in: {check_in}")
        print(f"Check-out: {check_out}")
        print(f"Gast: {guest.first_name} {guest.last_name}")
        print(f"E-Mail: {guest.email}")
        print(f"Gesamtpreis: {total_price:.2f} CHF")
        print("========================")

    # 1) Gast per E-Mail suchen oder neu anlegen
    while True:
        try:
            email = input_helper.input_valid_string("Ihre E-Mail: ", min_length=5)
            if not is_valid_email(email):
                print("Bitte geben Sie eine gültige E-Mail-Adresse ein!")
                continue
            break
        except Exception as err:
            print(f"Fehler: {err}")

    guest = gm.read_guest_by_email(email)
    if guest is None:
        print("Neu bei uns? Bitte geben Sie Ihren Namen und Ihre Adresse ein.")
        # Vorname
        while True:
            try:
                first = input_helper.input_valid_string("Vorname: ", min_length=2)
                break
            except Exception as err:
                print(f"Fehler: {err}")

        # Nachname
        while True:
            try:
                last = input_helper.input_valid_string("Nachname: ", min_length=2)
                break
            except Exception as err:
                print(f"Fehler: {err}")

        # Straße (mit Hausnummer)
        while True:
            try:
                street = input_helper.input_valid_string("Straße (mit Hausnummer): ", min_length=2)
                if not valid_street(street):
                    print("Bitte geben Sie Straße und Hausnummer an (z.B. 'Musterstrasse 5')!")
                    continue
                break
            except Exception as err:
                print(f"Fehler: {err}")

        # Stadt
        while True:
            try:
                city = input_helper.input_valid_string("Stadt: ", min_length=2)
                if len(city) < 2:
                    print("Die Stadt muss mindestens 2 Zeichen lang sein.")
                    continue
                break
            except Exception as err:
                print(f"Fehler: {err}")

        # PLZ
        while True:
            try:
                zip_code = input_helper.input_valid_string("PLZ: ", min_length=2)
                break
            except Exception as err:
                print(f"Fehler: {err}")

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

    while True:
        # 2) Stadt abfragen und Hotel auswählen
        while True:
            city = input_helper.input_valid_string("In welcher Stadt möchten Sie ein Hotel buchen? ", min_length=2)
            if len(city) < 2:
                print("Die Stadt muss mindestens 2 Zeichen lang sein.")
                continue
            hotels = hm.get_hotels_by_city(city)
            if not hotels:
                print(f"In {city} sind derzeit keine Hotels verfügbar. Bitte geben Sie eine andere Stadt ein.")
                continue
            print(f"\nHotels in {city}:")
            for i, h in enumerate(hotels, start=1):
                print(f" {i}. {h.name} — {h.address.get_full_address()} ({h.stars} Sterne)")
            try:
                idx = input_helper.input_valid_int(
                    "Wählen Sie ein Hotel (Nummer): ",
                    min_value=1, max_value=len(hotels)
                )
                hotel = hotels[idx-1]
                break
            except (ValueError, input_helper.EmptyInputError) as err:
                print(f"Fehler: {err}")
                continue

        # 3) Zimmer im gewählten Hotel auflisten und auswählen
        rooms = hotel.rooms
        print(f"\nZimmer im Hotel «{hotel.name}»:")
        for i, r in enumerate(rooms, start=1):
            print(f" {i}. Zimmer {r.room_number} — {r.price_per_night:.2f} CHF/Nacht — für max. {r.room_type.max_guests} Personen")
        try:
            idx = input_helper.input_valid_int(
                "Wählen Sie ein Zimmer (Nummer): ",
                min_value=1, max_value=len(rooms)
            )
            room = rooms[idx-1]
        except (ValueError, input_helper.EmptyInputError) as err:
            print(f"Fehler: {err}")
            continue

        # 4) Check-in und Check-out eingeben
        while True:
            try:
                ci_str = input_helper.input_valid_string("Check-in (YYYY-MM-DD): ", min_length=10, max_length=10)
                co_str = input_helper.input_valid_string("Check-out (YYYY-MM-DD): ", min_length=10, max_length=10)
                check_in = datetime.strptime(ci_str, "%Y-%m-%d").date()
                check_out = datetime.strptime(co_str, "%Y-%m-%d").date()
                
                if check_in >= check_out:
                    print("Check-out muss nach dem Check-in liegen!")
                    continue
                if check_in < datetime.now().date():
                    print("Check-in kann nicht in der Vergangenheit liegen!")
                    continue
                break
            except ValueError:
                print("Bitte geben Sie das Datum im Format YYYY-MM-DD ein!")
                continue

        # 5) Preis berechnen und Buchung bestätigen
        total_price = calculate_total_price(room, check_in, check_out)
        show_booking_summary(hotel, room, guest, check_in, check_out, total_price)

        while True:
            confirm = input_helper.input_valid_string(
                "Möchten Sie diese Buchung bestätigen? (ja/nein): ",
                min_length=2
            ).strip().lower()
            if confirm in ("ja", "nein"):
                break
            print("Bitte geben Sie 'ja' oder 'nein' ein.")

        if confirm == "ja":
            # 6) Buchung anlegen
            booking = bm.create_booking(guest, room, check_in, check_out)
            print(f"\n Buchung erfolgreich!")
            break
        else:
            while True:
                again = input_helper.input_valid_string(
                    "Möchten Sie eine andere Buchung vornehmen? (ja/nein): ",
                    min_length=2
                ).strip().lower()
                if again in ("ja", "nein"):
                    break
                print("Bitte geben Sie 'ja' oder 'nein' ein.")
            
            if again == "nein":
                print("Buchung abgebrochen. Auf Wiedersehen!")
                break