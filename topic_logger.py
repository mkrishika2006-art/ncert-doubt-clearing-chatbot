from datetime import datetime
from database import get_connection

def log_topic(topic):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO topics (topic, time) VALUES (%s, %s)",
        (topic, datetime.now())
    )

    conn.commit()

    cursor.close()
    conn.close()