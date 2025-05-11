from data_access.booking_data_access import BookingDataAccess

class BookingManager:
    def __init__(self):
        self.booking_dao = BookingDataAccess()

    def cancel_booking(self, booking_id: int) -> bool:
        return self.booking_dao.cancel_booking(booking_id)

    def get_booking_by_id(self, booking_id: int):
        return self.booking_dao.read_booking_by_id(booking_id)
