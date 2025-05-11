from data_access.room_data_access import RoomDataAccess
from datetime import timedelta, date

class PricingManager:
    def __init__(self):
        self.room_dao = RoomDataAccess()

    def calculate_price(self, room_id: int, check_in: date, check_out: date, guests: int) -> float:
        room = self.room_dao.read_room_by_id(room_id)
        if not room:
            raise ValueError("Zimmer nicht gefunden.")

        nights = (check_out - check_in).days
        if nights <= 0:
            raise ValueError("Aufenthaltsdauer muss mindestens 1 Nacht sein.")

        price = room.base_price_per_night * nights

        # Zuschläge
        if guests > room.max_guests:
            raise ValueError("Zu viele Gäste für diesen Zimmertyp.")

        if guests > 2:
            price *= 1.2  # 20% Aufschlag ab 3 Gästen

        if nights >= 5:
            price *= 0.9  # 10% Rabatt für längeren Aufenthalt

        return round(price, 2)
