from ui import input_helper
from model.hotel import Hotel

def run(hotel_manager):
    """
    Zeigt die verfügbaren Zimmertypen eines Hotels an.
    """
    hotel = None
    cancel = False

    # 1. Stadt abfragen und Hotel auswählen
    while not hotel and not cancel:
        try:
            city = input_helper.input_valid_string("In welcher Stadt möchten Sie ein Hotel auswählen? ", min_length=2)
            hotels = hotel_manager.get_hotels_by_city(city)
            if not hotels:
                print(f"In {city} sind derzeit keine Hotels verfügbar. Bitte geben Sie eine andere Stadt ein.")
                continue
            print(f"\nHotels in {city}:")
            for i, h in enumerate(hotels, start=1):
                print(f" {i}. {h.name} — {h.address.get_full_address()} ({h.stars} Sterne)")
            idx = input_helper.input_valid_int(
                "Wählen Sie ein Hotel (Nummer): ",
                min_value=1, max_value=len(hotels)
            )
            hotel = hotels[idx-1]
        except input_helper.EmptyInputError:
            cancel = True
        except ValueError as err:
            print("Fehler:", err)

    if cancel:
        print("Vorgang abgebrochen.")
        return

    # 2. Zimmertypen anzeigen
    print(f"\nVerfügbare Zimmertypen in {hotel.name}:")
    print("-" * 50)
    
    # Gruppiere Zimmer nach Typ
    room_types = {}
    for room in hotel.rooms:
        room_type = room.room_type
        if room_type not in room_types:
            room_types[room_type] = []
        room_types[room_type].append(room)

    # Zeige Details für jeden Zimmertyp
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
        
        # Zeige Anzahl verfügbarer Zimmer
        print(f"Verfügbare Zimmer: {len(rooms)}")
        print("-" * 50) 