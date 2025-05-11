from __future__ import annotations
from datetime import date

class Invoice:
    """
    Model Class Invoice
    """

    def __init__(
        self,
        booking: Booking,
        issue_date: date,
        total_amount: float
    ):
        # Validation
        if booking is None or not hasattr(booking, "booking_id"):
            raise ValueError("invoice must be created with a valid Booking")
        if not isinstance(issue_date, date):
            raise ValueError("issue_date is required and must be date")
        if total_amount is None or not isinstance(total_amount, float):
            raise ValueError("total_amount is required and must be float")

        # private attributes
        self.__booking: Booking   = booking
        self.__issue_date: date   = issue_date
        self.__total_amount: float = total_amount

    def __repr__(self) -> str:
        return (
            f"Invoice(booking_id={self.__booking.booking_id!r}, "
            f"issue_date={self.__issue_date!r}, amount={self.__total_amount!r})"
        )

    @property
    def booking(self) -> Booking:
        # The Booking this Invoice belongs to.
        return self.__booking

    @property
    def issue_date(self) -> date:
        return self.__issue_date

    @issue_date.setter
    def issue_date(self, dt: date) -> None:
        if not isinstance(dt, date):
            raise ValueError("issue_date must be date")
        self.__issue_date = new_issue_date

    @property
    def total_amount(self) -> float:
        return self.__total_amount

    @total_amount.setter
    def total_amount(self, amount: float) -> None:
        if amount is None or not isinstance(amount, float):
            raise ValueError("total_amount must be float")
        self.__total_amount = new_total_amount

    def get_invoice_details(self) -> str:
        # Return a one-line summary of the invoice.
        return (
            f"Invoice for Booking {self.__booking.booking_id}: "
            f"Date {self.__issue_date}, Amount {self.__total_amount:.2f} CHF"
        )