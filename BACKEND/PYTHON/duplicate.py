from database import get_connection


def find_similar_complaints(category, location):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM complaints
        WHERE category = ?
        AND location = ?
    """, (category, location))

    complaints = cursor.fetchall()

    connection.close()

    return complaints