from ui import input_helper
from business_logic.hotel_manager import HotelManager
from business_logic.address_manager import AddressManager
from model.address import Address

def run(hotel_manager: HotelManager):
    print("=== Neues Hotel zum System hinzufügen ===")
    cancel = False

    # 1. Hoteldaten abfragen
    while True:
        try:
            name = input_helper.input_valid_string("Hotelname: ", min_length=3)
            while True:
                try:
                    stars = input_helper.input_valid_int("Sterne (1-5): ", min_value=1, max_value=5)
                    break
                except input_helper.EmptyInputError:
                    print("Vorgang abgebrochen.")
                    return
                except ValueError as err:
                    print("Fehler: Die Anzahl der Sterne muss zwischen 1 und 5 liegen.")
            break
        except input_helper.EmptyInputError:
            print("Vorgang abgebrochen.")
            return
        except ValueError as err:
            print("Fehler:", err)

    # 2. Adressdaten abfragen
    while True:
        try:
            street = input_helper.input_valid_string("Straße (mit Hausnummer): ", min_length=3)
            city = input_helper.input_valid_string("Stadt: ", min_length=2)
            zip_code = input_helper.input_valid_string("PLZ: ", min_length=2)
            break
        except input_helper.EmptyInputError:
            print("Vorgang abgebrochen.")
            return
        except ValueError as err:
            print("Fehler:", err)

    # 3. Adresse anlegen
    address_manager = AddressManager()
    address = Address(0, street, city, zip_code)
    address_id = address_manager.create_address(address)
    address = Address(int(address_id), street, city, zip_code)

    # 4. Hotel anlegen
    try:
        new_hotel = hotel_manager.create_hotel(name, stars, address)
    except Exception as err:
        print("Fehler beim Hinzufügen des Hotels:", err)
        return

    # 5. Bestätigung und Hoteldetails anzeigen (ohne ID)
    print("\n✅ Hotel erfolgreich hinzugefügt!")
    print(f"Name: {new_hotel.name}")
    print(f"Sterne: {new_hotel.stars}")
    print(f"Adresse: {new_hotel.address.street}, {new_hotel.address.zip_code} {new_hotel.address.city}")
