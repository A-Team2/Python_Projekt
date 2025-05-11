from __future__ import annotations

class Address:
    """
    Model Class Address
    """
    def __init__(self, address_id: int, street: str, city: str, zip_code: str):
        # Ensure values for not nullable attributes or not the right type
        if address_id is None or not isinstance(address_id, int):
            raise ValueError("address_id is required and must be int")
        if not street or not isinstance(street, str):
            raise ValueError("street is required and must be str")
        if not city or not isinstance(city, str):
            raise ValueError("city is required and must be str")
        if not zip_code or not isinstance(zip_code, str):
            raise ValueError("zip_code is required and must be str")

        # private Attributes
        self.__address_id: int = address_id
        self.__street: str    = street
        self.__city: str      = city
        self.__zip_code: str  = zip_code

    def __repr__(self) -> str:
        return (
            f"Address(id={self.__address_id!r}, "
            f"{self.__street!r}, {self.__zip_code!r} {self.__city!r})"
        )

    @property
    def address_id(self) -> int:
        return self.__address_id

    @property
    def street(self) -> str:
        return self.__street

    @street.setter
    def street(self, street: str) -> None:
        if not street or not isinstance(street, str):
            raise ValueError("street must be an str")
        self.__street = street

    @property
    def city(self) -> str:
        return self.__city

    @city.setter
    def city(self, city: str) -> None:
        if not city or not isinstance(city, str):
            raise ValueError("city must be an str")
        self.__city = city

    @property
    def zip_code(self) -> str:
        return self.__zip_code

    @zip_code.setter
    def zip_code(self, zip_code: str) -> None:
        if not zip_code or not isinstance(zip_code, str):
            raise ValueError("zip_code must be an str")
        self.__zip_code = zip_code

    def get_full_address(self) -> str:
        # Returns a formatted address.
        return f"{self.__street}, {self.__zip_code} {self.__city}"