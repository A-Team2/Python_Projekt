from __future__ import annotations
from model.address import Address


class Hotel:
    """
    Model Class Hotel
    """

    def __init__(
        self,
        hotel_id: int,
        name: str,
        stars: int,
        address: Address
    ):
        # Ensure values for not nullable attributes or not the right type
        if hotel_id is None or not isinstance(hotel_id, int):
            raise ValueError("hotel_id is required and must be int")
        if not name or not isinstance(name, str):
            raise ValueError("name is required and must be str")
        if stars is None or not isinstance(stars, int):
            raise ValueError("stars is required and must be int")
        if address is None or not isinstance(address, Address):
            raise ValueError("address is required and must be Address")

        # private Attributes
        self.__hotel_id: int    = hotel_id
        self.__name: str        = name
        self.__stars: int       = stars
        self.__address: Address = address

        # Composition:Hotel maintains a list of its rooms.
        self.__rooms: list[Room] = []

    def __repr__(self) -> str:
        return (
            f"Hotel(id={self.__hotel_id!r}, name={self.__name!r}, "
            f"stars={self.__stars!r}, address={self.__address!r})"
        )

    @property
    def hotel_id(self) -> int:
        return self.__hotel_id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        if not name or not isinstance(name, str):
            raise ValueError("name must be an str")
        self.__name = name

    @property
    def stars(self) -> int:
        return self.__stars

    @stars.setter
    def stars(self, stars: int) -> None:
        if stars is None or not isinstance(stars, int):
            raise ValueError("stars must be int")
        self.__stars = stars

    @property
    def address(self) -> Address:
        return self.__address

    @address.setter
    def address(self, address: Address) -> None:
        from model.address import Address
        if address is None or not isinstance(address, Address):
            raise ValueError("address must be an Address instance")
        self.__address = address

    @property
    def rooms(self) -> list[Room]:
        # Return a copy so that the caller cannot modify the private list directly.
        return self.__rooms.copy()

    def add_room(self, room: Room) -> None:
        # Adds a room to the Hotel and sets the back-reference in the Room to this Hotel.
        from model.room import Room
        if not isinstance(room, Room):
            raise ValueError("room must be a Room instance")
        if room not in self.__rooms:
            self.__rooms.append(room)
            room.hotel = self

    def remove_room(self, room: Room) -> None:
        # Removes a room from the Hotel and clears its back-reference.
        from model.room import Room
        if not isinstance(room, Room):
            raise ValueError("room must be a Room instance")
        if room in self.__rooms:
            self.__rooms.remove(room)
            room.hotel = None

    def get_hotel_details(self) -> str:
        # Returns the name, star rating, and address.
        return f"{self.__name} ({self.__stars}★), {self.__address.get_full_address()}"
