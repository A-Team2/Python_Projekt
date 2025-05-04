class Hotel:
    def __init__(self, hotel_id: int, name: str, stars: int, address_id: int):
        self._hotel_id = hotel_id
        self._name = name
        self._stars = stars
        self._address_id = address_id

    def hotel_id(self) -> int:
        return self._hotel_id

    def name(self) -> str:
        return self._name

    def name_set(self, name: str) -> None:
        self._name = name

    def stars(self) -> int:
        return self._stars

    def stars_set(self, stars: int) -> None:
        self._stars = stars

    def address_id(self) -> int:
        return self._address_id

    def address_id_set(self, address_id: int) -> None:
        self._address_id = address_id

    def __repr__(self):
        return f"Hotel(id={self._hotel_id}, name='{self._name}', stars={self._stars})"
