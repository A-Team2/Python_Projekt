from data_access.base_data_access import BaseDataAccess
from model.guest import Guest

class GuestDataAccess(BaseDataAccess):
    def create_guest(self, guest: Guest) -> int:
        sql = """
        INSERT INTO guest (first_name, last_name, email, address_id)
        VALUES (?, ?, ?, ?)
        """
        params = (guest.first_name, guest.last_name, guest.email, guest.address_id)
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
            return Guest(*row)
        return None

    def read_all_guests(self) -> list[Guest]:
        sql = "SELECT guest_id, first_name, last_name, email, address_id FROM guest"
        rows = self.fetchall(sql)
        return [Guest(*row) for row in rows]
