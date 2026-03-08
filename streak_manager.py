from datetime import date, timedelta
from database import get_connection

def update_streak():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT last_login, streak FROM streaks ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()

    today = date.today()

    if result:
        last_login, streak = result

        if last_login == today:
            return streak

        elif last_login == today - timedelta(days=1):
            streak += 1
        else:
            streak = 1
    else:
        streak = 1

    cursor.execute(
        "INSERT INTO streaks (last_login, streak) VALUES (%s, %s)",
        (today, streak)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return streak