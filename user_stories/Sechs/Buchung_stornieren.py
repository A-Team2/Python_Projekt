from ui import input_helper
from business_logic.guest_manager import GuestManager
from business_logic.booking_manager import BookingManager
from business_logic.invoice_manager import InvoiceManager
from ui.validation_helper import is_valid_email
from datetime import date

def run():
    gm = GuestManager()
    bm = BookingManager()
    im = InvoiceManager()

    # 1) E-Mail abfragen
    email = None
    cancel = False
    while not email and not cancel:
        try:
            email = input_helper.input_valid_string("E-Mail zum Identifizieren: ", min_length=5)
            if not is_valid_email(email):
                print("Bitte geben Sie eine gültige E-Mail-Adresse ein!")
                email = None
                continue
        except input_helper.EmptyInputError:
            cancel = True
        except ValueError as err:
            print(err)
    if cancel or not email:
        print("Abgebrochen.")
        return

    # 2) Gast laden
    try:
        guest = gm.read_guest_by_email(email)
    except ValueError as err:
        print("Fehler:", err)
        return

    if not guest:
        print("Unbekannte E-Mail.")
        return

    # 3) Alle offenen Buchungen holen
    bookings = bm.get_bookings_for_guest(guest)
    open_bookings = [b for b in bookings if not b.is_cancelled and b.check_out_date > date.today()]
    if not open_bookings:
        print("Keine aktiven Buchungen zum Stornieren.")
        return

    # 4) Liste anzeigen
    print("Ihre aktiven Buchungen:")
    for i, b in enumerate(open_bookings, start=1):
        if b.rooms and len(b.rooms) > 0:
            print(f" {i}. Hotel {b.rooms[0].hotel.name}, {b.check_in_date} – {b.check_out_date}")
        else:
            print(f" {i}. (Zimmerdaten nicht geladen), {b.check_in_date} – {b.check_out_date}")

    # 5) Auswahl treffen
    choice = None
    while choice is None:
        try:
            choice = input_helper.input_valid_int(
                f"Bitte Buchung wählen (1–{len(open_bookings)}): ",
                min_value=1,
                max_value=len(open_bookings)
            )
        except (ValueError, input_helper.EmptyInputError) as err:
            print(err)
    to_cancel = open_bookings[choice - 1]

    # 6) Stornieren und Rechnung erzeugen
    bm.cancel_booking(to_cancel.booking_id)
    invoice = im.generate_invoice(to_cancel)
    print(f"Buchung {to_cancel.booking_id} storniert. Stornorechnung #{invoice.invoice_id} erstellt.")