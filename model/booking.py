from __future__ import annotations
from datetime import date
from model.guest import Guest
from model.invoice import Invoice


class Booking:
    """
    Model Class for Booking
    """

    def __init__(
        self,
        booking_id: int,
        check_in_date: date,
        check_out_date: date,
        guest: Guest,
        rooms: list['Room'],
        total_amount: float = 0.0,
        is_cancelled: bool = False
    ):
        # Validierung
        if booking_id is None or not isinstance(booking_id, int):
            raise ValueError("booking_id is required and must be int")
        if not isinstance(check_in_date, date):
            raise ValueError("check_in_date is required and must be date")
        if not isinstance(check_out_date, date):
            raise ValueError("check_out_date is required and must be date")
        if guest is None or not isinstance(guest, Guest):
            raise ValueError("guest is required and must be Guest")
        from model.room import Room
        if not isinstance(rooms, list) or any(not isinstance(r, Room) for r in rooms):
            raise ValueError("rooms is required and must be list of Room")
        if total_amount is None or not isinstance(total_amount, float):
            raise ValueError("total_amount is required and must be float")
        if not isinstance(is_cancelled, bool):
            raise ValueError("is_cancelled must be boolean")

        # private Attribute
        self.__booking_id     = booking_id
        self.__check_in_date  = check_in_date
        self.__check_out_date = check_out_date
        self.__is_cancelled   = is_cancelled
        self.__total_amount   = total_amount

        # Assoziation: beim Gast registrieren.
        self.__guest = guest
        guest.add_booking(self)

        # Assoziation: Rooms managen
        self.__rooms: list['Room'] = []
        for room in rooms:
            self.add_room(room)

        
    def __repr__(self) -> str:
        return (
            f"Booking(id={self.__booking_id!r}, guest={self.__guest!r}, "
            f"{self.__check_in_date!r}-{self.__check_out_date!r}, "
            f"cancelled={self.__is_cancelled!r}, amount={self.__total_amount!r})"
        )

    @property
    def booking_id(self) -> int:
        return self.__booking_id

    @property
    def check_in_date(self) -> date:
        return self.__check_in_date

    @property
    def check_out_date(self) -> date:
        return self.__check_out_date

    @property
    def is_cancelled(self) -> bool:
        return self.__is_cancelled

    @is_cancelled.setter
    def is_cancelled(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError("is_cancelled muss ein bool sein")
        self.__is_cancelled = value

    def cancel(self) -> None:
        # Markiert diese Buchung als storniert und entfernt die zugehörige Rechnung.
        self.__is_cancelled = True
        # Setzt die Rechnungsreferenz auf NULL.
        self.__invoice = None

    @property
    def total_amount(self) -> float:
        return self.__total_amount

    @total_amount.setter
    def total_amount(self, amount: float) -> None:
        if amount is None or not isinstance(amount, float):
            raise ValueError("total_amount must be float")
        self.__total_amount = amount

    @property
    def guest(self) -> Guest:
        return self.__guest
   
    @guest.setter
    def guest(self, guest: Guest) -> None:
        if guest is None or not isinstance(guest, Guest):
             raise ValueError("guest must be a Guest instance or None")
        self.__guest = guest

    @property
    def rooms(self) -> list['Room']:
        # Gibt eine Kopie zurück, um die interne Liste zu schützen.
        return self.__rooms.copy()

    def add_room(self, room: 'Room') -> None:
        from model.room import Room
        if not isinstance(room, Room):
            raise ValueError("room must be a Room instance")
        if room not in self.__rooms:
            self.__rooms.append(room)

    def remove_room(self, room: 'Room') -> None:
        from model.room import Room
        if room in self.__rooms:
            self.__rooms.remove(room)

    

    def get_booking_details(self) -> str:
        # Gibt eine kurze Zusammenfassung dieser Buchung zurück.
        status = "cancelled" if self.__is_cancelled else "active"
        return (
            f"Booking {self.__booking_id}: Guest {self.__guest}, "
            f"{self.__check_in_date}-{self.__check_out_date} ({status}), "
            f"Total {self.__total_amount:.2f} CHF"
        )