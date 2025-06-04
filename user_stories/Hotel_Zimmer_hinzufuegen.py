from business_logic.hotel_manager import HotelManager
from model.room import Room
from model.room_type import RoomType
from ui import input_helper
from data_access.room_type_data_access import RoomTypeDataAccess
from data_access.room_data_access import RoomDataAccess

def run(hotel_manager: HotelManager):
    hotels = hotel_manager.get_all_hotels()
    if not hotels:
        print("Keine Hotels gefunden.")
        return
    print("Alle Hotels:")
    for i, h in enumerate(hotels, start=1):
        print(f" {i}. {h.name}, {h.address.street}, {h.address.zip_code} {h.address.city} ({h.stars} Sterne)")
    while True:
        try:
            idx = input_helper.input_valid_int("Zu welchem Hotel möchten Sie ein Zimmer hinzufügen? (Nummer): ", min_value=1, max_value=len(hotels))
            hotel = hotels[idx-1]
            break
        except Exception as err:
            print(f"Fehler: {err}")

    # Zimmertypen anzeigen und auswählen
    room_type_da = RoomTypeDataAccess()
    room_types = room_type_da.read_all_room_types()
    if not room_types:
        print("Keine Zimmertypen vorhanden. Bitte zuerst Zimmertypen anlegen.")
        return
    print("Verfügbare Zimmertypen:")
    for rt in room_types:
        print(f" {rt.room_type_id}: {rt.description} (max. Gäste: {rt.max_guests})")
    while True:
        try:
            type_id = input_helper.input_valid_int("Bitte geben Sie die ID des gewünschten Zimmertyps ein: ", min_value=1)
            room_type = next((rt for rt in room_types if rt.room_type_id == type_id), None)
            if not room_type:
                print("Ungültige Zimmertyp-ID.")
                continue
            break
        except Exception as err:
            print(f"Fehler: {err}")

    # Zimmerdaten abfragen
    while True:
        try:
            room_number = input_helper.input_valid_int("Zimmernummer: ", min_value=1)
            break
        except Exception as err:
            print(f"Fehler: {err}")
    while True:
        try:
            price = float(input_helper.input_valid_string("Preis pro Nacht (CHF): ", min_length=1))
            break
        except Exception as err:
            print(f"Fehler: {err}")
    ausstattung = input_helper.input_valid_string("Ausstattung (Komma-getrennt, z.B. WLAN, TV, Balkon): ", min_length=0)
    facilities = [a.strip() for a in ausstattung.split(",") if a.strip()]

    # Zimmer in der DB anlegen und dann Room-Objekt holen
    room_da = RoomDataAccess()
    try:
        new_room_id = room_da.create_room(hotel.hotel_id, room_number, price, room_type.room_type_id)
        new_room = room_da.read_room_by_id(new_room_id)
        # Ausstattung zuweisen (hier ggf. FacilityDataAccess nutzen, falls vorhanden)
        for f in facilities:
            try:
                new_room.add_facility(f)
            except Exception:
                pass
        hotel.add_room(new_room)
        print(f"Zimmer {room_number} ({room_type.description}) wurde dem Hotel '{hotel.name}' hinzugefügt.")
    except Exception as err:
        print(f"Fehler beim Hinzufügen des Zimmers: {err}")

    # Alle Zimmer im Hotel anzeigen
    print("\nAlle Zimmer im Hotel:")
    for z in hotel.rooms:
        print(f" Zimmer {z.room_number}: {z.room_type.description}, max. Gäste: {z.room_type.max_guests}, Preis: {z.price_per_night} CHF/Nacht") 