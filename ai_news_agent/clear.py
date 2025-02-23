# clear.py
import sqlite3

def clear_database(db_path="news.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS articles")
    conn.commit()
    conn.close()
    print("Database cleared successfully.")

if __name__ == "__main__":
    clear_database()