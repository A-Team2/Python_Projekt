from data_access.base_data_access import BaseDataAccess
from model.booking import Booking

class BookingDataAccess(BaseDataAccess):
    def create_booking(self, booking: Booking) -> int:
        sql = """
        INSERT INTO booking (check_in_date, check_out_date, is_cancelled, total_amount, guest_id, room_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            booking.check_in_date,
            booking.check_out_date,
            int(booking.is_cancelled),  # SQLite kennt kein echtes BOOL
            booking.total_amount,
            booking.guest_id,
            booking.room_id
        )
        last_id, _ = self.execute(sql, params)
        return last_id

    def read_booking_by_id(self, booking_id: int) -> Booking | None:
        sql = """
        SELECT booking_id, check_in_date, check_out_date, is_cancelled, total_amount, guest_id, room_id
        FROM booking
        WHERE booking_id = ?
        """
        row = self.fetchone(sql, (booking_id,))
        if row:
            return Booking(*row)
        return None

    def cancel_booking(self, booking_id: int) -> bool:
        sql = "UPDATE booking SET is_cancelled = 1 WHERE booking_id = ?"
        _, affected = self.execute(sql, (booking_id,))
        return affected == 1  # True, wenn genau eine Buchung aktualisiert wurde
