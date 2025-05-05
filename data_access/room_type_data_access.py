from data_access.base_data_access import BaseDataAccess
from model.room_type import RoomType

class RoomTypeDataAccess(BaseDataAccess):
    def read_all_room_types(self) -> list[RoomType]:
        sql = """
        SELECT room_type_id, name, description
        FROM room_type
        """
        rows = self.fetchall(sql)
        return [RoomType(*row) for row in rows]
