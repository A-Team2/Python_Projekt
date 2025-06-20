from model.guest import Guest
from data_access.guest_data_access import GuestDataAccess

class GuestManager:
    def __init__(self):
        self.__guest_da = GuestDataAccess()

    def read_guest_by_id(self, guest_id: int) -> Guest | None:
        # Validierung
        if not isinstance(guest_id, int) or guest_id < 1:
            raise ValueError("guest_id muss eine positive Ganzzahl sein")
        # Delegation an DAL
        return self.__guest_da.read_guest_by_id(guest_id)

    def read_guest_by_email(self, email: str) -> Guest | None:
        # Validierung
        if not email or not isinstance(email, str):
            raise ValueError("email muss eine nicht-leere Zeichenkette sein")
        # Delegation an DAL
        return self.__guest_da.read_guest_by_email(email)

    def create_guest(
        self,
        first_name: str,
        last_name: str,
        email: str,
        address: 'Address'
    ) -> Guest:
        # Validierung der Eingaben
        if not first_name or not isinstance(first_name, str):
            raise ValueError("first_name musst eine nicht-leere Zeichenkette sein")
        if not last_name or not isinstance(last_name, str):
            raise ValueError("last_name muss eine nicht-leere Zeichenkette sein")
        if not email or not isinstance(email, str):
            raise ValueError("email muss eine nicht-leere Zeichenkette sein")
        if address is None or not hasattr(address, 'address_id'):
            raise ValueError("address muss ein valid Address-Objekt sein")
        # Insert in DB, liefert neue guest_id
        new_id = self.__guest_da.insert_guest(
            first_name = first_name,
            last_name  = last_name,
            email      = email,
            address_id = address.address_id
        )
        # Sofort frisch laden und zurückgeben
        guest = self.__guest_da.read_guest_by_id(new_id)
        if guest is None:
            raise RuntimeError(f"Konnte Gast nicht laden mit GastId: {new_id}")
        return guest

    def read_all_guests(self) -> list[Guest]:
        # Einfach alle Gäste auslesen
        return self.__guest_da.read_all_guests()