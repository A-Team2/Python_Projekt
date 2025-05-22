import model
import data_access
from model.hotel import Hotel
from model.address import Address
from datetime import date



class HotelManager:
    def __init__(self):
        self.__hotel_da = data_access.HotelDataAccess()

    def get_hotels_by_city(self, city: str) -> list[Hotel]:
        #Gibt alle Hotels in einer bestimmten Stadt zurück.
        
        if not city or not isinstance(city, str):
            raise ValueError("City must be a non-empty string.")
        return self.__hotel_da.read_hotels_by_city(city.strip())

    def get_hotels_by_city_and_min_stars(self, city: str, min_stars: int) -> list[Hotel]:
        #Gibt alle Hotels in der Stadt zurück, deren Sterne >= min_stars sind.
        
        hotels_in_city = self.__hotel_da.read_hotels_by_city(city.strip())
        return [h for h in hotels_in_city if h.stars >= min_stars]

    def get_hotels_by_city_and_guests(self, city: str, guests: int) -> list[Hotel]:
        """
        Gibt Hotels in der Stadt zurück, die mindestens ein Zimmer mit ausreichender Gästeanzahl anbieten.
        """
        hotels_in_city = self.__hotel_da.read_hotels_by_city(city.strip())
        matching_hotels = []

        for hotel in hotels_in_city:
            for room in hotel.rooms:
                if room.room_type.max_guests >= guests:
                    matching_hotels.append(hotel)
                    break  # Nur ein passendes Zimmer reicht aus

        return matching_hotels

    def get_hotels_by_city_and_availability(
        self,
        city: str,
        check_in: date,
        check_out: date
    ) -> list[Hotel]:
        """
        Gibt alle Hotels in der Stadt zurück, die im gewünschten Zeitraum
        mindestens ein verfügbares Zimmer haben.
        """
        hotels_in_city = self.__hotel_da.read_hotels_by_city(city.strip())
        matching_hotels = []

        for hotel in hotels_in_city:
            for room in hotel.rooms:
                if room.is_available(check_in, check_out):
                    matching_hotels.append(hotel)
                    break  # Nur ein freies Zimmer reicht

        return matching_hotels

    def get_hotels_by_all_criteria(
        self,
        city: str,
        min_stars: int,
        guest_count: int,
        check_in_date: date,
        check_out_date: date
    ) -> list[Hotel]:
        """
        Gibt Hotels zurück, die alle angegebenen Kriterien erfüllen.
        """
        # Eingabevalidierung
        if not city or not isinstance(city, str):
            raise ValueError("City must be a non-empty string.")
        if not isinstance(min_stars, int) or min_stars < 1 or min_stars > 5:
            raise ValueError("Min_stars must be an integer between 1 and 5.")
        if not isinstance(guest_count, int) or guest_count < 1:
            raise ValueError("Guest_count must be a positive integer.")
        if not isinstance(check_in_date, date):
            raise ValueError("Check_in_date must be a date object.")
        if not isinstance(check_out_date, date):
            raise ValueError("Check_out_date must be a date object.")
        if check_out_date <= check_in_date:
            raise ValueError("Check_out_date must be after Check_in_date.")

        # Delegation an den Data Access Layer
        return self.__hotel_da.read_hotels_by_all_criteria(
            city.strip(),
            min_stars,
            guest_count,
            check_in_date,
            check_out_date
        )

    def get_hotel_by_name(self, name: str) -> Hotel | None:
        """
        Gibt ein Hotel anhand seines Namens zurück.
        """
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string.")
        return self.__hotel_da.read_hotel_by_name(name.strip())
    
    def read_hotel_by_id(self, hotel_id: int) -> Hotel | None:
        #Gibt ein Hotel anhand seiner Datenbank-ID zurück.
        
        # Eingabevalidierung
        if not isinstance(hotel_id, int) or hotel_id < 1:
            raise ValueError("hotel_id must be a positive integer.")
        # Delegation an den Data‐Access‐Layer
        return self.__hotel_da.read_hotel_by_id(hotel_id)

    def create_hotel(self, name: str, stars: int, address: Address) -> Hotel:
        # Validierung
        if not name or not isinstance(name, str) or len(name) < 3:
            raise ValueError("Hotelname muss mindestens 3 Zeichen lang sein.")
        if not isinstance(stars, int) or not (1 <= stars <= 5):
            raise ValueError("Sterne müssen zwischen 1 und 5 liegen.")
        if address is None or not isinstance(address, Address):
            raise ValueError("Adresse muss ein Address-Objekt sein.")
        # Insert in DB, liefert neue hotel_id
        new_id = self.__hotel_da.insert_hotel(name, stars, address.address_id)
        # Frisch aus der DB laden und zurückgeben
        hotel = self.__hotel_da.read_hotel_by_id(new_id)
        if hotel is None:
            raise RuntimeError(f"Hotel mit id {new_id} konnte nicht geladen werden.")
        return hotel

    def delete_hotel(self, hotel_id: int) -> None:
        if not isinstance(hotel_id, int) or hotel_id < 1:
            raise ValueError("hotel_id muss eine positive ganze Zahl sein.")
        self.__hotel_da.delete_hotel(hotel_id)

    def update_hotel(self, hotel_id: int, name: str, stars: int, address) -> None:
        if not isinstance(hotel_id, int) or hotel_id < 1:
            raise ValueError("hotel_id muss eine positive ganze Zahl sein.")
        if not name or not isinstance(name, str) or len(name) < 3:
            raise ValueError("Hotelname muss mindestens 3 Zeichen lang sein.")
        if not isinstance(stars, int) or not (1 <= stars <= 5):
            raise ValueError("Sterne müssen zwischen 1 und 5 liegen.")
        if address is None:
            raise ValueError("Adresse darf nicht None sein.")
        self.__hotel_da.update_hotel(hotel_id, name, stars, address)