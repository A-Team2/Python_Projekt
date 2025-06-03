from ui import input_helper

def run(hotel_manager):
    hotels = hotel_manager.get_all_hotels()
    if not hotels:
        print("Keine Hotels im System vorhanden.")
        return

    print("\nAlle Hotels:")
    for i, hotel in enumerate(hotels, start=1):
        print(f" {i}. {hotel.name}, {hotel.address.get_full_address()} ({hotel.stars} Sterne)")

    # Warte auf 'Exit' zum Zurückkehren
    while True:
        user_input = input_helper.input_valid_string("Geben Sie 'Exit' ein, um ins Menü zurückzukehren: ", min_length=2)
        if user_input.strip().lower() == "exit":
            print("Zurück zum Hauptmenü.")
            return
        else:
            print("Bitte geben Sie 'Exit' ein, um ins Menü zurückzukehren.")