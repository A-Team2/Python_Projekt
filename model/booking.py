class Booking:
    def __init__(self, booking_id: int, check_in_date: str, check_out_date: str, is_cancelled: bool,
                 total_amount: float, guest_id: int, room_id: int):
        self._booking_id = booking_id
        self._check_in_date = check_in_date
        self._check_out_date = check_out_date
        self._is_cancelled = is_cancelled
        self._total_amount = total_amount
        self._guest_id = guest_id
        self._room_id = room_id

    def booking_id(self) -> int:
        return self._booking_id

    def check_in_date(self) -> str:
        return self._check_in_date

    def check_in_date_set(self, date: str) -> None:
        self._check_in_date = date

    def check_out_date(self) -> str:
        return self._check_out_date

    def check_out_date_set(self, date: str) -> None:
        self._check_out_date = date

    def is_cancelled(self) -> bool:
        return self._is_cancelled

    def is_cancelled_set(self, cancelled: bool) -> None:
        self._is_cancelled = cancelled

    def total_amount(self) -> float:
        return self._total_amount

    def total_amount_set(self, amount: float) -> None:
        self._total_amount = amount

    def guest_id(self) -> int:
        return self._guest_id

    def guest_id_set(self, guest_id: int) -> None:
        self._guest_id = guest_id

    def room_id(self) -> int:
        return self._room_id

    def room_id_set(self, room_id: int) -> None:
        self._room_id = room_id

    def __repr__(self):
        return f"Booking(id={self._booking_id}, guest_id={self._guest_id}, room_id={self._room_id})"
