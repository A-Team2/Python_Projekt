from ui import input_helper
from business_logic.hotel_manager import HotelManager

def run(hotel_manager: HotelManager):
    print("=== Hotelinformationen aktualisieren ===")
    while True:
        # 1. Stadt abfragen und Hotel auswählen
        city = input_helper.input_valid_string("In welcher Stadt möchten Sie ein Hotel aktualisieren? ", min_length=2)
        hotels = hotel_manager.get_hotels_by_city(city)
        if not hotels:
            print(f"In {city} sind derzeit keine Hotels verfügbar. Bitte geben Sie eine andere Stadt ein.")
            continue
        print(f"\nHotels in {city}:")
        for i, h in enumerate(hotels, start=1):
            print(f" {i}. {h.name} — {h.address.get_full_address()} ({h.stars} Sterne)")
        idx = input_helper.input_valid_int(
            "Welches Hotel möchten Sie aktualisieren (Nummer): ",
            min_value=1, max_value=len(hotels)
        )
        hotel = hotels[idx-1]

        # 2. Auswahl, was geändert werden soll
        print("\nWas möchten Sie aktualisieren?")
        print("1. Name")
        print("2. Sterne")
        print("3. Adresse")
        print("0. Abbrechen")
        choice = input_helper.input_valid_int("Bitte wählen Sie eine Option (0-3): ", min_value=0, max_value=3)
        if choice == 0:
            print("Vorgang abgebrochen.")
            return

        new_name = hotel.name
        new_stars = hotel.stars
        new_address = hotel.address

        if choice == 1:
            new_name = input_helper.input_valid_string("Neuer Hotelname: ", min_length=3)
        elif choice == 2:
            new_stars = input_helper.input_valid_int("Neue Sterne (1-5): ", min_value=1, max_value=5)
        elif choice == 3:
            street = input_helper.input_valid_string("Neue Straße (mit Hausnummer): ", min_length=3)
            city = input_helper.input_valid_string("Neue Stadt: ", min_length=2)
            zip_code = input_helper.input_valid_string("Neue PLZ: ", min_length=2)
            from model.address import Address
            new_address = Address(hotel.address.address_id, street, city, zip_code)

        # 3. Änderungen speichern?
        confirm = input_helper.input_valid_string(
            "Möchten Sie die Änderungen speichern? (ja/nein): ", min_length=2
        ).strip().lower()
        if confirm != "ja":
            print("Änderungen verworfen.")
        else:
            try:
                hotel_manager.update_hotel(hotel.hotel_id, new_name, new_stars, new_address)
                print("\n✅ Hotel wurde erfolgreich aktualisiert.")
            except Exception as err:
                print("Fehler beim Aktualisieren des Hotels:", err)

        # 4. Noch ein Hotel aktualisieren?
        again = input_helper.input_valid_string(
            "Möchten Sie ein weiteres Hotel aktualisieren? (ja/nein): ", min_length=2
        ).strip().lower()
        if again != "ja":
            print("Vorgang beendet.")
            break 