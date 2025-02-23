import sqlite3

def init_db(db_path="news.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Ensure the articles table exists with the required fields
    c.execute('''CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        sub_topic TEXT,
        title TEXT NOT NULL,
        url TEXT,
        raw_text TEXT,
        full_post TEXT,  -- Full blog post content
        seo_title TEXT,
        seo_keywords TEXT,
        meta_description TEXT,  -- Add meta description column
        date TEXT,
        published INTEGER DEFAULT 0
    )''')

    # Check if the 'full_post' column exists, if not, add it
    c.execute("PRAGMA table_info(articles)")
    columns = [row[1] for row in c.fetchall()]
    
    if "full_post" not in columns:
        c.execute("ALTER TABLE articles ADD COLUMN full_post TEXT")
        print("✅ Added missing column: full_post")

    if "meta_description" not in columns:
        c.execute("ALTER TABLE articles ADD COLUMN meta_description TEXT")
        print("✅ Added missing column: meta_description")

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")

if __name__ == "__main__":
    init_db()
