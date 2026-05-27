# db/setup_db.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "parking.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts DATETIME DEFAULT CURRENT_TIMESTAMP,
        source TEXT NOT NULL,      -- sensor/button/gate/manager
        topic TEXT NOT NULL,
        payload TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS state_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts DATETIME DEFAULT CURRENT_TIMESTAMP,
        parking_occupied INTEGER NOT NULL,
        gate_open INTEGER NOT NULL,
        last_level TEXT,
        last_message TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts DATETIME DEFAULT CURRENT_TIMESTAMP,
        level TEXT NOT NULL,       -- INFO/WARNING/ALARM
        message TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()
    print(f"DB ready at: {DB_PATH}")

if __name__ == "__main__":
    main()
