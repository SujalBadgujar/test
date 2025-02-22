import sqlite3
from flask import Flask, render_template, abort

app = Flask(__name__)

class Publisher:
    def __init__(self, db_path="news.db"):
        self.db_path = db_path
        self.setup_routes()

    def setup_routes(self):
        """Set up Flask routes for the blog."""
        @app.route('/')
        def index():
            """Display the list of published articles."""
            try:
                with sqlite3.connect(self.db_path) as conn:
                    c = conn.cursor()
                    c.execute("SELECT id, seo_title, date FROM articles WHERE published = 1 ORDER BY date DESC")
                    articles = c.fetchall()
                return render_template('index.html', articles=articles)
            except Exception as e:
                print(f"[ERROR] Could not fetch articles: {e}")
                return "Error loading articles", 500

        @app.route('/article/<int:article_id>')
        def article(article_id):
            """Display a specific article."""
            try:
                with sqlite3.connect(self.db_path) as conn:
                    c = conn.cursor()
                    c.execute("""
                        SELECT seo_title, summary, date, seo_keywords 
                        FROM articles 
                        WHERE id = ? AND published = 1
                    """, (article_id,))
                    article_data = c.fetchone()

                if article_data:
                    seo_title, summary, date, seo_keywords = article_data
                    return render_template('article.html', 
                                           title=seo_title, 
                                           summary=summary, 
                                           date=date, 
                                           seo_keywords=seo_keywords,
                                           meta_description=summary[:150])  # Short SEO-friendly description
                return abort(404, description="Article not found")
            except Exception as e:
                print(f"[ERROR] Could not fetch article ID {article_id}: {e}")
                return "Error loading article", 500

    def publish_articles(self):
        """Publish all optimized articles that are not yet published."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute("""
                    SELECT id, seo_title 
                    FROM articles 
                    WHERE seo_title IS NOT NULL AND published = 0
                """)
                articles = c.fetchall()

                if not articles:
                    print("[INFO] No new articles to publish.")
                else:
                    for article_id, seo_title in articles:
                        c.execute("UPDATE articles SET published = 1 WHERE id = ?", (article_id,))
                        print(f"[SUCCESS] Published article ID {article_id}: {seo_title}")

                conn.commit()
        except Exception as e:
            print(f"[ERROR] Could not publish articles: {e}")

    def run_server(self):
        """Run the Flask server."""
        try:
            print("[INFO] Starting Flask server at http://127.0.0.1:5000")
            app.run(host="127.0.0.1", port=5000, debug=True)
        except Exception as e:
            print(f"[ERROR] Flask server failed to start: {e}")

if __name__ == "__main__":
    publisher = Publisher()
    publisher.publish_articles()
    publisher.run_server()
