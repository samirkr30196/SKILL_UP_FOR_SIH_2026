from database import get_connection

def get_officer_complaints(department):
    connection = get_connection()
    rows = connection.execute(
        "SELECT * FROM complaints WHERE category=? ORDER BY id DESC",
        (department.replace(" Department", ""),)
    ).fetchall()
    connection.close()
    return [dict(row) for row in rows]

def update_complaint(complaint_id, officer_id, status, remark):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE complaints
        SET status=?, remark=?, officer_id=?
        WHERE id=?
    """, (status, remark, officer_id, complaint_id))
    connection.commit()
    updated = cursor.rowcount > 0
    connection.close()
    return updated