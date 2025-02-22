# # database.py
# import sqlite3

# def init_db():
#     conn = sqlite3.connect('news.db')
#     c = conn.cursor()

#     # Create table for news articles
#     c.execute('''CREATE TABLE IF NOT EXISTS articles (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         topic TEXT NOT NULL,
#         sub_topic TEXT,
#         title TEXT NOT NULL,
#         url TEXT,
#         raw_text TEXT,
#         summary TEXT,
#         seo_title TEXT,
#         seo_keywords TEXT,
#         date TEXT,
#         published INTEGER DEFAULT 0
#     )''')

#     conn.commit()
#     conn.close()
#     print("Database initialized successfully.")

# # Insert hardcoded sample data for testing
# def insert_sample_data():
#     conn = sqlite3.connect('news.db')
#     c = conn.cursor()

#     sample_data = [
#         ("Uttar Pradesh", "Lucknow", "Crime Wave Hits Lucknow", "http://example.com",
#          "A daring robbery occurred in Lucknow yesterday. Thieves stole gold from a shop in broad daylight. Police are investigating this shocking crime.",
#          None, None, None, "2025-02-20"),

#         ("Sports", "Global", "Epic Cricket Match Ends in Tie", "http://example.com",
#          "The cricket world is buzzing after a nail-biting tie in the latest match. Fans went wild as the final ball sealed the deal.",
#          None, None, None, "2025-02-21")
#     ]

#     c.executemany(
#         "INSERT INTO articles (topic, sub_topic, title, url, raw_text, summary, seo_title, seo_keywords, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
#         sample_data
#     )

#     conn.commit()  # Make sure this is aligned correctly!
#     conn.close()
#     print("Sample data inserted successfully.")


# if __name__ == "__main__":
#     init_db()
#     insert_sample_data()


import sqlite3


def init_db():
    """Initialize the database and create the articles table if it does not exist."""
    conn = sqlite3.connect("news.db")
    c = conn.cursor()

    c.execute(
        """
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        sub_topic TEXT,
        title TEXT NOT NULL,
        url TEXT,
        raw_text TEXT,
        image_url TEXT,  -- Added this line to store image links
        summary TEXT,
        seo_title TEXT,
        seo_keywords TEXT,
        date TEXT,
        published INTEGER DEFAULT 0
    )
    """
    )

    conn.commit()
    conn.close()
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()
