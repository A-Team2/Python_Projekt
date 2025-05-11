from ui import input_helper
from business_logic.booking_manager import BookingManager

def run(booking_manager: BookingManager):
    print("=== Buchung stornieren (User Story 6) ===")

    booking_id = None
    cancel = False

    # 1. Buchungs-ID eingeben
    while not booking_id and not cancel:
        try:
            booking_id = input_helper.input_valid_int("Buchungs-ID eingeben: ", min_value=1)
        except input_helper.EmptyInputError:
            cancel = True
        except ValueError as err:
            print("Fehler:", err)

    # 2. Buchung laden
    if booking_id and not cancel:
        booking = booking_manager.get_booking_by_id(booking_id)
        if booking is None:
            print(f"Keine Buchung mit ID {booking_id} gefunden.")
            return

        print(f"\nBuchung gefunden für Gast-ID {booking.guest_id} mit Check-In {booking.check_in_date}.")

        # 3. Stornierung bestätigen
        yes_no = input_helper.input_y_n("Buchung wirklich stornieren (y/n)? ", default=input_helper.YesOrNo.NO)

        if yes_no == input_helper.YesOrNo.YES:
            success = booking_manager.cancel_booking(booking_id)
            if success:
                print(f"Buchung mit ID {booking_id} wurde erfolgreich storniert.")
            else:
                print("Stornierung fehlgeschlagen.")
        else:
            print("Stornierung abgebrochen.")
    else:
        print("Vorgang abgebrochen.")
