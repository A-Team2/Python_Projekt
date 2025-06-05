from data_access.base_data_access import BaseDataAccess

class AnalyticsDataAccess(BaseDataAccess):
    """
    DAL-Klasse für Analytics-Abfragen (z. B. Belegungsraten).
    Erbt von BaseDataAccess und implementiert read_occupancy_by_hotel().
    """

    def read_occupancy_by_hotel(self, hotel_id: int) -> list[tuple]:
        """
        SQL-Abfrage, die für ein gegebenes Hotel die Belegungsdaten pro Zimmertyp
        zurückliefert als Liste von Tupeln:
          (type_id, description, total_rooms, booked_rooms, belegung_rate)
        """
        sql = """
            SELECT
                rt.type_id,
                rt.description,
                COUNT(r.room_id) AS total_rooms,
                SUM(CASE WHEN EXISTS (
                    SELECT 1
                    FROM Booking AS b
                    WHERE b.room_id = r.room_id
                      AND b.is_cancelled = 0
                      AND b.check_in_date  < date('now')
                      AND b.check_out_date > date('now')
                ) THEN 1 ELSE 0 END) AS booked_rooms,
                ROUND(
                    CAST(SUM(CASE WHEN EXISTS (
                        SELECT 1
                        FROM Booking AS b2
                        WHERE b2.room_id = r.room_id
                          AND b2.is_cancelled = 0
                          AND b2.check_in_date  < date('now')
                          AND b2.check_out_date > date('now')
                    ) THEN 1 ELSE 0 END) AS REAL) 
                    / COUNT(r.room_id), 2
                ) AS belegung_rate
            FROM
                Room AS r
                JOIN Room_Type AS rt ON r.type_id = rt.type_id
            WHERE
                r.hotel_id = ?
            GROUP BY
                rt.type_id,
                rt.description
            """
        params = (hotel_id,)
        # fetchall() liefert eine Liste von Tupeln
        rows = self.fetchall(sql, params)
        return rows