from database import get_connection

def get_all_complaints():
    connection = get_connection()
    rows = connection.execute(
        "SELECT * FROM complaints ORDER BY id DESC"
    ).fetchall()
    connection.close()
    return [dict(row) for row in rows]

def get_city_statistics():
    connection = get_connection()
    total = connection.execute(
        "SELECT COUNT(*) FROM complaints"
    ).fetchone()[0]
    pending = connection.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='Pending'"
    ).fetchone()[0]
    resolved = connection.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='Resolved'"
    ).fetchone()[0]
    connection.close()

    return {"total": total, "pending": pending, "resolved": resolved}