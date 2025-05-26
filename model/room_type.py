from __future__ import annotations

class RoomType:
    """
    Model Class for RoomType
    """

    def __init__(self, room_type_id: int, description: str, max_guests: int):
        # Validierung
        if room_type_id is None or not isinstance(room_type_id, int):
            raise ValueError("room_type_id is required and must be int")
        if not description or not isinstance(description, str):
            raise ValueError("description is required and must be str")
        if max_guests is None or not isinstance(max_guests, int):
            raise ValueError("max_guests is required and must be int")

        # private Attribute
        self.__room_type_id: int = room_type_id
        self.__description: str  = description
        self.__max_guests: int   = max_guests

        # Bidirektionale Assoziation zu Zimmern.
        self.__rooms: list[Room] = []

    def __repr__(self) -> str:
        return (
            f"RoomType(id={self.__room_type_id!r}, "
            f"description={self.__description!r}, max_guests={self.__max_guests!r})"
        )

    @property
    def room_type_id(self) -> int:
        return self.__room_type_id

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str) -> None:
        if not description or not isinstance(description, str):
            raise ValueError("description must be a non-empty str")
        self.__description = description

    @property
    def max_guests(self) -> int:
        return self.__max_guests

    @max_guests.setter
    def max_guests(self, max_guests: int) -> None:
        if max_guests is None or not isinstance(max_guests, int):
            raise ValueError("max_guests must be int")
        self.__max_guests = max_guests

    @property
    def rooms(self) -> list[Room]:
        # Gibt eine Kopie zurück, um die interne Liste zu schützen.
        return self.__rooms.copy()

    def add_room(self, room: Room) -> None:
        # Fügt diesem Zimmertyp ein Zimmer hinzu und setzt im Zimmer die Rückreferenz auf diesen Zimmertyp.
        from model.room import Room
        if not isinstance(room, Room):
            raise ValueError("room must be a Room instance")
        if room not in self.__rooms:
            self.__rooms.append(room)
            room.room_type = self

    def remove_room(self, room: Room) -> None:
        # Entfernt ein Zimmer aus diesem Zimmertyp und entfernt im Zimmer die Rückreferenz auf diesen Zimmertyp.
        from model.room import Room
        if room in self.__rooms:
            self.__rooms.remove(room)
            room.room_type = None

    def get_room_type_info(self) -> str:
        # Gibt eine kurze Beschreibung dieses Zimmertyps zurück.
        return f"{self.__description}, max guests: {self.__max_guests}"