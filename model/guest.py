from __future__ import annotations
from model.address import Address

class Guest:
    """
    Model Class for Guest
    """

    def __init__(
        self,
        guest_id: int,
        first_name: str,
        last_name: str,
        email: str,
        address: Address
    ):
        # Validierung
        if guest_id is None or not isinstance(guest_id, int):
            raise ValueError("guest_id is required and must be int")
        if not first_name or not isinstance(first_name, str):
            raise ValueError("first_name is required and must be str")
        if not last_name or not isinstance(last_name, str):
            raise ValueError("last_name is required and must be str")
        if not email or not isinstance(email, str):
            raise ValueError("email is required and must be str")
        if address is None or not isinstance(address, Address):
            raise ValueError("address is required and must be Address")

        # private Attribute
        self.__guest_id: int     = guest_id
        self.__first_name: str   = first_name
        self.__last_name: str    = last_name
        self.__email: str        = email
        self.__address: Address  = address

        # Assoziation: Der Gast führt eine Liste seiner Buchungen (die Buchungen existieren eigenständig weiter).
        self.__bookings: list[Booking] = []

    def __repr__(self) -> str:
        return (
            f"Guest(id={self.__guest_id!r}, "
            f"name={self.__first_name!r} {self.__last_name!r}, "
            f"email={self.__email!r})"
        )

    @property
    def guest_id(self) -> int:
        return self.__guest_id

    @property
    def first_name(self) -> str:
        return self.__first_name

    @first_name.setter
    def first_name(self, name: str) -> None:
        if not name or not isinstance(name, str):
            raise ValueError("first_name must be an str")
        self.__first_name = name

    @property
    def last_name(self) -> str:
        return self.__last_name

    @last_name.setter
    def last_name(self, name: str) -> None:
        if not name or not isinstance(name, str):
            raise ValueError("last_name must be an str")
        self.__last_name = name

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str) -> None:
        if not email or not isinstance(email, str):
            raise ValueError("email must be an str")
        self.__email = email

    @property
    def address(self) -> Address:
        return self.__address

    @property
    def bookings(self) -> list[Booking]:
        # Gibt eine Kopie zurück, um die interne Liste zu schützen.
        return self.__bookings.copy()

    def add_booking(self, booking: Booking) -> None:
        # Verknüpft diesen Gast mit einer Buchung; die Buchungen existieren unabhängig weiter.
        from model.booking import Booking
        if not isinstance(booking, Booking):
            raise ValueError("booking must be a Booking instance")
        if booking not in self.__bookings:
            self.__bookings.append(booking)
            booking.guest = self

    def remove_booking(self, booking: Booking) -> None:
        # Entfernt die Verknüpfung zwischen diesem Gast und einer Buchung.
        # Das Booking-Objekt selbst bleibt weiterhin bestehen.
        from model.booking import Booking
        if booking in self.__bookings:
            self.__bookings.remove(booking)
            booking.guest = None

    def get_guest_info(self) -> str:
        # Gibt den vollständigen Namen und die E-Mail des Gasts zurück.
        return f"{self.__first_name} {self.__last_name} <{self.__email}>"