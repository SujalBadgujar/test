import sqlite3

def clear_database(db_path="news.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM articles")  # Removes all records
    conn.commit()
    conn.close()
    print("Database cleared!")

clear_database()
