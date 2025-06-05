import ui.input_helper as input_helper
from business_logic.hotel_manager import HotelManager
from business_logic.hotel_manager import HotelManager
from business_logic.booking_manager import BookingManager
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date


def run(hotel_manager: HotelManager):
    print("\n=== Belegungsraten (US 7) ===\n")

    # 1. Stadt abfragen und alle Hotels in dieser Stadt anzeigen
    city = input_helper.input_valid_string("Stadt für Hotelwahl: ")
    hotels = hotel_manager.read_hotels_by_city(city)
    if not hotels:
        print(f"Keine Hotels in «{city}» gefunden.")
        return

    for idx, h in enumerate(hotels, start=1):
        print(f"{idx}. {h.name}")
    choice = input_helper.input_valid_int(f"Hotel wählen (1–{len(hotels)}): ", 1, len(hotels))
    selected_hotel = hotels[choice - 1]

    # 2. Zeitraum abfragen
    start_date = input_helper.input_valid_date("Startdatum (YYYY-MM-DD): ")
    end_date   = input_helper.input_valid_date("Enddatum   (YYYY-MM-DD): ")
    if end_date <= start_date:
        print("Fehler: Enddatum muss nach dem Startdatum liegen.")
        return

    # 3. Alle Räume des gewählten Hotels holen
    hm = HotelManager()
    rooms = hm.get_available_rooms(hotel_id, check_in, check_out)

    # 4. Für jeden Raum: Zimmertyp ermitteln und Buchungen zählen
    booking_manager = BookingManager()
    daten = []

    for room in rooms:
        alle_buchungen = booking_manager.get_bookings_for_room(room.room_id)
        anzahl_in_zeitraum = sum(
            1
            for b in alle_buchungen
            if (not b.is_cancelled)
               and (b.check_in_date >= start_date)
               and (b.check_out_date <= end_date)
        )
        daten.append({
            "Zimmertyp": room.room_type.description,
            "Anzahl Buchungen": anzahl_in_zeitraum
        })

    if not daten:
        print("Keine Räume gefunden oder keine Buchungen im Zeitraum.")
        return

    # 5. DataFrame erzeugen und anzeigen
    df = pd.DataFrame(daten)
    display_dataframe_to_user(
        name="Belegungsraten je Zimmertyp",
        dataframe=df
    )

    # 6. Balkendiagramm mit Matplotlib
    plt.figure(figsize=(8, 5))
    grouped = df.groupby("Zimmertyp")["Anzahl Buchungen"].sum()
    grouped.plot.bar()
    plt.title(f"Belegungsraten: {selected_hotel.name}\n{start_date} bis {end_date}")
    plt.xlabel("Zimmertyp")
    plt.ylabel("Anzahl Buchungen")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()