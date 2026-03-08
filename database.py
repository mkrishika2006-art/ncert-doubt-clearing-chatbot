# database.py

import json
from pathlib import Path

DB_FILE = Path("db.json")

def get_connection():
    """
    Dummy function to replace MySQL.
    We'll read/write directly to db.json for streaks and topics.
    """
    if not DB_FILE.exists():
        DB_FILE.write_text(json.dumps({"streaks": [], "topics": []}, indent=2))
    return DB_FILE
    

