import sqlite3

def create_connection():
    conn = sqlite3.connect("database/production.db")
    return conn


def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS production_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        machine_id TEXT,
        mass REAL,
        timestamp TEXT,
        UNIQUE(machine_id, timestamp)
    )
    """)

    conn.commit()
    conn.close()

def insert_data(data):
    conn = create_connection()
    cursor = conn.cursor()

    inserted = 0

    for index, row in data.iterrows():
        try:
            cursor.execute("""
            INSERT INTO production_data (machine_id, mass, timestamp)
            VALUES (?, ?, ?)
            """, (row["machine_id"], row["mass"], row["timestamp"]))

            inserted += 1

        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

    return inserted