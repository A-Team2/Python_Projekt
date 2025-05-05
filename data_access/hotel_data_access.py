from data_access.base_data_access import BaseDataAccess
from model.hotel import Hotel

class HotelDataAccess(BaseDataAccess):
    def read_all_hotels(self) -> list[Hotel]:
        sql = """
        SELECT hotel_id, name, description, stars, address_id
        FROM hotel
        """
        rows = self.fetchall(sql)
        return [Hotel(*row) for row in rows]

    def read_hotels_by_city(self, city: str) -> list[Hotel]:
        sql = """
        SELECT h.hotel_id, h.name, h.description, h.stars, h.address_id
        FROM hotel h
        JOIN address a ON h.address_id = a.address_id
        WHERE a.city = ?
        """
        rows = self.fetchall(sql, (city,))
        return [Hotel(*row) for row in rows]

    def read_hotels_by_city_and_stars(self, city: str, stars: int) -> list[Hotel]:
        sql = """
        SELECT h.hotel_id, h.name, h.description, h.stars, h.address_id
        FROM hotel h
        JOIN address a ON h.address_id = a.address_id
        WHERE a.city = ? AND h.stars = ?
        """
        rows = self.fetchall(sql, (city, stars))
        return [Hotel(*row) for row in rows]
