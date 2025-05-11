from datetime import date
from model.booking import Booking
from model.invoice import Invoice
from model.guest import Guest
from model.room import Room
from data_access.booking_data_access import BookingDataAccess
from data_access.invoice_data_access import InvoiceDataAccess

class BookingManager:
    def __init__(self):
        self.booking_dao = BookingDataAccess()
        self.invoice_dao = InvoiceDataAccess()

    def cancel_booking(self, booking_id: int) -> bool:
        return self.booking_dao.cancel_booking(booking_id)

    def get_booking_by_id(self, booking_id: int):
        return self.booking_dao.read_booking_by_id(booking_id)

    def create_booking(
        self,
        guest: Guest,
        room: Room,
        check_in: date,
        check_out: date
    ) -> Booking:
        # 1. Verfügbarkeit prüfen
        if not room.is_available(check_in, check_out):
            raise ValueError("Das gewählte Zimmer ist im angegebenen Zeitraum nicht verfügbar.")

        # 2. Preis berechnen
        num_nights = (check_out - check_in).days
        if num_nights <= 0:
            raise ValueError("Ungültiger Zeitraum: Check-out muss nach Check-in liegen.")
        total_amount = float(num_nights * room.price_per_night)

        # 3. Booking-Objekt erzeugen
        booking = Booking(
            booking_id=0,  # Platzhalter – wird durch DB ersetzt
            check_in_date=check_in,
            check_out_date=check_out,
            guest=guest,
            rooms=[room],
            total_amount=total_amount,
            is_cancelled=False
        )
        room.add_booking(booking)  # Verbindung setzen

        # 4. In Datenbank speichern
        booking_id = self.booking_dao.create_booking(booking)
        booking._Booking__booking_id = booking_id  # booking_id setzen (workaround wegen private attr)

        # 5. Rechnung erzeugen
        invoice = Invoice(
            booking=booking,
            issue_date=check_out,
            total_amount=total_amount
        )
        self.invoice_dao.create_invoice(invoice)

        return booking

