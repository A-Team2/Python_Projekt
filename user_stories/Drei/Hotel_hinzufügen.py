from ui import input_helper
from business_logic.hotel_manager import HotelManager
from business_logic.address_manager import AddressManager
from model.address import Address
from ui.validation_helper import valid_street

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
            print(err)

    # 2. Adressdaten abfragen
    # Straße und Hausnummer in eigener Schleife
    while True:
        try:
            street_input = input_helper.input_valid_string("Strasse und Hausnummer (z.B. Sonnfeldweg 12): ", min_length=3)
            parts = street_input.strip().split()
            if len(parts) < 2:
                print("Fehler: Bitte geben Sie Strasse und Hausnummer an (z.B. Sonnfeldweg 12).")
                continue
            street = " ".join(parts[:-1])
            house_number = parts[-1]
            if len(street.replace(' ', '')) < 3:
                print("Fehler: Der Strassenname muss mindestens 3 Buchstaben lang sein.")
                continue
            street_full = f"{street} {house_number}"
            break
        except input_helper.EmptyInputError:
            print("Vorgang abgebrochen.")
            return
        except ValueError as err:
            print(err)

    # Stadt in eigener Schleife
    while True:
        try:
            city = input_helper.input_valid_string("Stadt: ", min_length=3)
            if len(city.strip()) < 3:
                print("Eingabe zu kurz. Bitte mindestens 3 Zeichen für die Stadt eingeben.")
                continue
            break
        except input_helper.EmptyInputError:
            print("Vorgang abgebrochen.")
            return
        except ValueError as err:
            print(err)

    # PLZ in eigener Schleife
    while True:
        try:
            zip_code = input_helper.input_valid_string("PLZ: ", min_length=3)
            if len(zip_code) < 3:
                print("Eingabe zu kurz. Bitte mindestens 3 Zeichen eingeben.")
                continue
            break
        except input_helper.EmptyInputError:
            print("Vorgang abgebrochen.")
            return
        except ValueError as err:
            print(err)

    # 3. Adresse anlegen
    address_manager = AddressManager()
    address = Address(0, street_full, city, zip_code)
    address_id = address_manager.create_address(address)
    address = Address(int(address_id), street_full, city, zip_code)

    # 4. Hotel anlegen
    try:
        new_hotel = hotel_manager.create_hotel(name, stars, address)
    except Exception as err:
        print("Fehler beim Hinzufügen des Hotels:", err)
        return

    # 5. Bestätigung und Hoteldetails anzeigen (ohne ID)
    print("\nHotel erfolgreich hinzugefügt!")
    print(f"Name: {new_hotel.name}")
    print(f"Sterne: {new_hotel.stars}")
    print(f"Adresse: {new_hotel.address.street}, {new_hotel.address.zip_code} {new_hotel.address.city}")
