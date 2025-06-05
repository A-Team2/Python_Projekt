from data_access.analytics_data_access import AnalyticsDataAccess
import pandas as pd


class AnalyticsManager:
    """
    Business-Logic-Layer für Analysen (z.B. Belegungsraten).
    """

    def __init__(self):
        # Initialisiere die DataAccess-Klasse für Analytics
        self.__analytics_da = AnalyticsDataAccess()

    def get_occupancy_by_room_type(self, hotel_id: int) -> pd.DataFrame:
        """
        Holt aus der DAL eine Liste von Tupeln:
            (type_id, description, total_rooms, booked_rooms, belegung_rate)
        und baut daraus ein pandas.DataFrame mit genau diesen Spalten:

        Spalten (in exakt dieser Reihenfolge):
          - type_id        : int    (ID des Zimmertyps)
          - description    : str    (Beschreibung, z.B. "Single", "Suite" etc.)
          - total_rooms    : int    (Anzahl aller Räume dieses Typs im Hotel)
          - booked_rooms   : int    (Anzahl aktuell gebuchter Räume dieses Typs)
          - belegung_rate  : float  (Verhältnis booked_rooms/total_rooms, Wert zwischen 0 und 1)
        """
        # 1) Liste von Tupeln aus der DAL holen
        rows = self.__analytics_da.read_occupancy_by_hotel(hotel_id)

        # 2) DataFrame erzeugen – die Spaltennamen müssen exakt passen:
        df = pd.DataFrame(
            rows,
            columns=[
                "type_id",       # ID des Zimmertyps
                "description",   # Beschreibung (z. B. "Double", "Suite" usw.)
                "total_rooms",   # Anzahl aller Räume dieses Typs
                "booked_rooms",  # Anzahl aktuell gebuchter Räume
                "belegung_rate"  # Verhältnis booked_rooms / total_rooms (float 0–1)
            ]
        )

        return df