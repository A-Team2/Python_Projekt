from ui import input_helper
from datetime import date
from business_logic.pricing_manager import PricingManager

def run():
    print("🧮 Dynamische Preisberechnung für Zimmer")

    pricing_manager = PricingManager()
    cancel = False

    # 1. Zimmer-ID eingeben
    try:
        room_id = input_helper.input_valid_int("Zimmer-ID: ", min_value=1)
    except Exception as e:
        print("Fehler bei Zimmer-ID:", e)
        cancel = True

    # 2. Check-in Datum
    if not cancel:
        try:
            check_in = input_helper.input_valid_date("Check-in Datum (YYYY-MM-DD): ")
        except Exception as e:
            print("Ungültiges Datum:", e)
            cancel = True

    # 3. Check-out Datum
    if not cancel:
        try:
            check_out = input_helper.input_valid_date("Check-out Datum (YYYY-MM-DD): ", compare_date=check_in, compare_type="gt")
        except Exception as e:
            print("Ungültiges Datum:", e)
            cancel = True

    # 4. Gästeanzahl
    if not cancel:
        try:
            guests = input_helper.input_valid_int("Anzahl Gäste (1-10): ", min_value=1, max_value=10)
        except Exception as e:
            print("Ungültige Gästeanzahl:", e)
            cancel = True

    # 5. Preis berechnen
    if not cancel:
        try:
            total_price = pricing_manager.calculate_price(room_id, check_in, check_out, guests)
            print(f"💰 Gesamtpreis für den Aufenthalt: {total_price:.2f} CHF")
        except Exception as e:
            print("Fehler bei Preisberechnung:", e)
