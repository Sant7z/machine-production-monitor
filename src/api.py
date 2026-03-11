from fastapi import FastAPI
import sqlite3

MIN_MASS = 95
MAX_MASS = 105

app = FastAPI()


def get_connection():
    return sqlite3.connect("database/production.db")


@app.get("/")
def home():
    return {"message": "Machine Production Monitor API"}


@app.get("/production")
def get_production_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT machine_id, mass, timestamp FROM production_data")
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "machine_id": row[0],
            "mass": row[1],
            "timestamp": row[2]
        }
        for row in rows
    ]


@app.get("/alerts")
def get_alerts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT machine_id, mass, timestamp
        FROM production_data
        WHERE mass < ? OR mass > ?
    """, (MIN_MASS, MAX_MASS))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "machine_id": row[0],
            "mass": row[1],
            "timestamp": row[2]
        }
        for row in rows
    ]