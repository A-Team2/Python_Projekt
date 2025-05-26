from __future__ import annotations

class Facilities:
    """
    Model Class for Facilities
    """

    def __init__(self, facility_id: int, facility_name: str):
        # Validierung
        if facility_id is None or not isinstance(facility_id, int):
            raise ValueError("facility_id is required and must be int")
        if not facility_name or not isinstance(facility_name, str):
            raise ValueError("facility_name is required and must be str")

        # private Attribute
        self.__facility_id: int    = facility_id
        self.__facility_name: str  = facility_name

        # Bidirektionale Assoziation zu Zimmern.
        self.__rooms: list[Room] = []

    def __repr__(self) -> str:
        return (
            f"Facilities(id={self.__facility_id!r}, "
            f"name={self.__facility_name!r})"
        )

    @property
    def facility_id(self) -> int:
        return self.__facility_id

    @property
    def facility_name(self) -> str:
        return self.__facility_name

    @facility_name.setter
    def facility_name(self, facility_name: str) -> None:
        if not facility_name or not isinstance(facility_name, str):
            raise ValueError("facility_name must be a non-empty str")
        self.__facility_name = facility_name

    @property
    def rooms(self) -> list[Room]:
        return self.__rooms.copy()

    def add_room(self, room: Room) -> None:
        # Fügt dieser Einrichtung ein Zimmer hinzu und setzt im Zimmer die Rückreferenz.
        from model.room import Room
        if not isinstance(room, Room):
            raise ValueError("room must be a Room instance")
        if room not in self.__rooms:
            self.__rooms.append(room)
            room.add_facility(self)

    def remove_room(self, room: Room) -> None:
        # Entfernt ein Zimmer von dieser Einrichtung und entfernt im Zimmer die Rückreferenz.
        from model.room import Room
        if room in self.__rooms:
            self.__rooms.remove(room)
            room.remove_facility(self)

    def get_facility_info(self) -> str:
        # Gibt den Namen dieser Einrichtung zurück.
        return self.__facility_name