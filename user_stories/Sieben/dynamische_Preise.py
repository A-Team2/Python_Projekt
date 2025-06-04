import ui.input_helper as input_helper
from business_logic.hotel_manager import HotelManager
from business_logic.pricing_manager import PricingManager
from datetime import datetime, timedelta

def run(hotel_manager: HotelManager):
    # Stadt abfragen
    while True:
        try:
            city = input_helper.input_valid_string("In welcher Stadt möchten sie ein Zimmer buchen: ", min_length=2)
            break
        except Exception as err:
            print(f"Fehler: {err}")

    # Hotels in der Stadt holen
    hotels = hotel_manager.get_hotels_by_city(city)
    if not hotels:
        print(f"Keine Hotels in {city} gefunden.")
        return

    # Hotel auswählen
    while True:
        for i, h in enumerate(hotels, start=1):
            print(f" {i}. {h.name} ({h.stars} Sterne)")
        try:
            choice = input_helper.input_valid_int(
                f"Wählen Sie ein Hotel (1–{len(hotels)}): ",
                min_value=1,
                max_value=len(hotels)
            )
            hotel = hotels[choice - 1]
            break
        except Exception as err:
            print(f"Fehler: {err}")

    # Zimmer und Preisstruktur anzeigen
    pm = PricingManager()
    print(f"\nZimmer und Preisinformationen im Hotel «{hotel.name}»:\n")
    for i, r in enumerate(hotel.rooms, start=1):
        zimmertyp = getattr(r, 'room_type', None)
        zimmertyp_str = zimmertyp.description if zimmertyp and hasattr(zimmertyp, 'description') else "?"
        max_personen = zimmertyp.max_guests if zimmertyp and hasattr(zimmertyp, 'max_guests') else "?"
        print(f" {i}. Zimmer {r.room_number} | Typ: {zimmertyp_str} | max. Personen: {max_personen}")
        saison_monate = pm.get_season_months(r.room_id) if hasattr(pm, 'get_season_months') else [6,7,8]
        saison_preis = pm.get_season_price(r.room_id) if hasattr(pm, 'get_season_price') else r.price_per_night * 1.2
        normal_preis = r.price_per_night
        saison_monate_str = ', '.join([datetime(2000, m, 1).strftime('%B') for m in saison_monate])
        # Übersetze Monatsnamen ins Deutsche
        monate_de = {
            'January': 'Januar', 'February': 'Februar', 'March': 'März', 'April': 'April', 'May': 'Mai', 'June': 'Juni',
            'July': 'Juli', 'August': 'August', 'September': 'September', 'October': 'Oktober', 'November': 'November', 'December': 'Dezember'
        }
        saison_monate_str = ', '.join([monate_de[datetime(2000, m, 1).strftime('%B')] for m in saison_monate])
        print(f"    - Normalpreis: {normal_preis:.2f} CHF/Nacht")
        print(f"    - Saisonpreis ({saison_monate_str}): {saison_preis:.2f} CHF/Nacht")

    # Zimmer auswählen
    while True:
        try:
            choice = input_helper.input_valid_int(
                f"Wählen Sie ein Zimmer (1–{len(hotel.rooms)}): ",
                min_value=1,
                max_value=len(hotel.rooms)
            )
            room = hotel.rooms[choice - 1]
            break
        except Exception as err:
            print(f"Fehler: {err}")

    # Check-in und Check-out abfragen
    while True:
        try:
            s = input_helper.input_valid_string("Check-in (YYYY-MM-DD): ", min_length=10)
            check_in = datetime.strptime(s, "%Y-%m-%d").date()
            break
        except Exception as err:
            print(f"Ungültiges Datum: {err}")
    while True:
        try:
            s = input_helper.input_valid_string("Check-out (YYYY-MM-DD): ", min_length=10)
            check_out = datetime.strptime(s, "%Y-%m-%d").date()
            if check_out <= check_in:
                print("Check-out muss nach Check-in liegen.")
                continue
            break
        except Exception as err:
            print(f"Ungültiges Datum: {err}")

    # Gesamtpreis berechnen (zeige Aufschlüsselung nur, wenn beide Preistypen vorkommen)
    saison_monate = pm.get_season_months(room.room_id) if hasattr(pm, 'get_season_months') else [6,7,8]
    saison_preis = pm.get_season_price(room.room_id) if hasattr(pm, 'get_season_price') else room.price_per_night * 1.2
    normal_preis = room.price_per_night
    nights = (check_out - check_in).days
    saison_naechte = 0
    nebensaison_naechte = 0
    for i in range(nights):
        tag = check_in + timedelta(days=i)
        if tag.month in saison_monate:
            saison_naechte += 1
        else:
            nebensaison_naechte += 1
    total = saison_naechte * saison_preis + nebensaison_naechte * normal_preis
    saison_monate_str = ', '.join([datetime(2000, m, 1).strftime('%B') for m in saison_monate])
    # Übersetze Monatsnamen ins Deutsche
    monate_de = {
        'January': 'Januar', 'February': 'Februar', 'March': 'März', 'April': 'April', 'May': 'Mai', 'June': 'Juni',
        'July': 'Juli', 'August': 'August', 'September': 'September', 'October': 'Oktober', 'November': 'November', 'December': 'Dezember'
    }
    saison_monate_str = ', '.join([monate_de[datetime(2000, m, 1).strftime('%B')] for m in saison_monate])
    if saison_naechte > 0 and nebensaison_naechte > 0:
        print(f"\nPreisaufschlüsselung für den gewählten Zeitraum:")
        print(f"  - {saison_naechte} Nacht/Nächte zum Saisonpreis ({saison_preis:.2f} CHF, Monate: {saison_monate_str}): {saison_naechte * saison_preis:.2f} CHF")
        print(f"  - {nebensaison_naechte} Nacht/Nächte zum Normalpreis ({normal_preis:.2f} CHF): {nebensaison_naechte * normal_preis:.2f} CHF")
    print(f"\nGesamtpreis für {nights} Nacht(en) in Zimmer {room.room_number}: {total:.2f} CHF")