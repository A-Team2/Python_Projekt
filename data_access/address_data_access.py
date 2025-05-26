from data_access.base_data_access import BaseDataAccess
from model.address import Address

class AddressDataAccess(BaseDataAccess):
    def create_address(self, address: Address) -> int:
        sql = """
        INSERT INTO Address (street, city, zip_code)
        VALUES (?, ?, ?)
        """
        params = (address.street, address.city, address.zip_code)
        last_id, _ = self.execute(sql, params)
        return int(last_id)

    def read_address_by_id(self, address_id: int) -> Address | None:
        sql = """
        SELECT address_id, street, city, zip_code
        FROM Address
        WHERE address_id = ?
        """
        row = self.fetchone(sql, (address_id,))
        if row:
            return Address(*row)
        return None
