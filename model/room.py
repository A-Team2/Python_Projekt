from __future__ import annotations

class Room:
    """
    Model Class Room
    """

    def __init__(
        self,
        room_id: int,
        room_no: int,
        price_per_night: float,
        hotel: Hotel,
        room_type: RoomType
    ):
        # Validation
        if room_id is None or not isinstance(room_id, int):
            raise ValueError("room_id is required and must be int")
        if room_no is None or not isinstance(room_no, int):
            raise ValueError("room_no is required and must be int")
        if price_per_night is None or not isinstance(price_per_night, float):
            raise ValueError("price_per_night is required and must be float")
        if hotel is None or not isinstance(hotel, Hotel):
            raise ValueError("hotel is required and must be Hotel")
        if room_type is None or not isinstance(room_type, RoomType):
            raise ValueError("room_type is required and must be RoomType")

        # private Attributes
        self.__room_id: int = room_id
        self.__room_no: int = room_no
        self.__price_per_night: float = price_per_night
        self.__hotel: Hotel = hotel
        self.__room_type: RoomType = room_type

        # Registers the room with the hotel and establishes the hotel’s reference in the room (bidirectional association).
        self.__hotel.add_room(self)

        # Initialize associations to Facilities and Bookings.
        self.__facilities: list[Facilities] = []
        self.__bookings: list[Booking] = []

    def __repr__(self) -> str:
        return (
            f"Room(id={self.__room_id!r}, no={self.__room_no!r}, "
            f"price={self.__price_per_night!r}, hotel={self.__hotel!r})"
        )

    @property
    def room_id(self) -> int:
        return self.__room_id

    @property
    def room_no(self) -> int:
        return self.__room_no

    @room_no.setter
    def room_no(self, room_no: int) -> None:
        if room_no is None or not isinstance(room_no, int):
            raise ValueError("room_no must be int")
        self.__room_no = room_no

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

    @hotel.setter
    def hotel(self, hotel: Hotel) -> None:
        from model.hotel import Hotel
        if hotel is None or not isinstance(hotel, Hotel):
            raise ValueError("hotel must be a Hotel instance")
        # Remove old relation.
        if self.__hotel is not hotel:
            self.__hotel.remove_room(self)
            self.__hotel = hotel
            hotel.add_room(self)

    @property
    def room_type(self) -> RoomType:
        return self.__room_type

    @room_type.setter
    def room_type(self, room_type: RoomType) -> None:
        from model.room_type import RoomType
        if room_type is None or not isinstance(room_type, RoomType):
            raise ValueError("room_type must be a RoomType instance")
        self.__room_type = room_type

    @property
    def facilities(self) -> list[Facilities]:
        # Return a copy to protect the internal list.
        return self.__facilities.copy()

    def add_facility(self, facility: Facilities) -> None:
        from model.facilities import Facilities
        if not isinstance(facility, Facilities):
            raise ValueError("facility must be a Facilities instance")
        if facility not in self.__facilities:
            self.__facilities.append(facility)

    def remove_facility(self, facility: Facilities) -> None:
        from model.facilities import Facilities
        if facility in self.__facilities:
            self.__facilities.remove(facility)

    @property
    def bookings(self) -> list[Booking]:
        return self.__bookings.copy()

    def add_booking(self, booking: Booking) -> None:
        from model.booking import Booking
        if not isinstance(booking, Booking):
            raise ValueError("booking must be a Booking instance")
        if booking not in self.__bookings:
            self.__bookings.append(booking)

    def remove_booking(self, booking: Booking) -> None:
        from model.booking import Booking
        if booking in self.__bookings:
            self.__bookings.remove(booking)

    def get_room_details(self) -> str:
        # Returns a short description of the room.
        return f"Zimmer {self.__room_no}, Preis: {self.__price_per_night:.2f} CHF/Nacht"