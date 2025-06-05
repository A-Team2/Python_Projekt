from data_access.room_data_access import RoomDataAccess
import pandas as pd

def get_occupancy_by_room_type(self, hotel_id: int) -> pd.DataFrame:
         """
         Holt aus dem DataAccess eine Liste von Tupeln
         (type_id, description, total_rooms, booked_rooms, belegung_rate)
         und baut daraus ein pandas.DataFrame mit genau diesen Spalten:
         """
         # 1) Liste von Tupeln aus der DAL holen
         rows = self.__analytics_da.read_occupancy_by_hotel(hotel_id)

         # 2) DataFrame erzeugen – die Spaltennamen müssen exakt passen
         df = pd.DataFrame(rows, columns=[
             "type_id",       # ID des Zimmertyps
             "description",   # Beschreibung (z. B. „Double“, „Suite“ usw.)
             "total_rooms",   # Anzahl aller Räume dieses Typs
             "booked_rooms",  # Anzahl aktuell gebuchter Räume
             "belegung_rate"  # Verhältnis booked_rooms / total_rooms (float 0–1)
         ])
         return df