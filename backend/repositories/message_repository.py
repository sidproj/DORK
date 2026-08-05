from datetime import datetime
from database.database import Database
from models.message import Message


class MessageRepository:

    @staticmethod
    def create(
        conversation_id: int,
        role: str,
        content: str,
    ):

        conn = Database.get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO messages(
                conversation_id,
                role,
                content
            )
            VALUES (?, ?, ?)
            """,
            (
                conversation_id,
                role,
                content,
            ),
        )
        conn.commit()
        
        message_id = cursor.lastrowid
        
        # update conversation when new messages are generated
        cursor.execute(
            """
            UPDATE conversations 
            SET updated_at = ?
            WHERE id = ?
            """,
            (
                datetime.now().isoformat(),
                conversation_id
            )
        )
        
        conn.commit()

        cursor.execute(
            """
            SELECT *
            FROM messages
            WHERE id = ?
            """,
            (message_id,),
        )

        row = cursor.fetchone()

        conn.close()

        return Message(**dict(row))

    @staticmethod
    def get_by_conversation(
        conversation_id: int
    ):

        conn = Database.get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id
            """,
            (conversation_id,)
        )

        rows = cursor.fetchall()

        conn.close()

        return [
            Message(**dict(row))
            for row in rows
        ]