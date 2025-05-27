from datetime import date
from model.booking import Booking
from model.guest import Guest
from model.room import Room
from data_access.booking_data_access import BookingDataAccess
from business_logic.hotel_manager import HotelManager
from data_access.guest_data_access import GuestDataAccess 

# BookingManager verwaltet alle Buchungsregeln
class BookingManager:
    def __init__(self):
        self.__booking_da = BookingDataAccess()

    # Erstellt eine neue Buchung
    def create_booking(
        self,
        guest: Guest,
        room: Room,
        check_in: date,
        check_out: date
    ) -> Booking:
        # Prüft die Eingaben
        if check_out <= check_in:
            raise ValueError("Check-out muss nach Check-in liegen.")
        if not room.is_available(check_in, check_out):
            raise ValueError("Zimmer im gewünschten Zeitraum nicht verfügbar.")

        # Fuegt die Buchung in die Datenbank ein
        new_id = self.__booking_da.insert_booking(
            guest_id       = guest.guest_id,
            room_id        = room.room_id,
            check_in_date  = check_in,
            check_out_date = check_out
        )

        # Laedt die neue Buchung aus der Datenbank
        booking = self.__booking_da.read_booking_by_id(new_id)
        if booking is None:
            raise RuntimeError(f"Neue Buchung #{new_id} konnte nicht geladen werden.")
        return booking
    
    # Gibt alle Buchungen für einen Gast zurück
    def get_bookings_for_guest(self, guest) -> list[Booking]:
        # 1) Validierung
        from model.guest import Guest
        if guest is None or not isinstance(guest, Guest):
            raise ValueError("guest is required and must be a Guest instance")
        # 2) DB‐Rows abholen
        rows = self.__booking_da.read_bookings_by_guest_id(guest.guest_id)
        # 3) in Booking‐Objekte wandeln
        bookings: list[Booking] = []
        hotel_manager = HotelManager()
        for row in rows:
            booking_id, check_in_date, check_out_date, is_cancelled, total_amount, guest_id, room_id = row
            room = hotel_manager.get_room_by_id(room_id) if room_id else None
            rooms = [room] if room else []
            bookings.append(Booking(
                booking_id=booking_id,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                guest=guest,
                rooms=rooms,
                total_amount=float(total_amount),
                is_cancelled=bool(is_cancelled)
            ))
        return bookings
    
    # Gibt eine Buchung anhand der ID zurück
    def read_booking(self, booking_id: int) -> Booking | None:
        return self.__booking_da.read_booking_by_id(booking_id)

    # Storniert eine Buchung
    def cancel_booking(self, booking_id: int) -> None:
        if not isinstance(booking_id, int) or booking_id < 1:
            raise ValueError("booking_id must be a positive integer")
        # Prüfungen, ob die Buchung existiert
        booking = self.read_booking(booking_id)
        if booking is None:
            raise ValueError(f"No booking with id {booking_id}")
        # 1) DB-Flag setzen
        self.__booking_da.cancel_booking(booking_id)
        # 2) Objekt ebenfalls updaten
        booking.is_cancelled = True
        
    def get_all_bookings(self) -> list[Booking]:
        # 1) Alle Daten-Zeilen aus der DB holen
        rows = self.__booking_da.read_all_bookings()
        # 2) In Booking-Objekte umwandeln
        bookings: list[Booking] = []
        for b_id, ci, co, cancelled, total, guest_id, room_id in rows:
            guest = GuestDataAccess().read_guest_by_id(guest_id)
            booking = Booking(
                b_id,
                datetime.strptime(ci, "%Y-%m-%d").date() if isinstance(ci, str) else ci,
                datetime.strptime(co, "%Y-%m-%d").date() if isinstance(co, str) else co,
                guest,
                [],  # rooms nicht gebraucht
                float(total),
                bool(cancelled)
            )
            bookings.append(booking)
        return bookings