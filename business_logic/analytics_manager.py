from data_access.room_data_access import RoomDataAccess
import pandas as pd

class AnalyticsManager:
    def __init__(self):
        self.__analytics_da = AnalyticsDataAccess()

    def get_occupancy_by_room_type(self, hotel_id: int) -> pd.DataFrame:
        # Beispiel: AnalyticsDataAccess liefert List[tuple] in der Form
        # [(type_id, description, total_rooms, booked_rooms, belegung_rate), …]
        rows = self.__analytics_da.read_occupancy_by_hotel(hotel_id)

        # Spaltennamen genau so wählen, wie Du sie später im Notebook ansprichst
        columns = ["type_id", "description", "total_rooms", "booked_rooms", "belegung_rate"]

        # DataFrame erstellen
        df = pd.DataFrame(rows, columns=columns)

        return df