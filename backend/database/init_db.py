from database.database import Database
from database.schema import SCHEMA


def initialize_database():

    conn = Database.get_connection()

    cursor = conn.cursor()

    for query in SCHEMA:
        cursor.execute(query)

    conn.commit()
    conn.close()

    print("✓ Database initialized successfully.")