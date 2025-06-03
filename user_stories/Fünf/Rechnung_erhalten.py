import ui.input_helper as input_helper
from business_logic.guest_manager   import GuestManager
from business_logic.booking_manager import BookingManager
from business_logic.invoice_manager import InvoiceManager
from datetime import date
from ui.validation_helper import is_valid_email

def run(hotel_manager=None):
    gm = GuestManager()
    bm = BookingManager()
    im = InvoiceManager()

    # 1) E-Mail abfragen
    cancel = False
    email = None
    while not email and not cancel:
        try:
            email = input_helper.input_valid_string("E-Mail für Rechnung: ", min_length=5)
            if not is_valid_email(email):
                print("Bitte geben Sie eine gültige E-Mail-Adresse ein!")
                email = None
                continue
        except input_helper.EmptyInputError:
            cancel = True
        except ValueError as err:
            print(err)

    if cancel:
        print("Vorgang abgebrochen.")
        return

    # 2) Gast laden (als echtes Guest-Objekt!)
    guest = gm.read_guest_by_email(email)
    if guest is None:
        print("Unbekannte E-Mail.")
        return

    # 3) Buchungen holen (nur abgeschlossene)
    all_bookings = bm.get_bookings_for_guest(guest)
    completed   = [b for b in all_bookings if b.check_out_date < date.today()]

    if not completed:
        print("Sie haben derzeit keine abgeschlossenen Aufenthalte, die abgerechnet werden können.")
        return

    # 4) Nummerierte Liste anzeigen
    print(f"\nAbgeschlossene Aufenthalte für {guest.first_name} {guest.last_name}:")
    for i, b in enumerate(completed, start=1):
        print(f" {i}. {b.check_in_date} – {b.check_out_date}, Betrag: {b.total_amount:.2f} CHF")

    # 5) Auswahl abfragen
    idx = None
    cancel = False
    while idx is None and not cancel:
        try:
            idx = input_helper.input_valid_int(
                f"Bitte Aufenthalt wählen (1–{len(completed)}): ",
                min_value=1,
                max_value=len(completed)
            )
        except (ValueError, input_helper.EmptyInputError) as err:
            print(err)
            idx = None
    if cancel:
        print("Vorgang abgebrochen.")
        return

    selected_booking = completed[idx-1]
    # 6) Rechnung erzeugen und anzeigen
    invoice = im.generate_invoice(selected_booking)
    print("\nIhre Rechnung:")
    print(invoice.get_invoice_details())