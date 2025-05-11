# run.py
import os
import shutil

# 1. Umgebung vorbereiten
source = "database/hotel_reservation_sample.db"
db_file = "database/working_hotel.db"
shutil.copyfile(source, db_file)  # immer mit frischer Kopie starten
os.environ["DB_FILE"] = db_file   # Pfad für BaseDataAccess

# 2. Module importieren
import model
import data_access
import business_logic
import ui.input_helper as input_helper

# 3. Manager initialisieren
from business_logic.hotel_manager import HotelManager

hotel_manager = HotelManager()

# andere Manager bei Bedarf...

# 4. User Stories starten (Beispiel)
print("🏨 Hotel in Stadt anzeigen (US 1.1)")
from user_stories import Hotel_in_Stadt
Hotel_in_Stadt.run(hotel_manager)
