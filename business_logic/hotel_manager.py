import model
import data_access
from model.hotel import Hotel
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

    def get_hotel_by_name(self, name: str) -> Hotel | None:
        """
        Gibt ein Hotel anhand seines Namens zurück.
        """
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string.")
        return self.__hotel_da.read_hotel_by_name(name.strip())