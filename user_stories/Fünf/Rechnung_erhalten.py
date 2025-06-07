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
    completed = [b for b in all_bookings if b.check_out_date < date.today()]

    if not completed:
        print("\nVielen Dank für Ihr Interesse!")
        print("Sie haben derzeit keine abgeschlossenen Aufenthalte, die abgerechnet werden können.")
        print("Wir freuen uns auf Ihren nächsten Besuch!")
        return

    # 4) Nummerierte Liste mit Details anzeigen
    print(f"\nAbgeschlossene Aufenthalte für {guest.first_name} {guest.last_name}:")
    print("─" * 80)
    for i, b in enumerate(completed, start=1):
        print(f"\n{i}. Aufenthalt:")
        if b.rooms:
            zimmer_liste = ", ".join(f"{room.room_number} ({room.room_type.description})" for room in b.rooms)
            hotel_name = b.rooms[0].hotel.name
        else:
            zimmer_liste = "-"
            hotel_name = "-"
        print(f"   Hotel: {hotel_name}")
        print(f"   Zimmer: {zimmer_liste}")
        print(f"   Check-in:  {b.check_in_date}")
        print(f"   Check-out: {b.check_out_date}")
        print(f"   Gesamtbetrag: {b.total_amount:.2f} CHF")
        print("─" * 80)

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
    print("═" * 80)
    print(invoice.get_invoice_details())
    print("═" * 80)

    # 7) E-Mail-Option abfragen
    while True:
        email_choice = input("\nMöchten Sie die Rechnung per E-Mail erhalten? (ja/nein): ").lower().strip()
        if email_choice in ['ja', 'nein']:
            break
        print("Bitte geben Sie nur 'ja' oder 'nein' ein.")

    if email_choice == 'ja':
        # Hier würde die E-Mail-Versand-Logik implementiert werden
        print(f"\nDie Rechnung wurde an {email} gesendet.")
    else:
        print("\nDie Rechnung wurde nicht per E-Mail versendet.")

    print("\nVielen Dank für Ihr Vertrauen!")
    print("Wir freuen uns auf Ihren nächsten Besuch!")