from datetime import date
from ui import input_helper
from business_logic.booking_manager import BookingManager
from data_access.guest_data_access import GuestDataAccess
from data_access.room_data_access import RoomDataAccess

def run():
    print("\n🛏️ Zimmer buchen")

    # 1. Gast-ID eingeben
    guest_id = input_helper.input_valid_int("Geben Sie die Gast-ID ein: ", min_value=1)
    guest_dao = GuestDataAccess()
    guest = guest_dao.read_guest_by_id(guest_id)
    if not guest:
        print("❌ Kein Gast mit dieser ID gefunden.")
        return

    # 2. Zimmer-ID eingeben
    room_id = input_helper.input_valid_int("Geben Sie die Zimmer-ID ein: ", min_value=1)
    room_dao = RoomDataAccess()
    room = room_dao.read_room_by_id(room_id)
    if not room:
        print("❌ Kein Zimmer mit dieser ID gefunden.")
        return

    # 3. Check-in und Check-out Datum
    try:
        check_in = input_helper.input_valid_date("Check-in-Datum (YYYY-MM-DD): ")
        check_out = input_helper.input_valid_date("Check-out-Datum (YYYY-MM-DD): ")
    except ValueError:
        print("❌ Ungültiges Datum.")
        return

    # 4. Buchung durchführen
    try:
        manager = BookingManager()
        booking = manager.create_booking(guest, room, check_in, check_out)
        print("✅ Buchung erfolgreich erstellt!")
        print(booking.get_booking_details())
        print(booking.invoice.get_invoice_details())
    except Exception as err:
        print("❌ Fehler bei der Buchung:", err)
