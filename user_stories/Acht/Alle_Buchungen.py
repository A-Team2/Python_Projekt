from ui import input_helper
from business_logic.booking_manager import BookingManager

def run(hotel_manager):
    bm = BookingManager()
    bookings = bm.get_all_bookings()
    if not bookings:
        print("Keine Buchungen gefunden.")
        return

    print("\n=== Alle Buchungen ===")
    for i, b in enumerate(bookings, start=1):
        status = "storniert" if b.is_cancelled else "aktiv"
        print(f"{i}. ID {b.booking_id}: {b.guest.first_name} {b.guest.last_name}, "
              f"{b.check_in_date} bis {b.check_out_date}, {b.total_amount:.2f} CHF, {status}")