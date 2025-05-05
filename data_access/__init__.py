from datetime import date, datetime
import sqlite3

from .guest_data_access import GuestDataAccess
from .address_data_access import AddressDataAccess
from .hotel_data_access import HotelDataAccess
from .room_data_access import RoomDataAccess
from .room_type_data_access import RoomTypeDataAccess
from .facility_data_access import FacilityDataAccess
from .booking_data_access import BookingDataAccess
from .invoice_data_access import InvoiceDataAccess

# Adapter: Date → String
def date_to_db(d: date) -> str:
    return d.isoformat()

# Konverter: String (aus DB) → Date
def db_to_date(s: str) -> date:
    return datetime.strptime(s.decode(), "%Y-%m-%d").date()

# Registrierung der Konvertierung bei sqlite
sqlite3.register_adapter(date, date_to_db)
sqlite3.register_converter("DATE", db_to_date)