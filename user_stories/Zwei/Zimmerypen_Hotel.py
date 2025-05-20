from ui import input_helper
from model.hotel import Hotel

def run(hotel_manager):
    """
    Zeigt die verfügbaren Zimmertypen eines Hotels an.
    """
    hotel = None
    cancel = False

    # 1. Hotel auswählen
    while not hotel and not cancel:
        try:
            hotel_name = input_helper.input_valid_string("Hotelname eingeben: ", min_length=2, normalize_func=lambda s: s.strip().capitalize())
            hotel = hotel_manager.get_hotel_by_name(hotel_name)
            if not hotel:
                print(f"Hotel '{hotel_name}' nicht gefunden.")
                hotel = None
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