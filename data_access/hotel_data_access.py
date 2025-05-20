from data_access.base_data_access import BaseDataAccess
from data_access.address_data_access import AddressDataAccess
from data_access.room_data_access import RoomDataAccess
from model.hotel import Hotel
from datetime import date

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
        WHERE LOWER(a.city) = LOWER(?)
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

    def read_hotels_by_all_criteria(self, city: str, min_stars: int, guest_count: int, check_in_date: date, check_out_date: date) -> list[Hotel]:
        sql = """
        SELECT DISTINCT
            h.hotel_id, h.name, h.stars, h.address_id
        FROM
            Hotel h
        JOIN
            Address a ON h.address_id = a.address_id
        JOIN
            Room r ON r.hotel_id = h.hotel_id
        JOIN
            Room_Type rt ON r.type_id = rt.type_id
        LEFT JOIN -- Use LEFT JOIN to include rooms without bookings
            Booking b ON b.room_id = r.room_id AND b.is_cancelled = 0
        WHERE
            LOWER(a.city) = LOWER(?) -- City filter (case-insensitive)
            AND h.stars >= ? -- Minimum stars filter
            AND rt.max_guests >= ? -- Minimum guests per room filter
            -- Check for NO overlapping active bookings
            AND NOT EXISTS (
                SELECT 1
                FROM Booking b_overlap
                WHERE b_overlap.room_id = r.room_id
                AND b_overlap.is_cancelled = 0
                AND b_overlap.check_in_date < ? -- Requested check_out_date
                AND b_overlap.check_out_date > ? -- Requested check_in_date
            );
        """
        params = (city, min_stars, guest_count, check_out_date, check_in_date)
        rows = self.fetchall(sql, params)
        hotels = []
        for row in rows:
            hotel_id, name, stars, address_id = row
            address = self.__address_da.read_address_by_id(address_id)
            hotel = Hotel(hotel_id, name, stars, address)
            self.__load_hotel_rooms(hotel)
            hotels.append(hotel)
        return hotels

    def read_hotel_by_name(self, name: str) -> Hotel | None:
        sql = """
        SELECT h.hotel_id, h.name, h.stars, h.address_id
        FROM Hotel h
        WHERE LOWER(h.name) = LOWER(?)
        """
        row = self.fetchone(sql, (name,))

        if row:
            hotel_id, name, stars, address_id = row
            address = self.__address_da.read_address_by_id(address_id)
            hotel = Hotel(hotel_id, name, stars, address)
            self.__load_hotel_rooms(hotel)
            return hotel
        return None
