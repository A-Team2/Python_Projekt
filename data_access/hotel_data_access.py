from data_access.base_data_access import BaseDataAccess
from data_access.address_data_access import AddressDataAccess  # Hinzugefügt
from model.hotel import Hotel

class HotelDataAccess(BaseDataAccess):
    def __init__(self):
        super().__init__()
        self.__address_da = AddressDataAccess()  # Address-Zugriffsklasse

    def read_all_hotels(self) -> list[Hotel]:
        sql = """
        SELECT hotel_id, name, stars, address_id
        FROM hotel
        """
        rows = self.fetchall(sql)
        hotels = []

        for row in rows:
            hotel_id, name, stars, address_id = row
            address = self.__address_da.read_address_by_id(address_id)
            hotels.append(Hotel(hotel_id, name, stars, address))

        return hotels

    def read_hotels_by_city(self, city: str) -> list[Hotel]:
        sql = """
        SELECT h.hotel_id, h.name, h.stars, h.address_id
        FROM hotel h
        JOIN address a ON h.address_id = a.address_id
        WHERE a.city = ?
        """
        rows = self.fetchall(sql, (city,))
        hotels = []

        for row in rows:
            hotel_id, name, stars, address_id = row
            address = self.__address_da.read_address_by_id(address_id)
            hotels.append(Hotel(hotel_id, name, stars, address))

        return hotels

    def read_hotels_by_city_and_stars(self, city: str, stars: int) -> list[Hotel]:
        sql = """
        SELECT h.hotel_id, h.name, h.stars, h.address_id
        FROM hotel h
        JOIN address a ON h.address_id = a.address_id
        WHERE a.city = ? AND h.stars = ?
        """
        rows = self.fetchall(sql, (city, stars))
        hotels = []

        for row in rows:
            hotel_id, name, stars, address_id = row
            address = self.__address_da.read_address_by_id(address_id)
            hotels.append(Hotel(hotel_id, name, stars, address))

        return hotels
