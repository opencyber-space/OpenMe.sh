from .db import TimescaleDB

class ReadController:
    def __init__(self):
        self.db = TimescaleDB()

    def get_message_by_uuid(self, message_uuid):
        query = "SELECT * FROM message_exchange WHERE message_uuid = %s"
        with self.db.conn.cursor() as cur:
            cur.execute(query, (message_uuid,))
            return cur.fetchone()

    def get_messages_by_subject(self, subject_id):
        query = "SELECT * FROM message_exchange WHERE source_subject_id = %s OR %s = ANY(destination_subject_ids)"
        with self.db.conn.cursor() as cur:
            cur.execute(query, (subject_id, subject_id))
            return cur.fetchall()
