from __future__ import annotations
from datetime import date
from model.hotel import Hotel
from model.room_type import RoomType
from model.facilities import Facilities
from model.booking import Booking

class Room:
    """
    Model Class Room
    """

    def __init__(
        self,
        room_id: int,
        room_number: int,
        price_per_night: float,
        hotel: Hotel,
        room_type: RoomType
    ):
        # Validation
        if room_id is None or not isinstance(room_id, int):
            raise ValueError("room_id is required and must be int")
        if room_number is None or not isinstance(room_number, int):
            raise ValueError("room_number is required and must be int")
        if price_per_night is None or not isinstance(price_per_night, float):
            raise ValueError("price_per_night is required and must be float")
        if hotel is None or not isinstance(hotel, Hotel):
            raise ValueError("hotel is required and must be Hotel")
        if room_type is None or not isinstance(room_type, RoomType):
            raise ValueError("room_type is required and must be RoomType")

        # private Attributes
        self.__room_id: int = room_id
        self.__room_number: int = room_number
        self.__price_per_night: float = price_per_night
        self.__hotel: Hotel = hotel
        self.__room_type: RoomType = room_type

        # Registers the room with the hotel and establishes the hotel's reference in the room (bidirectional association).
        self.__hotel.add_room(self)

        # Initialize associations to Facilities and Bookings.
        self.__facilities: list[Facilities] = []
        self.__bookings: list[Booking] = []

    def __repr__(self) -> str:
        return (
            f"Room(id={self.__room_id!r}, number={self.__room_number!r}, "
            f"price={self.__price_per_night!r}, hotel={self.__hotel!r})"
        )

    @property
    def room_id(self) -> int:
        return self.__room_id

    @property
    def room_number(self) -> int:
        return self.__room_number

    @room_number.setter
    def room_number(self, room_number: int) -> None:
        if room_number is None or not isinstance(room_number, int):
            raise ValueError("room_number must be int")
        self.__room_number = room_number

    @property
    def price_per_night(self) -> float:
        return self.__price_per_night

    @price_per_night.setter
    def price_per_night(self, price: float) -> None:
        if price is None or not isinstance(price, float):
            raise ValueError("price_per_night must be float")
        self.__price_per_night = price

    @property
    def hotel(self) -> Hotel:
        return self.__hotel

    @property
    def room_type(self) -> RoomType:
        return self.__room_type

    @property
    def facilities(self) -> list[Facilities]:
        # Return a copy to protect the internal list.
        return self.__facilities.copy()

    def add_facility(self, facility: Facilities) -> None:
        if not isinstance(facility, Facilities):
            raise ValueError("facility must be a Facilities instance")
        if facility not in self.__facilities:
            self.__facilities.append(facility)

    def remove_facility(self, facility: Facilities) -> None:
        if facility in self.__facilities:
            self.__facilities.remove(facility)

    @property
    def bookings(self) -> list[Booking]:
        return self.__bookings.copy()

    def add_booking(self, booking: Booking) -> None:
        if not isinstance(booking, Booking):
            raise ValueError("booking must be a Booking instance")
        if booking not in self.__bookings:
            self.__bookings.append(booking)

    def remove_booking(self, booking: Booking) -> None:
        if booking in self.__bookings:
            self.__bookings.remove(booking)

    def get_room_details(self) -> str:
        # Returns a short description of the room.
        return f"Zimmer {self.__room_number}, Preis: {self.__price_per_night:.2f} CHF/Nacht"

    def is_available(self, check_in: date, check_out: date) -> bool:
        """
        Prüft, ob das Zimmer im angegebenen Zeitraum verfügbar ist.
        
        Args:
            check_in: Anreisedatum
            check_out: Abreisedatum
            
        Returns:
            bool: True wenn das Zimmer verfügbar ist, False wenn nicht
        """
        if not isinstance(check_in, date) or not isinstance(check_out, date):
            raise ValueError("check_in und check_out müssen vom Typ date sein")
        if check_in >= check_out:
            raise ValueError("check_in muss vor check_out liegen")
            
        # Prüfe alle Buchungen des Zimmers
        for booking in self.__bookings:
            # Wenn sich die Zeiträume überschneiden, ist das Zimmer nicht verfügbar
            if (check_in <= booking.check_out_date and check_out >= booking.check_in_date):
                return False
        return True