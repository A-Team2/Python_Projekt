from data_access.base_data_access import BaseDataAccess
from model.booking import Booking
from model.guest import Guest
from model.address import Address
from data_access.guest_data_access import GuestDataAccess
from datetime import date

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
            booking_id, check_in_date, check_out_date, is_cancelled, total_amount, guest_id, room_id = row
            guest = GuestDataAccess().read_guest_by_id(guest_id)
            # rooms = ... (hier leer, da Einzelbuchung)
            return Booking(booking_id, check_in_date, check_out_date, guest, [], float(total_amount), bool(is_cancelled))
        return None

    def cancel_booking(self, booking_id: int) -> bool:
        sql = "UPDATE booking SET is_cancelled = 1 WHERE booking_id = ?"
        _, affected = self.execute(sql, (booking_id,))
        return affected == 1  # True, wenn genau eine Buchung aktualisiert wurde

    def read_bookings_by_room(self, room_id: int) -> list[Booking]:
        sql = """
        SELECT booking_id, check_in_date, check_out_date, is_cancelled, total_amount, guest_id, room_id
        FROM Booking
        WHERE room_id = ?
        """
        rows = self.fetchall(sql, (room_id,))
        guest_da = GuestDataAccess()
        bookings = []
        for row in rows:
            booking_id, check_in_date, check_out_date, is_cancelled, total_amount, guest_id, room_id = row
            guest = guest_da.read_guest_by_id(guest_id)
            if guest is None:
                continue  # Buchung ignorieren, wenn Gast nicht existiert
            booking = Booking(booking_id, check_in_date, check_out_date, guest, [], float(total_amount), bool(is_cancelled))
            bookings.append(booking)
        return bookings
    
    def insert_booking(
        self,
        *,
        guest_id: int,
        room_id: int,
        check_in_date: date,
        check_out_date: date
    ) -> int:
        sql = """
        INSERT INTO booking (guest_id, room_id, check_in_date, check_out_date, total_amount, is_cancelled)
        VALUES (?, ?, ?, ?, 0.0, 0)
        """
        # wir setzen total_amount=0.0 und is_cancelled=0 als Default
        last_id, _ = self.execute(
            sql,
            (guest_id, room_id, check_in_date.isoformat(), check_out_date.isoformat())
        )
        return last_id
    
    def read_bookings_by_guest_id(self, guest_id: int) -> list[tuple]:
        
        # Liefert alle Buchungs‐Zeilen für einen Gast.
        
        sql = """
        SELECT booking_id,
               check_in_date,
               check_out_date,
               is_cancelled,
               total_amount,
               guest_id,
               room_id
          FROM booking
         WHERE guest_id = ?
        ORDER BY check_in_date
        """
        return self.fetchall(sql, (guest_id,))
    
    def read_all_bookings(self) -> list[tuple]:
        sql = """
        SELECT booking_id,
               check_in_date,
               check_out_date,
               is_cancelled,
               total_amount,
               guest_id,
               room_id
          FROM booking
        ORDER BY check_in_date
        """
        return self.fetchall(sql, ())
