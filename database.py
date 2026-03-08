# database.py

# Optional fallback if MySQL is not installed
try:
    import mysql.connector
except ModuleNotFoundError:
    mysql = None
    print("⚠️ MySQL not installed, database features will be disabled.")

def get_connection():
    if mysql is None:
        raise RuntimeError("Database not available. MySQL module not installed.")
    
    # Change these values if you have a real DB
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="chatbot_db"
    )
