from datetime import datetime
from database.database import Database
from models.conversation import Conversation


class ConversationRepository:

    @staticmethod
    def create():

        conn = Database.get_connection()

        try:

            cursor = conn.cursor()

            cur_date_time = datetime.now().isoformat()

            cursor.execute(
                """
                INSERT INTO conversations(title,created_at,updated_at)
                VALUES (?,?,?)
                """,
                ("New Chat",cur_date_time,cur_date_time)
            )

            conversation_id = cursor.lastrowid

            conn.commit()

            cursor.execute(
                """
                SELECT *
                FROM conversations
                WHERE id = ?
                """,
                (conversation_id,)
            )

            row = cursor.fetchone()

            return Conversation(**dict(row))

        finally:

            conn.close()

    @staticmethod
    def get(conversation_id: int):

        conn = Database.get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM conversations
            WHERE id = ?
            """,
            (conversation_id,)
        )

        row = cursor.fetchone()

        conn.close()

        if row is None:
            return None

        return Conversation(**dict(row))

    @staticmethod
    def get_all():

        conn = Database.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM conversations
            ORDER BY updated_at DESC
        """)

        rows = cursor.fetchall()

        conn.close()

        return [
            Conversation(**dict(row))
            for row in rows
        ]
    
    def update_title(conversation_id:int,title:str):
        conn = Database.get_connection()
        
        cursor = conn.cursor()
        
        cursor.execute(
            """
            UPDATE conversations
            SET title = ?
            WHERE id = ?
            """,
            (title,conversation_id)
        )
        conn.commit()
        
        conn.close()
        
        return 