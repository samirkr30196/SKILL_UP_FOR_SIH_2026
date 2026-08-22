from database import get_connection
from ai import classify_complaint, calculate_priority

def create_complaint(
    user_id,
    description,
    location,
    category,
    image_path=""
):
    category = classify_complaint(description) if not category else category
    priority = calculate_priority(description)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO complaints
        (user_id, description, location, category, priority, image_path)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        description,
        location,
        category,
        priority,
        image_path
    ))

    connection.commit()
    complaint_id = cursor.lastrowid
    connection.close()

    return {
        "id": complaint_id,
        "category": category,
        "priority": priority,
        "image_path": image_path
    }
def get_user_complaints(user_id):
    connection = get_connection()
    rows = connection.execute(
        "SELECT * FROM complaints WHERE user_id=? ORDER BY id DESC",
        (user_id,)
    ).fetchall()
    connection.close()
    return [dict(row) for row in rows]

def get_complaint(complaint_id):
    connection = get_connection()
    row = connection.execute(
        "SELECT * FROM complaints WHERE id=?", (complaint_id,)
    ).fetchone()
    connection.close()
    return dict(row) if row else None