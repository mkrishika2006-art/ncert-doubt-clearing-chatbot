# topic_logger.py

from datetime import datetime
from database import get_connection
import json

def log_topic(topic):
    db_file = get_connection()

    # Load data
    with open(db_file, "r") as f:
        data = json.load(f)

    topics = data.get("topics", [])

    topics.append({"topic": topic, "time": datetime.now().isoformat()})
    data["topics"] = topics

    with open(db_file, "w") as f:
        json.dump(data, f, indent=2)
