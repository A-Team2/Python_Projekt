from data_access.base_data_access import BaseDataAccess
from model.invoice import Invoice

class InvoiceDataAccess(BaseDataAccess):
    def create_invoice(self, invoice: Invoice) -> int:
        sql = """
        INSERT INTO invoice (booking_id, issue_date, total_amount)
        VALUES (?, ?, ?)
        """
        params = (invoice.booking_id, invoice.issue_date, invoice.total_amount)
        last_id, _ = self.execute(sql, params)
        return last_id

    def read_invoice_by_booking_id(self, booking_id: int) -> Invoice | None:
        sql = """
        SELECT invoice_id, booking_id, issue_date, total_amount
        FROM invoice
        WHERE booking_id = ?
        """
        row = self.fetchone(sql, (booking_id,))
        if row:
            return Invoice(*row)
        return None
    
    def insert_invoice(
        self,
        booking_id: int,
        issue_date,          # datetime.date
        total_amount: float
    ) -> int:
        # 1) Legt einen neuen Invoice-Datensatz an
        sql = """
        INSERT INTO invoice (issue_date, total_amount, booking_booking_id)
        VALUES (?, ?, ?)
        """
        params = (issue_date.isoformat(), total_amount, booking_id)
        last_id, _ = self.execute(sql, params)
        return last_id

