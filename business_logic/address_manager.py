from model.address import Address
from data_access.address_data_access import AddressDataAccess

class AddressManager:
    def __init__(self):
        self.__address_da = AddressDataAccess()

    def create_address(self, address: Address) -> int:
        # Validierung
        if not isinstance(address, Address):
            raise ValueError("address must be an Address object")
        return self.__address_da.create_address(address)

    def read_address_by_id(self, address_id: int) -> Address | None:
        if not isinstance(address_id, int) or address_id < 1:
            raise ValueError("address_id must be a positive integer")
        return self.__address_da.read_address_by_id(address_id) 