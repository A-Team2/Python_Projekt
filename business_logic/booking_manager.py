from datetime import date
from model.booking import Booking
from model.guest import Guest
from model.room import Room
from data_access.booking_data_access import BookingDataAccess

class BookingManager:
    def __init__(self):
        self.__booking_da = BookingDataAccess()

    def create_booking(
        self,
        guest: Guest,
        room: Room,
        check_in: date,
        check_out: date
    ) -> Booking:
        # 1) Prüfung
        if check_out <= check_in:
            raise ValueError("Check-out muss nach Check-in liegen.")
        if not room.is_available(check_in, check_out):
            raise ValueError("Zimmer im gewünschten Zeitraum nicht verfügbar.")

        # 2) Insert in die DB – liefert booking_id
        new_id = self.__booking_da.insert_booking(
            guest_id       = guest.guest_id,
            room_id        = room.room_id,
            check_in_date  = check_in,
            check_out_date = check_out
        )

        # 3) Frisch aus der DB laden und zurückgeben
        booking = self.__booking_da.read_booking_by_id(new_id)
        if booking is None:
            raise RuntimeError(f"Neue Buchung #{new_id} konnte nicht geladen werden.")
        return booking