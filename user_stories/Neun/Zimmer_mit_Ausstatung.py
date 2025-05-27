from ui import input_helper
from business_logic.hotel_manager import HotelManager

def run(hotel_manager: HotelManager):
    print("=== Zimmer mit Ausstattung anzeigen ===")
    
    # 1. Stadt abfragen und Hotel auswählen
    while True:
        city = input_helper.input_valid_string("In welcher Stadt möchten Sie die Zimmerausstattung sehen? ", min_length=2)
        hotels = hotel_manager.get_hotels_by_city(city)
        if not hotels:
            print(f"In {city} sind derzeit keine Hotels verfügbar. Bitte geben Sie eine andere Stadt ein.")
            continue
            
        print(f"\nHotels in {city}:")
        for i, h in enumerate(hotels, start=1):
            print(f" {i}. {h.name} — {h.address.get_full_address()} ({h.stars} Sterne)")
            
        idx = input_helper.input_valid_int(
            "Welches Hotel möchten Sie auswählen (Nummer): ",
            min_value=1, max_value=len(hotels)
        )
        hotel = hotels[idx-1]
        break

    # 2. Zimmer nach Typen gruppieren und Ausstattung anzeigen
    room_types = {}
    for room in hotel.rooms:
        if room.room_type not in room_types:
            room_types[room.room_type] = []
        room_types[room.room_type].append(room)

    print(f"\nZimmerausstattung im Hotel «{hotel.name}»:")
    print("=" * 50)
    
    for room_type, rooms in room_types.items():
        print(f"\n{room_type.description}:")
        print(f"Maximale Gäste: {room_type.max_guests}")
        
        # Berechne Durchschnittspreis für diesen Zimmertyp
        avg_price = sum(room.price_per_night for room in rooms) / len(rooms)
        print(f"Durchschnittspreis: {avg_price:.2f} CHF/Nacht")
        
        # Zeige verfügbare Ausstattung
        if rooms:
            facilities = set()
            for room in rooms:
                facilities.update(facility.facility_name for facility in room.facilities)
            if facilities:
                print("Ausstattung:", ", ".join(sorted(facilities)))
            else:
                print("Keine spezielle Ausstattung verfügbar")
        
        # Zeige Anzahl verfügbarer Zimmer
        print(f"Verfügbare Zimmer: {len(rooms)}")
        print("-" * 50)
