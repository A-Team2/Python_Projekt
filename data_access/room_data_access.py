from data_access.base_data_access import BaseDataAccess
from model.room import Room
from model.hotel import Hotel
from model.room_type import RoomType
from data_access.booking_data_access import BookingDataAccess

class RoomDataAccess(BaseDataAccess):
    def read_rooms_by_hotel_id(self, hotel_id: int, hotel: Hotel = None) -> list[Room]:
        sql = """
        SELECT r.room_id, r.room_number, r.price_per_night, r.hotel_id, r.type_id
        FROM Room r
        JOIN Room_Type rt ON r.type_id = rt.type_id
        WHERE r.hotel_id = ?
        """
        rows = self.fetchall(sql, (hotel_id,))
        rooms = []
        
        for row in rows:
            room_id, room_number, price_per_night, hotel_id, type_id = row
            room_number = int(room_number)
            # Hole das Hotel nur, wenn nicht übergeben
            if hotel is None:
                hotel_sql = "SELECT hotel_id, name, stars, address_id FROM Hotel WHERE hotel_id = ?"
                hotel_row = self.fetchone(hotel_sql, (hotel_id,))
                if hotel_row:
                    hotel_id, name, stars, address_id = hotel_row
                    address_sql = "SELECT address_id, street, city, zip_code FROM Address WHERE address_id = ?"
                    address_row = self.fetchone(address_sql, (address_id,))
                    if address_row:
                        from model.address import Address
                        address = Address(*address_row)
                        hotel_obj = Hotel(hotel_id, name, stars, address)
                    else:
                        print(f"Warnung: Keine Adresse gefunden für address_id {address_id}")
                        continue
                else:
                    print(f"Warnung: Kein Hotel gefunden für hotel_id {hotel_id}")
                    continue
            else:
                hotel_obj = hotel
            # Hole den Raumtyp
            room_type_sql = "SELECT type_id, description, max_guests FROM Room_Type WHERE type_id = ?"
            room_type_row = self.fetchone(room_type_sql, (type_id,))
            if room_type_row:
                type_id, description, max_guests = room_type_row
                room_type = RoomType(type_id, description, max_guests)
                room = Room(room_id, room_number, price_per_night, hotel_obj, room_type)
                # Buchungen laden und zuweisen
                booking_da = BookingDataAccess()
                bookings = booking_da.read_bookings_by_room(room_id)
                for booking in bookings:
                    room.add_booking(booking)
                rooms.append(room)
        return rooms

    def read_available_rooms(self, hotel_id: int, check_in, check_out) -> list[Room]:
        sql = """
        SELECT r.room_id, r.room_number, r.price_per_night, r.hotel_id, r.type_id
        FROM Room r
        JOIN Room_Type rt ON r.type_id = rt.type_id
        WHERE r.hotel_id = ?
        AND r.room_id NOT IN (
            SELECT b.room_id
            FROM Booking b
            WHERE b.is_cancelled = 0
            AND (
                b.check_in_date < ? AND b.check_out_date > ?
            )
        )
        """
        params = (hotel_id, check_out, check_in)
        rows = self.fetchall(sql, params)
        rooms = []
        
        for row in rows:
            room_id, room_number, price_per_night, hotel_id, type_id = row
            room_number = int(room_number)
            # Hole das Hotel
            hotel_sql = "SELECT hotel_id, name, stars, address_id FROM Hotel WHERE hotel_id = ?"
            hotel_row = self.fetchone(hotel_sql, (hotel_id,))
            if hotel_row:
                hotel_id, name, stars, address_id = hotel_row
                # Hole die Adresse
                address_sql = "SELECT address_id, street, city, zip_code FROM Address WHERE address_id = ?"
                address_row = self.fetchone(address_sql, (address_id,))
                if address_row:
                    from model.address import Address
                    address = Address(*address_row)
                    hotel = Hotel(hotel_id, name, stars, address)
                    
                    # Hole den Raumtyp
                    room_type_sql = "SELECT type_id, description, max_guests FROM Room_Type WHERE type_id = ?"
                    room_type_row = self.fetchone(room_type_sql, (type_id,))
                    if room_type_row:
                        type_id, description, max_guests = room_type_row
                        room_type = RoomType(type_id, description, max_guests)
                        room = Room(room_id, room_number, price_per_night, hotel, room_type)
                        # Buchungen laden und zuweisen
                        booking_da = BookingDataAccess()
                        bookings = booking_da.read_bookings_by_room(room_id)
                        for booking in bookings:
                            room.add_booking(booking)
                        rooms.append(room)
        
        return rooms

    def read_room_by_id(self, room_id: int) -> Room | None:
        sql = """
        SELECT r.room_id, r.room_number, r.price_per_night, r.hotel_id, r.type_id
        FROM Room r
        WHERE r.room_id = ?
        """
        row = self.fetchone(sql, (room_id,))
        if not row:
            return None
        room_id, room_number, price_per_night, hotel_id, type_id = row
        # Hole das Hotel
        hotel_sql = "SELECT hotel_id, name, stars, address_id FROM Hotel WHERE hotel_id = ?"
        hotel_row = self.fetchone(hotel_sql, (hotel_id,))
        if not hotel_row:
            return None
        hotel_id, name, stars, address_id = hotel_row
        address_sql = "SELECT address_id, street, city, zip_code FROM Address WHERE address_id = ?"
        address_row = self.fetchone(address_sql, (address_id,))
        if not address_row:
            return None
        from model.address import Address
        address = Address(*address_row)
        hotel = Hotel(hotel_id, name, stars, address)
        # Hole den Raumtyp
        room_type_sql = "SELECT type_id, description, max_guests FROM Room_Type WHERE type_id = ?"
        room_type_row = self.fetchone(room_type_sql, (type_id,))
        if not room_type_row:
            return None
        type_id, description, max_guests = room_type_row
        room_type = RoomType(type_id, description, max_guests)
        room = Room(room_id, int(room_number), price_per_night, hotel, room_type)
        # Buchungen laden und zuweisen
        booking_da = BookingDataAccess()
        bookings = booking_da.read_bookings_by_room(room_id)
        for booking in bookings:
            room.add_booking(booking)
        # Facilities laden
        from data_access.facility_data_access import FacilityDataAccess
        facility_da = FacilityDataAccess()
        facilities = facility_da.read_facilities_by_room(room_id)
        for facility in facilities:
            room.add_facility(facility)
        return room

    def delete_room(self, room_id: int) -> None:
        # Zuerst alle Buchungen und ggf. Facilities zum Zimmer löschen (wegen Foreign Keys)
        # (Hier ggf. weitere Lösch-Logik für Facilities/Buchungen ergänzen)
        sql = "DELETE FROM Room WHERE room_id = ?"
        self.execute(sql, (room_id,))

    def create_room(self, hotel_id: int, room_number: int, price_per_night: float, type_id: int) -> int:
        sql = """
        INSERT INTO Room (hotel_id, room_number, price_per_night, type_id)
        VALUES (?, ?, ?, ?)
        """
        params = (hotel_id, room_number, price_per_night, type_id)
        last_id, _ = self.execute(sql, params)
        return int(last_id)
