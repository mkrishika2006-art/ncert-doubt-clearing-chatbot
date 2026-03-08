from database import get_connection

def log_topic(topic):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO topics (topic, time) VALUES (%s, NOW())", (topic,))
        conn.commit()
        cursor.close()
        conn.close()
    except RuntimeError:
        # Database not available, skip logging
        print(f"⚠️ Skipping topic logging for '{topic}' because DB is not available.")
