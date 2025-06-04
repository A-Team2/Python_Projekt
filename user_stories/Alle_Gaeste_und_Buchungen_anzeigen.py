from business_logic.guest_manager import GuestManager
from business_logic.booking_manager import BookingManager

def run():
    gm = GuestManager()
    bm = BookingManager()
    guests = gm.read_all_guests()
    if not guests:
        print("Keine Gäste gefunden.")
        return
    print("Alle Gäste und deren Buchungen:")
    for guest in guests:
        print(f"- {guest.first_name} {guest.last_name} ({guest.email})")
        print(f"  Adresse: {guest.address.street}, {guest.address.zip_code} {guest.address.city}")
        bookings = bm.get_bookings_for_guest(guest)
        if not bookings:
            print("  Keine Buchungen.")
        else:
            for b in bookings:
                status = "Storniert" if getattr(b, 'is_cancelled', False) else "Aktiv"
                if hasattr(b, 'rooms') and b.rooms:
                    for room in b.rooms:
                        print(f"  Buchung: Hotel {room.hotel.name}, Zimmer {room.room_number}, {b.check_in_date} bis {b.check_out_date} [Status: {status}]")
                else:
                    print(f"  Buchung: (keine Zimmerdaten geladen), {b.check_in_date} bis {b.check_out_date} [Status: {status}]")
        print() 