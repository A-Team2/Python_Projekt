class Guest:
    def __init__(self, guest_id: int, first_name: str, last_name: str, email: str, address_id: int):
        self._guest_id = guest_id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._address_id = address_id

    def guest_id(self) -> int:
        return self._guest_id

    def first_name(self) -> str:
        return self._first_name

    def first_name_set(self, name: str) -> None:
        self._first_name = name

    def last_name(self) -> str:
        return self._last_name

    def last_name_set(self, name: str) -> None:
        self._last_name = name

    def email(self) -> str:
        return self._email

    def email_set(self, mail: str) -> None:
        self._email = mail

    def address_id(self) -> int:
        return self._address_id

    def address_id_set(self, address_id: int) -> None:
        self._address_id = address_id

    def __repr__(self):
        return f"Guest(id={self._guest_id}, name='{self._first_name} {self._last_name}')"
