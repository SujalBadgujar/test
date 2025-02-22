import sqlite3
import random

class BlogPostGenerator:
    def __init__(self, db_path="news.db"):
        self.db_path = db_path

    def fetch_unsummarized_articles(self):
        """Fetch articles that haven't been published yet."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT id, title, raw_text, image_url, topic, sub_topic, date FROM articles WHERE published = 0")
        articles = c.fetchall()
        conn.close()
        return articles

    def generate_seo_title(self, title):
        """Generate an SEO-friendly title by making it catchy and keyword-rich."""
        seo_variations = [
            f"{title} - Everything You Need to Know!",
            f"The Latest Update on {title} - Explained!",
            f"Breaking: {title} and Why It Matters!",
            f"{title} - A Deep Dive Into the Details!",
        ]
        return random.choice(seo_variations)

    def generate_meta_description(self, title, topic):
        """Generate an SEO-friendly meta description."""
        return f"Read about {title}, the latest in {topic}. Get insights, analysis, and key takeaways in this detailed blog post."

    def generate_keywords(self, topic, sub_topic):
        """Generate SEO-friendly keywords."""
        return f"{topic}, {sub_topic}, latest {topic} news, breaking news, {topic} updates"

    def format_blog_post(self, title, raw_text, image_url, seo_title, meta_desc, keywords, date):
        """Format the article into a blog post structure."""
        blog_post = f"""
        <article>
            <h1>{seo_title}</h1>
            <img src="{image_url}" alt="{title}">
            <p><strong>Published on:</strong> {date}</p>
            <p>{meta_desc}</p>
            <hr>
            <p>{raw_text}</p>
            <hr>
            <h2>Conclusion</h2>
            <p>Stay updated on {title}. Follow us for more updates on {keywords}.</p>
            <p><em>Source: Web Scraped News</em></p>
        </article>
        """
        return blog_post

    def generate_blog_posts(self):
        """Generate blog posts for all unsummarized articles."""
        articles = self.fetch_unsummarized_articles()

        if not articles:
            print("No new articles to generate blog posts for.")
            return
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        for article in articles:
            article_id, title, raw_text, image_url, topic, sub_topic, date = article
            
            seo_title = self.generate_seo_title(title)
            meta_desc = self.generate_meta_description(title, topic)
            keywords = self.generate_keywords(topic, sub_topic)

            blog_post = self.format_blog_post(title, raw_text, image_url, seo_title, meta_desc, keywords, date)
            
            # Save the generated blog post back to the database
            c.execute("UPDATE articles SET summary = ?, seo_title = ?, seo_keywords = ?, published = 1 WHERE id = ?", 
                      (blog_post, seo_title, keywords, article_id))
            
            print(f"📝 Generated blog post for: {title}")

        conn.commit()
        conn.close()

if __name__ == "__main__":
    generator = BlogPostGenerator()
    generator.generate_blog_posts()
