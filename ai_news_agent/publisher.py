import sqlite3
from flask import Flask, render_template, abort
import threading
import os

app = Flask(__name__)

class Publisher:
    def __init__(self, db_path="news.db"):
        self.db_path = db_path
        self.app = app
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/")
        def index():
            """Display all published articles."""
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute(
                "SELECT id, seo_title, date, full_post FROM articles WHERE published = 1 ORDER BY date DESC"
            )
            articles = c.fetchall()
            conn.close()
            return render_template("index.html", articles=articles)

        @self.app.route("/article/<int:article_id>")
        def article(article_id):
            """Display a single published article."""
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute(
                """
                SELECT seo_title, full_post, date, seo_keywords 
                FROM articles 
                WHERE id = ? AND published = 1
                """,
                (article_id,),
            )
            article_data = c.fetchone()
            conn.close()

            if article_data:
                seo_title, full_post, date, seo_keywords = article_data
                return render_template(
                    "article.html",
                    title=seo_title,
                    content=full_post,
                    date=date,
                    seo_keywords=seo_keywords,
                    meta_description=full_post[:150],  # Meta description from first 150 chars
                )

            abort(404)  # Return proper 404 page

    def publish_articles(self):
        """Publish all articles that have been processed for SEO."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "UPDATE articles SET published = 1 WHERE seo_title IS NOT NULL AND published = 0"
        )
        conn.commit()
        conn.close()
        print("✅ Published all optimized articles.")

    def run_server(self):
        """Run the Flask server."""
        port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port
        print(f"🚀 Starting Flask server at http://0.0.0.0:{port}")
        self.app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False, threaded=True)

    def start(self):
        """Start the server in a separate thread."""
        self.publish_articles()
        server_thread = threading.Thread(target=self.run_server)
        server_thread.daemon = True
        server_thread.start()
        print("✅ Blog server started at http://127.0.0.1:5000")

if __name__ == "__main__":
    publisher = Publisher()
    publisher.run_server()  # Removed threading, Flask runs normally
