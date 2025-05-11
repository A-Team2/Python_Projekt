# US6: Buchung stornieren
from ui import input_helper
from business_logic.booking_manager import BookingManager

def run(booking_manager: BookingManager):
    booking_id = None
    cancel = False

    # 1. Buchungs-ID eingeben
    while not booking_id and not cancel:
        try:
            booking_id = input_helper.input_valid_int("Bitte Buchungs-ID eingeben: ", min_value=1)
        except input_helper.EmptyInputError:
            cancel = True
        except ValueError as err:
            print("Fehler:", err)

    # 2. Buchung auslesen und bestätigen
    if booking_id and not cancel:
        booking = booking_manager.get_booking_by_id(booking_id)
        if booking:
            print(f"\nGefundene Buchung: {booking}")
            confirm = input_helper.input_y_n("Möchten Sie diese Buchung stornieren? (y/n): ")
            if confirm:
                success = booking_manager.cancel_booking(booking_id)
                if success:
                    print(f"Buchung mit ID {booking_id} wurde storniert.")
                else:
                    print("Fehler beim Stornieren der Buchung.")
            else:
                print("Stornierung abgebrochen.")
        else:
            print(f"Keine Buchung mit ID {booking_id} gefunden.")
    else:
        print("Vorgang abgebrochen.")
