class Invoice:
    def __init__(self, invoice_id: int, issue_date: str, total_amount: float, booking_id: int):
        self._invoice_id = invoice_id
        self._issue_date = issue_date
        self._total_amount = total_amount
        self._booking_id = booking_id

    def invoice_id(self) -> int:
        return self._invoice_id

    def issue_date(self) -> str:
        return self._issue_date

    def issue_date_set(self, date: str) -> None:
        self._issue_date = date

    def total_amount(self) -> float:
        return self._total_amount

    def total_amount_set(self, amount: float) -> None:
        self._total_amount = amount

    def booking_id(self) -> int:
        return self._booking_id

    def booking_id_set(self, booking_id: int) -> None:
        self._booking_id = booking_id

    def __repr__(self):
        return f"Invoice(id={self._invoice_id}, amount={self._total_amount})"
