from data_access.base_data_access import BaseDataAccess
from model.room_type import RoomType

class RoomTypeDataAccess(BaseDataAccess):
    def read_all_room_types(self) -> list[RoomType]:
        sql = """
        SELECT type_id, description, max_guests
        FROM Room_Type
        """
        rows = self.fetchall(sql)
        return [RoomType(*row) for row in rows]
