from ui import input_helper
from business_logic.hotel_manager import HotelManager
from collections import defaultdict

def run(hotel_manager: HotelManager):
    print("=== Zimmer mit Ausstattung anzeigen ===")
    
    # 1. Stadt abfragen und Hotel auswählen
    while True:
        # Stadt-Eingabe in Loop mit Fehlerbehandlung
        while True:
            try:
                city = input_helper.input_valid_string("In welcher Stadt möchten Sie die Zimmerausstattung sehen? ", min_length=2)
                break
            except Exception as err:
                print(f"Fehler: {err}")
        hotels = hotel_manager.get_hotels_by_city(city)
        if not hotels:
            print(f"In {city} sind derzeit keine Hotels verfügbar. Bitte geben Sie eine andere Stadt ein.")
            continue
        print(f"\nHotels in {city}:")
        for i, h in enumerate(hotels, start=1):
            print(f" {i}. {h.name} — {h.address.get_full_address()} ({h.stars} Sterne)")
        # Hotelauswahl in Loop mit Fehlerbehandlung
        while True:
            try:
                idx = input_helper.input_valid_int(
                    "Welches Hotel möchten Sie auswählen (Nummer): ",
                    min_value=1, max_value=len(hotels)
                )
                hotel = hotels[idx-1]
                break
            except Exception as err:
                print(f"Fehler: {err}")
        break

    # 2. Zimmer nach Typ, max. Gäste und Preis gruppieren und Ausstattung anzeigen
    grouped = defaultdict(list)
    for room in hotel.rooms:
        key = (room.room_type.description, room.room_type.max_guests, room.price_per_night)
        grouped[key].append(room)

    print(f"\nZimmerausstattung im Hotel «{hotel.name}»:\n" + "=" * 50)
    for (desc, max_guests, price), rooms in grouped.items():
        if len(rooms) == 1:
            room = rooms[0]
            print(f"\n{desc} (Zimmer {room.room_number}):")
            print(f"Maximale Gäste: {max_guests}")
            print(f"Preis: {price:.2f} CHF/Nacht")
            facilities = set(facility.facility_name for facility in room.facilities)
            if facilities:
                print("Ausstattung:", ", ".join(sorted(facilities)))
            else:
                print("Keine spezielle Ausstattung verfügbar")
            print("-" * 50)
        else:
            print(f"\n{desc}:")
            print(f"Maximale Gäste: {max_guests}")
            print(f"Preis: {price:.2f} CHF/Nacht")
            facilities = set()
            for room in rooms:
                facilities.update(facility.facility_name for facility in room.facilities)
            if facilities:
                print("Ausstattung:", ", ".join(sorted(facilities)))
            else:
                print("Keine spezielle Ausstattung verfügbar")
            print(f"Verfügbare Zimmer: {len(rooms)} (Zimmernummern: {', '.join(str(r.room_number) for r in rooms)})")
            print("-" * 50)
