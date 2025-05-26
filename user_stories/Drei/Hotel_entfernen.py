from ui import input_helper
from business_logic.hotel_manager import HotelManager

def run(hotel_manager: HotelManager):
    print("=== Hotel aus dem System entfernen ===")
    # 1. Stadt abfragen und Hotel auswählen
    while True:
        city = input_helper.input_valid_string("In welcher Stadt möchten Sie ein Hotel entfernen? ", min_length=2)
        hotels = hotel_manager.get_hotels_by_city(city)
        if not hotels:
            print(f"In {city} sind derzeit keine Hotels verfügbar. Bitte geben Sie eine andere Stadt ein.")
            continue
        print(f"\nHotels in {city}:")
        for i, h in enumerate(hotels, start=1):
            print(f" {i}. {h.name} — {h.address.get_full_address()} ({h.stars} Sterne)")
        idx = input_helper.input_valid_int(
            "Welches Hotel möchten Sie entfernen (Nummer): ",
            min_value=1, max_value=len(hotels)
        )
        hotel = hotels[idx-1]
        break

    # 2. Bestätigung
    confirm = input_helper.input_valid_string(
        f"Sind Sie sicher, dass Sie das Hotel '{hotel.name}' entfernen möchten? (ja/nein): ",
        min_length=2
    ).strip().lower()
    if confirm != "ja":
        print("Vorgang abgebrochen.")
        return

    # 3. Hotel entfernen
    try:
        hotel_manager.delete_hotel(hotel.hotel_id)
        print(f"\n✅ Hotel '{hotel.name}' wurde erfolgreich entfernt.")
    except Exception as err:
        print("Fehler beim Entfernen des Hotels:", err)
