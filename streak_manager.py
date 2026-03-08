# streak_manager.py

from datetime import date, timedelta
from database import get_connection

def update_streak():
    today = date.today()

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Get the latest streak
        cursor.execute("SELECT last_login, streak FROM streaks ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()

        if result:
            last_login, streak = result

            if last_login == today:
                return streak  # Already updated today

            elif last_login == today - timedelta(days=1):
                streak += 1  # Continue streak
            else:
                streak = 1  # Reset streak
        else:
            streak = 1  # First streak

        # Save the new streak
        cursor.execute(
            "INSERT INTO streaks (last_login, streak) VALUES (%s, %s)",
            (today, streak)
        )

        conn.commit()
        cursor.close()
        conn.close()

    except RuntimeError:
        # Database not available, skip saving streak
        print(f"⚠️ Skipping streak update; DB not available.")
        streak = 1  # Optional: always return 1 if no DB

    return streak
