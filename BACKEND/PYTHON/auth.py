from database import get_connection

def register_citizen(name, email, mobile, password):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users(name,email,mobile,password) VALUES(?,?,?,?)",
            (name, email, mobile, password)
        )
        connection.commit()
        return {"id": cursor.lastrowid, "name": name, "email": email}
    finally:
        connection.close()

def login_citizen(email, password):
    connection = get_connection()
    row = connection.execute(
        "SELECT id,name,email FROM users WHERE email=? AND password=?",
        (email, password)
    ).fetchone()
    connection.close()
    return dict(row) if row else None

def login_officer(officer_id, password):
    connection = get_connection()
    row = connection.execute(
        "SELECT officer_id,department FROM officers WHERE officer_id=? AND password=?",
        (officer_id, password)
    ).fetchone()
    connection.close()
    return dict(row) if row else None

def login_admin(admin_id, password):
    connection = get_connection()
    row = connection.execute(
        "SELECT admin_id FROM admins WHERE admin_id=? AND password=?",
        (admin_id, password)
    ).fetchone()
    connection.close()
    return dict(row) if row else None