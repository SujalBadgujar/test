import sqlite3
import random


class BlogPostGenerator:
    def __init__(self, db_path="news.db"):
        self.db_path = db_path

    def fetch_unsummarized_articles(self):
        """Fetch articles that haven't been converted into blog posts yet."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "SELECT id, title, raw_text, topic, sub_topic, date FROM articles WHERE published = 0"
        )
        articles = c.fetchall()
        conn.close()
        return articles

    def generate_seo_title(self, title):
        """Generate an SEO-friendly title that is engaging and keyword-rich."""
        seo_variations = [
            f"{title} - Everything You Need to Know!",
            f"The Latest on {title} - Full Details!",
            f"Breaking News: {title} and Why It Matters!",
            f"{title} - A Deep Dive Into the Developments!",
        ]
        return random.choice(seo_variations)

    def generate_meta_description(self, title, topic):
        """Generate a short, engaging meta description for SEO purposes."""
        return f"Get the latest insights on {title}. Stay informed about the most recent updates in {topic}."

    def generate_keywords(self, topic, sub_topic):
        """Generate relevant SEO keywords."""
        return (
            f"{topic}, {sub_topic}, latest {topic} news, breaking news, {topic} updates"
        )

    def format_blog_post(self, title, raw_text, seo_title, meta_desc, keywords, date):
        """Format the raw article into a well-structured, engaging blog post."""
        blog_post = f"""
        <article>
            <h1>{seo_title}</h1>
            <p><strong>Published on:</strong> {date}</p>
            <hr>

            <h3>Introduction</h3>
            <p>In recent developments, {title}. This article covers all the details, key highlights, and expert opinions.</p>

            <h3>Key Highlights</h3>
            <ul>
        """

        # Extract key paragraphs from the raw text to create bullet points
        paragraphs = raw_text.split(". ")
        for para in paragraphs[:5]:  # Take the first 5 main points
            if len(para) > 30:  # Ensure it's a meaningful point
                blog_post += f"<li>{para.strip()}.</li>\n"

        blog_post += """
            </ul>
            <hr>

    
        </article>
        """
        return blog_post

    def generate_blog_posts(self):
        """Convert articles into well-structured blog posts."""
        articles = self.fetch_unsummarized_articles()

        if not articles:
            print("No new articles to convert into blog posts.")
            return

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        for article in articles:
            article_id, title, raw_text, topic, sub_topic, date = article

            seo_title = self.generate_seo_title(title)
            meta_desc = self.generate_meta_description(title, topic)
            keywords = self.generate_keywords(topic, sub_topic)

            blog_post = self.format_blog_post(
                title, raw_text, seo_title, meta_desc, keywords, date
            )

            # Save the formatted blog post to the database
            c.execute(
                "UPDATE articles SET full_post = ?, seo_title = ?, meta_description = ?, seo_keywords = ?, published = 1 WHERE id = ?",
                (blog_post, seo_title, meta_desc, keywords, article_id),
            )

            print(f"📝 Blog post generated for: {title}")

        conn.commit()
        conn.close()


if __name__ == "__main__":
    generator = BlogPostGenerator()
    generator.generate_blog_posts()
