from data_access.room_data_access import RoomDataAccess
from datetime import date, timedelta

class PricingManager:
    def __init__(self):
        self.room_dao = RoomDataAccess()

    def calculate_price(
        self,
        room_id: int,
        check_in: date,
        check_out: date
    ) -> float:
        # 1) Zimmer laden
        room = self.room_dao.read_room_by_id(room_id)
        if not room:
            raise ValueError("Zimmer nicht gefunden.")

        # 2) Aufenthaltsdauer prüfen
        nights = (check_out - check_in).days
        if nights <= 0:
            raise ValueError("Aufenthaltsdauer muss mindestens 1 Nacht sein.")

        # 3) Saisonal dynamischen Preis pro Tag berechnen
        total = 0.0
        current = check_in
        while current < check_out:
            base = room.price_per_night
            month = current.month

            if 6 <= month <= 8:
                factor = 1.2   # Hochsaison
            elif month in (11, 12, 1, 2):
                factor = 0.8   # Nebensaison
            else:
                factor = 1.0   # Zwischensaison

            total += base * factor
            current += timedelta(days=1)

        return round(total, 2)