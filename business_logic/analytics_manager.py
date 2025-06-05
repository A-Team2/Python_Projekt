from data_access.room_data_access import RoomDataAccess

class AnalyticsManager:
# Stellt Auswertungen und Charts bereit (z.B. Belegungsraten pro Zimmertyp).
    
    def __init__(self):
        self.__room_da = RoomDataAccess()

    def get_occupancy_by_room_type(self, hotel_id: int) -> list[tuple[str, int]]:
        
        #Gibt eine Liste von (room_type_description, belegung) zurück,
        #wobei 'belegung' die Anzahl aktiver (nicht stornierter) Buchungen dieses Zimmertyps ist.
        
        if not isinstance(hotel_id, int) or hotel_id < 1:
            raise ValueError("hotel_id muss eine positive Ganzzahl sein")
        return self.__room_da.read_occupancy_by_room_type(hotel_id)