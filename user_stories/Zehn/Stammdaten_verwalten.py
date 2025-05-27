from ui import input_helper
from business_logic.hotel_manager import HotelManager
from model.hotel import Hotel
from model.room_type import RoomType
from model.facilities import Facilities
from model.room import Room

def show_hotel_menu(hotel: Hotel):
    print(f"\n=== Stammdaten verwalten für {hotel.name} ===")
    print("1. Zimmertypen bearbeiten")
    print("2. Einrichtungen bearbeiten")
    print("3. Preise bearbeiten")
    print("4. Beschreibung bearbeiten")
    print("5. Adresse bearbeiten")
    print("6. Sterne bearbeiten")
    print("0. Zurück zur Hotelauswahl")
    print("================================")

def edit_room_types(hotel: Hotel) -> bool:
    print("\n=== Zimmertypen bearbeiten ===")
    room_types = hotel.get_room_types()
    
    if not room_types:
        print("Keine Zimmertypen vorhanden.")
        return False
        
    print("\nVorhandene Zimmertypen:")
    for i, rt in enumerate(room_types, 1):
        print(f"{i}. {rt.description} - Max. Gäste: {rt.max_guests}")
    
    idx = input_helper.input_valid_int(
        "Welchen Zimmertyp möchten Sie bearbeiten? (0 für zurück): ",
        min_value=0, max_value=len(room_types)
    )
    
    if idx == 0:
        return False
        
    room_type = room_types[idx-1]
    
    print("\nWas möchten Sie ändern?")
    print("1. Beschreibung")
    print("2. Maximale Gästeanzahl")
    print("0. Zurück")
    
    choice = input_helper.input_valid_int(
        "Ihre Wahl: ",
        min_value=0, max_value=2
    )
    
    if choice == 0:
        return False
        
    if choice == 1:
        new_desc = input_helper.input_valid_string(
            "Neue Beschreibung: ",
            min_length=3
        )
        room_type.description = new_desc
    elif choice == 2:
        new_max = input_helper.input_valid_int(
            "Neue maximale Gästeanzahl: ",
            min_value=1, max_value=10
        )
        room_type.max_guests = new_max
        
    return True

def edit_facilities(hotel: Hotel) -> bool:
    print("\n=== Einrichtungen bearbeiten ===")
    all_facilities = hotel.get_all_facilities()
    
    if not all_facilities:
        print("Keine Einrichtungen vorhanden.")
        return False
        
    print("\nVorhandene Einrichtungen:")
    for i, fac in enumerate(all_facilities, 1):
        print(f"{i}. {fac.facility_name}")
    
    print("\nWas möchten Sie tun?")
    print("1. Neue Einrichtung hinzufügen")
    print("2. Einrichtung entfernen")
    print("0. Zurück")
    
    choice = input_helper.input_valid_int(
        "Ihre Wahl: ",
        min_value=0, max_value=2
    )
    
    if choice == 0:
        return False
        
    if choice == 1:
        new_facility = input_helper.input_valid_string(
            "Name der neuen Einrichtung: ",
            min_length=3
        )
        hotel.add_facility(Facility(new_facility))
    elif choice == 2:
        idx = input_helper.input_valid_int(
            "Welche Einrichtung soll entfernt werden? (0 für zurück): ",
            min_value=0, max_value=len(all_facilities)
        )
        if idx > 0:
            hotel.remove_facility(all_facilities[idx-1])
            
    return True

def edit_prices(hotel: Hotel) -> bool:
    print("\n=== Preise bearbeiten ===")
    rooms = hotel.rooms
    
    if not rooms:
        print("Keine Zimmer vorhanden.")
        return False
        
    print("\nVorhandene Zimmer:")
    for i, room in enumerate(rooms, 1):
        print(f"{i}. {room.room_type.description} - {room.price_per_night} CHF/Nacht")
    
    idx = input_helper.input_valid_int(
        "Welches Zimmer möchten Sie bearbeiten? (0 für zurück): ",
        min_value=0, max_value=len(rooms)
    )
    
    if idx == 0:
        return False
        
    room = rooms[idx-1]
    new_price = input_helper.input_valid_float(
        "Neuer Preis pro Nacht (CHF): ",
        min_value=0.0
    )
    room.price_per_night = new_price
    
    return True

def edit_description(hotel: Hotel) -> bool:
    print("\n=== Beschreibung bearbeiten ===")
    while True:
        try:
            new_desc = input_helper.input_valid_string(
                "Neue Beschreibung: ",
                min_length=10
            )
            break
        except ValueError:
            print("Fehler: Die Beschreibung muss mindestens 10 Zeichen lang sein. Bitte erneut eingeben.")
    hotel.description = new_desc
    return True

def edit_address(hotel: Hotel) -> bool:
    print("\n=== Adresse bearbeiten ===")
    street = input_helper.input_valid_string("Straße: ", min_length=3)
    house_number = input_helper.input_valid_string("Hausnummer: ", min_length=1)
    zip_code = input_helper.input_valid_string("PLZ: ", min_length=4)
    city = input_helper.input_valid_string("Stadt: ", min_length=2)
    
    hotel.address.street = street
    hotel.address.house_number = house_number
    hotel.address.zip_code = zip_code
    hotel.address.city = city
    
    return True

def edit_stars(hotel: Hotel) -> bool:
    print("\n=== Sterne bearbeiten ===")
    new_stars = input_helper.input_valid_int(
        "Neue Anzahl Sterne (1-5): ",
        min_value=1, max_value=5
    )
    hotel.stars = new_stars
    return True

def run(hotel_manager: HotelManager):
    print("=== Stammdaten verwalten ===")
    
    while True:
        print("\nMöchten Sie:")
        print("1. Alle Hotels anzeigen")
        print("2. Nach Stadt filtern")
        print("0. Beenden")
        
        choice = input_helper.input_valid_int(
            "Ihre Wahl: ",
            min_value=0, max_value=2
        )
        
        if choice == 0:
            break
            
        if choice == 1:
            hotels = hotel_manager.get_all_hotels()
        else:
            city = input_helper.input_valid_string("Stadt: ", min_length=2)
            hotels = hotel_manager.get_hotels_by_city(city)
            
        if not hotels:
            print("Keine Hotels gefunden.")
            continue
            
        print("\nVerfügbare Hotels:")
        for i, h in enumerate(hotels, 1):
            print(f"{i}. {h.name} - {h.address.get_full_address()} ({h.stars} Sterne)")
            
        idx = input_helper.input_valid_int(
            "Welches Hotel möchten Sie bearbeiten? (0 für zurück): ",
            min_value=0, max_value=len(hotels)
        )
        
        if idx == 0:
            continue
            
        hotel = hotels[idx-1]
        changes_made = False
        
        while True:
            show_hotel_menu(hotel)
            choice = input_helper.input_valid_int(
                "Ihre Wahl: ",
                min_value=0, max_value=6
            )
            
            if choice == 0:
                break
                
            if choice == 1:
                changes_made |= edit_room_types(hotel)
            elif choice == 2:
                changes_made |= edit_facilities(hotel)
            elif choice == 3:
                changes_made |= edit_prices(hotel)
            elif choice == 4:
                changes_made |= edit_description(hotel)
            elif choice == 5:
                changes_made |= edit_address(hotel)
            elif choice == 6:
                changes_made |= edit_stars(hotel)
                
        if changes_made:
            save = input_helper.input_valid_string(
                "Möchten Sie die Änderungen speichern? (j/n): ",
                min_length=1
            ).lower() == 'j'
            
            if save:
                hotel_manager.update_hotel(hotel.hotel_id, hotel.name, hotel.stars, hotel.address)
                print("Änderungen wurden gespeichert.")
            else:
                print("Änderungen wurden verworfen.")
                
        continue_editing = input_helper.input_valid_string(
            "Möchten Sie weitere Stammdaten bearbeiten? (j/n): ",
            min_length=1
        ).lower() == 'j'
        
        if not continue_editing:
            break
