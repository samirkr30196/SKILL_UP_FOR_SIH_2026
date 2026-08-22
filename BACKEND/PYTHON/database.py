import sqlite3
from pathlib import Path

DATABASE_DIR = Path(__file__).resolve().parent.parent / "DATABASE"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)
DATABASE = DATABASE_DIR / "civicPulse.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            mobile TEXT NOT NULL,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS officers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            officer_id TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            department TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            location TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            remark TEXT DEFAULT '',
            officer_id TEXT,
            image_path TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cursor.executemany("""
        INSERT INTO officers (officer_id, password, department)
        VALUES (?, ?, ?)
        ON CONFLICT(officer_id) DO UPDATE SET
            password = excluded.password,
            department = excluded.department
    """, [
        ("road@gmail.com", "road1234", "Road Department"),
        ("water@gmail.com", "water1234", "Water Department"),
        ("electricity@gmail.com", "electricity1234", "Electricity Department"),
        ("sanitation@gmail.com", "sanitation1234", "Sanitation Department"),
        ("health@gmail.com", "health1234", "Health Department"),
    ])

    cursor.execute("""
        INSERT INTO admins (admin_id, password)
        VALUES (?, ?)
        ON CONFLICT(admin_id) DO UPDATE SET
            password = excluded.password
    """, ("samirkr30196@gmail.com", "samir4412#"))

    try:
        cursor.execute(
            "ALTER TABLE complaints ADD COLUMN image_path TEXT DEFAULT ''"
        )
    except sqlite3.OperationalError:
        pass

    connection.commit()
    connection.close()