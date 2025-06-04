from business_logic.hotel_manager import HotelManager

def run(hotel_manager: HotelManager):
    hotels = hotel_manager.get_all_hotels()
    if not hotels:
        print("Keine Hotels gefunden.")
    else:
        print("Alle Hotels in der Datenbank:")
        for h in hotels:
            print(f"- {h.name}, {h.address.street}, {h.address.zip_code} {h.address.city} ({h.stars} Sterne)") 