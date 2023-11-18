import os
import time
import sqlite3


class Database:
    DATABASE_PATH = os.path.join("cache", "data.db")

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect_db()
        self.create_table()

    def connect_db(self):
        self.conn = sqlite3.connect(self.DATABASE_PATH)
        self.cursor = self.conn.cursor()

    def disconnect_db(self):
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    server TEXT PRIMARY KEY,
                    response BLOB,
                    response_time REAL,
                    expiration_time REAL
                )
            """)

    def add_entry(self,
                  server: str,
                  response: bytes,
                  response_time: int | float,
                  ttl: int | float,
                  ):
        self.connect_db()
        expiration_time = time.time() + ttl
        self.cursor.execute("""
            INSERT OR REPLACE INTO cache (server, response, response_time, expiration_time) 
            VALUES (?, ?, ?, ?)
        """, (server, response, response_time, expiration_time))
        self.disconnect_db()

    def check_expiration(self):
        self.connect_db()
        current_time = time.time()
        self.cursor.execute("""
            DELETE FROM cache WHERE expiration_time <= ?
        """, (current_time,))
        self.disconnect_db()

    def check_server_exists(self, server: str):
        self.connect_db()
        self.cursor.execute("""
                SELECT EXISTS(SELECT 1 FROM cache WHERE server = ?)
            """, (server,))
        result = self.cursor.fetchone()
        self.disconnect_db()
        return result[0] == 1

    def get_response(self, server: str):
        self.connect_db()
        self.cursor.execute("""
            SELECT response FROM cache WHERE server = ?
        """, (server,))
        response = self.cursor.fetchone()
        self.disconnect_db()
        return response[0] if response else None
