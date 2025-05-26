from data_access.base_data_access import BaseDataAccess
from model.guest import Guest
from data_access.address_data_access import AddressDataAccess

class GuestDataAccess(BaseDataAccess):
    def create_guest(self, guest: Guest) -> int:
        sql = """
        INSERT INTO guest (first_name, last_name, email, address_id)
        VALUES (?, ?, ?, ?)
        """
        params = (guest.first_name, guest.last_name, guest.email, guest.address.address_id)
        last_id, _ = self.execute(sql, params)
        return last_id

    def read_guest_by_id(self, guest_id: int) -> Guest | None: 
        sql = """
        SELECT guest_id, first_name, last_name, email, address_id
        FROM guest
        WHERE guest_id = ?
        """
        row = self.fetchone(sql, (guest_id,))
        if row:
            guest_id, first_name, last_name, email, address_id = row
            address_da = AddressDataAccess()
            address = address_da.read_address_by_id(address_id)
            if address is None:
                return None
            return Guest(guest_id, first_name, last_name, email, address)
        return None

    def read_all_guests(self) -> list[Guest]:
        sql = "SELECT guest_id, first_name, last_name, email, address_id FROM guest"
        rows = self.fetchall(sql)
        address_da = AddressDataAccess()
        guests = []
        for row in rows:
            guest_id, first_name, last_name, email, address_id = row
            address = address_da.read_address_by_id(address_id)
            if address:
                guests.append(Guest(guest_id, first_name, last_name, email, address))
        return guests
    
    def read_guest_by_email(self, email: str) -> Guest | None:
        sql = """
        SELECT guest_id, first_name, last_name, email, address_id
        FROM guest
        WHERE email = ?
        """
        row = self.fetchone(sql, (email,))
        if not row:
            return None

        guest_id, first_name, last_name, email, address_id = row
        address = AddressDataAccess().read_address_by_id(address_id)
        if address is None:
            return None

        return Guest(guest_id, first_name, last_name, email, address)
    
    def insert_guest(
        self,
        *,
        first_name: str,
        last_name: str,
        email: str,
        address_id: int
    ) -> int:
        
        # Legt einen neuen Gast an.
        
        sql = """
        INSERT INTO guest (first_name, last_name, email, address_id)
        VALUES (?, ?, ?, ?)
        """
        params = (first_name, last_name, email, address_id)
        last_id, _ = self.execute(sql, params)
        return last_id
