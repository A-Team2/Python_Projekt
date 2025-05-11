import os
import sqlite3
from contextlib import closing
from typing import Optional


class BaseDataAccess:
    def __init__(self, db_connection_str: Optional[str] = None):
        # Immer die working_hotel.db verwenden
        self.__db_connection_str = "database/working_hotel.db"

    def _connect(self):
        # Öffnet die Verbindung mit aktivem Datums-Support
        return sqlite3.connect(self.__db_connection_str, detect_types=sqlite3.PARSE_DECLTYPES)

    def fetchone(self, sql: str, params: tuple = ()):
        with closing(self._connect()) as conn:
            try:
                cur = conn.cursor()
                cur.execute(sql, params)
                result = cur.fetchone()
            except sqlite3.Error as e:
                conn.rollback()
                raise e
            finally:
                cur.close()
        return result

    def fetchall(self, sql: str, params: tuple = ()):
        with closing(self._connect()) as conn:
            try:
                cur = conn.cursor()
                cur.execute(sql, params)
                result = cur.fetchall()
            except sqlite3.Error as e:
                conn.rollback()
                raise e
            finally:
                cur.close()
        return result

    def execute(self, sql: str, params: tuple = ()) -> tuple[int, int]:
        with closing(self._connect()) as conn:
            try:
                cur = conn.cursor()
                cur.execute(sql, params)
            except sqlite3.Error as e:
                conn.rollback()
                raise e
            else:
                conn.commit()
            finally:
                cur.close()
        return cur.lastrowid, cur.rowcount
