import psycopg2
from psycopg2.extras import Json
from .config import Config

class TimescaleDB:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            dbname=Config.DB_NAME
        )
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS message_exchange (
            message_uuid UUID PRIMARY KEY,
            origin_ts TIMESTAMPTZ,
            ack_ts TIMESTAMPTZ,
            message_data JSONB,
            source_subject_id TEXT,
            destination_subject_ids TEXT[],
            topic TEXT,
            message_type TEXT,
            message_metadata JSONB
        );
        """
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()

    def batch_insert(self, messages):
        query = """
        INSERT INTO message_exchange (
            message_uuid, origin_ts, ack_ts, message_data, 
            source_subject_id, destination_subject_ids, topic, 
            message_type, message_metadata
        ) VALUES %s
        """
        with self.conn.cursor() as cur:
            psycopg2.extras.execute_values(cur, query, messages)
            self.conn.commit()
