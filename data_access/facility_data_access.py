from data_access.base_data_access import BaseDataAccess
from model.facilities import Facilities

class FacilityDataAccess(BaseDataAccess):
    def read_all_facilities(self) -> list[Facilities]:
        sql = "SELECT facility_id, facility_name FROM facilities"
        rows = self.fetchall(sql)
        return [Facilities(*row) for row in rows]

    def read_facilities_by_room(self, room_id: int) -> list[Facilities]:
        sql = """
        SELECT f.facility_id, f.facility_name
        FROM facilities f
        JOIN room_facilities rf ON f.facility_id = rf.facility_id
        WHERE rf.room_id = ?
        """
        rows = self.fetchall(sql, (room_id,))
        return [Facilities(*row) for row in rows]

    def assign_facility_to_room(self, room_id: int, facility_id: int) -> None:
        sql = "INSERT INTO room_facilities (room_id, facility_id) VALUES (?, ?)"
        self.execute(sql, (room_id, facility_id))
