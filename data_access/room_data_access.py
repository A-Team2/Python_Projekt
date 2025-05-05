from data_access.base_data_access import BaseDataAccess
from model.room import Room

class RoomDataAccess(BaseDataAccess):
    def read_rooms_by_hotel(self, hotel_id: int) -> list[Room]:
        sql = """
        SELECT room_id, hotel_id, room_type_id, price
        FROM room
        WHERE hotel_id = ?
        """
        rows = self.fetchall(sql, (hotel_id,))
        return [Room(*row) for row in rows]

    def read_available_rooms(self, hotel_id: int, check_in, check_out) -> list[Room]:
        sql = """
        SELECT r.room_id, r.hotel_id, r.room_type_id, r.price
        FROM room r
        WHERE r.hotel_id = ?
        AND r.room_id NOT IN (
            SELECT b.room_id
            FROM booking b
            WHERE b.is_cancelled = 0
            AND (
                b.check_in_date < ? AND b.check_out_date > ?
            )
        )
        """
        params = (hotel_id, check_out, check_in)
        rows = self.fetchall(sql, params)
        return [Room(*row) for row in rows]
