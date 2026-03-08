# streak_manager.py

from datetime import date, timedelta
from database import get_connection
import json

def update_streak():
    today = date.today()
    db_file = get_connection()

    # Load data
    with open(db_file, "r") as f:
        data = json.load(f)

    streaks = data.get("streaks", [])

    if streaks:
        last_entry = streaks[-1]
        last_login = date.fromisoformat(last_entry["last_login"])
        streak = last_entry["streak"]

        if last_login == today:
            return streak
        elif last_login == today - timedelta(days=1):
            streak += 1
        else:
            streak = 1
    else:
        streak = 1

    # Append new streak
    streaks.append({"last_login": today.isoformat(), "streak": streak})
    data["streaks"] = streaks

    with open(db_file, "w") as f:
        json.dump(data, f, indent=2)

    return streak
