from model.invoice import Invoice
from data_access.invoice_data_access import InvoiceDataAccess
from datetime import date

class InvoiceManager:
    def __init__(self):
        self.__invoice_da = InvoiceDataAccess()

    def generate_invoice(self, booking) -> Invoice:
        # Eingaben prüfen
        from model.booking import Booking
        if booking is None or not isinstance(booking, Booking):
            raise ValueError("booking is required and must be Booking")

        # Rechnungsbetrag bestimmen
        # Falls Booking.calculate_total_price() existiert, nutze es,
        # sonst direkt booking.total_amount
        total = (
            booking.calculate_total_price()
            if hasattr(booking, "calculate_total_price")
            else booking.total_amount
        )
        # Heutiges Datum als Ausgabe-Datum
        issue_date = date.today()

        # Datensatz anlegen und neue Invoice-ID holen
        new_id = self.__invoice_da.insert_invoice(
            booking.booking_id,
            issue_date,
            total
        )

        # Frisch aus DB laden und zurückgeben
        invoice = self.__invoice_da.read_invoice_by_id(new_id)
        if invoice is None:
            raise RuntimeError(f"Failed to load invoice #{new_id}")
        return invoice