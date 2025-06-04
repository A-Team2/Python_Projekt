from __future__ import annotations
from datetime import date
from model.hotel import Hotel
from model.room_type import RoomType
from model.facilities import Facilities
from model.booking import Booking

class Room:
    """
    Model-Klasse für Zimmer
    """

    def __init__(
        self,
        room_id: int,
        room_number: int,
        price_per_night: float,
        hotel: Hotel,
        room_type: RoomType
    ):
        # Validierung
        if room_id is None or not isinstance(room_id, int):
            raise ValueError("room_id is required and must be int")
        if room_number is None or not isinstance(room_number, int):
            raise ValueError("room_number is required and must be int")
        if price_per_night is None or not isinstance(price_per_night, float):
            raise ValueError("price_per_night is required and must be float")
        if hotel is None or not isinstance(hotel, Hotel):
            raise ValueError("hotel is required and must be Hotel")
        if room_type is None or not isinstance(room_type, RoomType):
            raise ValueError("room_type is required and must be RoomType")

        # private Attribute
        self.__room_id: int = room_id
        self.__room_number: int = room_number
        self.__price_per_night: float = price_per_night
        self.__hotel: Hotel = hotel
        self.__room_type: RoomType = room_type

        # Registriert das Zimmer beim Hotel und setzt im Zimmer die Referenz auf dieses Hotel (bidirektionale Assoziation).
        self.__hotel.add_room(self)

        # Initialisiert die Verknüpfungen zu Einrichtungen und Buchungen.
        self.__facilities: list[Facilities] = []
        self.__bookings: list[Booking] = []

    def __repr__(self) -> str:
        return (
            f"Room(id={self.__room_id!r}, number={self.__room_number!r}, "
            f"price={self.__price_per_night!r}, hotel={self.__hotel!r})"
        )

    @property
    def room_id(self) -> int:
        # Gibt die Zimmer-ID zurück
        return self.__room_id
    

    @property
    def room_number(self) -> int:
        # Gibt die Zimmernummer zurück
        return self.__room_number

    @room_number.setter
    def room_number(self, room_number: int) -> None:
        if room_number is None or not isinstance(room_number, int):
            raise ValueError("room_number must be int")
        self.__room_number = room_number

    @property
    def price_per_night(self) -> float:
        # Gibt den Preis pro Nacht zurück
        return self.__price_per_night

    @price_per_night.setter
    def price_per_night(self, price: float) -> None:
        if price is None or not isinstance(price, float):
            raise ValueError("price_per_night must be float")
        self.__price_per_night = price

    @property
    def hotel(self) -> Hotel:
        # Gibt das zugehörige Hotel zurück
        return self.__hotel

    @hotel.setter
    def hotel(self, hotel: Hotel) -> None:
        if hotel is None or not isinstance(hotel, Hotel):
            raise ValueError("hotel must be a Hotel instance")
        # Entferne alte Relation.
        if self.__hotel is not hotel:
            if self.__hotel is not None:
                self.__hotel.remove_room(self)
            self.__hotel = hotel
            # Füge neue Relation hinzu, falls das Hotel nicht None ist und das Zimmer noch nicht enthalten ist.
            if hotel is not None and self not in hotel.rooms:
                hotel.add_room(self)

    @property
    def room_type(self) -> RoomType:
        # Gibt den Zimmertyp zurück
        return self.__room_type

    @property
    def facilities(self) -> list[Facilities]:
        # Gibt die Liste der Ausstattungen zurück
        # Gibt eine Kopie zurück, um die interne Liste zu schützen.
        return self.__facilities.copy()

    def add_facility(self, facility: Facilities) -> None:
        if not isinstance(facility, Facilities):
            raise ValueError("facility must be a Facilities instance")
        if facility not in self.__facilities:
            self.__facilities.append(facility)

    def remove_facility(self, facility: Facilities) -> None:
        if facility in self.__facilities:
            self.__facilities.remove(facility)

    @property
    def bookings(self) -> list[Booking]:
        # Gibt die Liste der Buchungen zurück
        return self.__bookings.copy()

    def add_booking(self, booking: Booking) -> None:
        if not isinstance(booking, Booking):
            raise ValueError("booking must be a Booking instance")
        if booking not in self.__bookings:
            self.__bookings.append(booking)

    def remove_booking(self, booking: Booking) -> None:
        if booking in self.__bookings:
            self.__bookings.remove(booking)

    def get_room_details(self) -> str:
        # Gibt eine Kurzbeschreibung des Zimmers zurück
        return f"Zimmer {self.__room_number}, Preis: {self.__price_per_night:.2f} CHF/Nacht"

    def is_available(self, check_in: date, check_out: date) -> bool:
        
       # Prüft, ob das Zimmer im angegebenen Zeitraum verfügbar ist.
        
        # Args:
        # check_in: Anreisedatum
        # check_out: Abreisedatum
            
        #Returns:
        #bool: True wenn das Zimmer verfügbar ist, False wenn nicht
        
        if not isinstance(check_in, date) or not isinstance(check_out, date):
            raise ValueError("check_in und check_out müssen vom Typ date sein")
        if check_in >= check_out:
            raise ValueError("check_in muss vor check_out liegen")
            
        # Prüfe alle Buchungen des Zimmers
        for booking in self.__bookings:
            # Wenn sich die Zeiträume überschneiden, ist das Zimmer nicht verfügbar
            if (check_in <= booking.check_out_date and check_out >= booking.check_in_date):
                return False
        return True
    
    @property
    def room_no(self) -> int:
        # Gibt die Zimmernummer für Menschen lesbar zurück
        return self.__room_number