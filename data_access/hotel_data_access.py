from data_access.base_data_access import BaseDataAccess
from data_access.address_data_access import AddressDataAccess
from data_access.room_data_access import RoomDataAccess
from model.hotel import Hotel

class HotelDataAccess(BaseDataAccess):
    def __init__(self):
        super().__init__()
        self.__address_da = AddressDataAccess()
        self.__room_da = RoomDataAccess()

    def __load_hotel_rooms(self, hotel: Hotel) -> None:
        """Lädt alle Zimmer für ein Hotel."""
        rooms = self.__room_da.read_rooms_by_hotel_id(hotel.hotel_id, hotel)
        for room in rooms:
            hotel.add_room(room)

    def read_all_hotels(self) -> list[Hotel]:
        sql = """
        SELECT hotel_id, name, stars, address_id
        FROM Hotel
        """
        rows = self.fetchall(sql)
        hotels = []

        for row in rows:
            hotel_id, name, stars, address_id = row
            address = self.__address_da.read_address_by_id(address_id)
            hotel = Hotel(hotel_id, name, stars, address)
            self.__load_hotel_rooms(hotel)
            hotels.append(hotel)

        return hotels

    def read_hotels_by_city(self, city: str) -> list[Hotel]:
        sql = """
        SELECT h.hotel_id, h.name, h.stars, h.address_id
        FROM Hotel h
        JOIN Address a ON h.address_id = a.address_id
        WHERE a.city = ?
        """
        rows = self.fetchall(sql, (city,))
        hotels = []

        for row in rows:
            hotel_id, name, stars, address_id = row
            address = self.__address_da.read_address_by_id(address_id)
            hotel = Hotel(hotel_id, name, stars, address)
            self.__load_hotel_rooms(hotel)
            hotels.append(hotel)

        return hotels

    def read_hotels_by_city_and_stars(self, city: str, stars: int) -> list[Hotel]:
        sql = """
        SELECT h.hotel_id, h.name, h.stars, h.address_id
        FROM Hotel h
        JOIN Address a ON h.address_id = a.address_id
        WHERE a.city = ? AND h.stars = ?
        """
        rows = self.fetchall(sql, (city, stars))
        hotels = []

        for row in rows:
            hotel_id, name, stars, address_id = row
            address = self.__address_da.read_address_by_id(address_id)
            hotel = Hotel(hotel_id, name, stars, address)
            self.__load_hotel_rooms(hotel)
            hotels.append(hotel)

        return hotels
