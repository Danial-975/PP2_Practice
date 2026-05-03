import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG

class DatabaseManager:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.conn.autocommit = True
        except Exception as e:
            print(f"Error with connection to database: {e}")
            exit()

    def execute_query(self, query, params=None, fetch=True):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            if fetch and cur.description:
                return cur.fetchall()
            return None

    def call_proc(self, proc_name, params):
        with self.conn.cursor() as cur:
            placeholders = ",".join(["%s"] * len(params))
            query = f"CALL {proc_name}({placeholders})"
            cur.execute(query, params)