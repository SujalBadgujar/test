# blog_writer.py
import sqlite3
import logging

class BlogWriter:
    def __init__(self, db_path="news.db"):
        self.db_path = db_path

    def convert_first_article_to_blog(self):
        """Fetch the first unprocessed article and convert it to a blog post."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Fetch the most recent article that hasn't been processed (no seo_title yet)
        c.execute("""
            SELECT id, topic, sub_topic, title, raw_text, date 
            FROM articles 
            WHERE seo_title IS NULL 
            ORDER BY id DESC 
            LIMIT 1
        """)
        article = c.fetchone()

        if article:
            article_id, topic, sub_topic, title, raw_text, date = article
            
            # Create blog post content
            blog_content = self._create_blog_post(topic, sub_topic, title, raw_text, date)
            
            # Update the database with the blog content (overwriting raw_text)
            c.execute("""
                UPDATE articles 
                SET raw_text = ? 
                WHERE id = ?
            """, (blog_content, article_id))
            logging.info(f"Converted article {article_id} to blog post: {title}")
        else:
            logging.info("No new articles found to convert to blog post.")

        conn.commit()
        conn.close()

    def _create_blog_post(self, topic, sub_topic, title, raw_text, date):
        """Transform news data into a human-like blog post."""
        intro = f"Hey there, readers! Today, we’re diving into some big news from {sub_topic}, {topic}. On {date}, something noteworthy caught our attention: {title}. Let’s break it down and see what’s happening!"

        body = f"So, here’s the story: {raw_text}\n\nNow, let’s unpack this a bit. This event in {sub_topic} isn’t just another headline—it’s a glimpse into what’s shaping {topic} right now. Whether it’s the people, the place, or the sheer impact, there’s a lot to chew on here. Imagine being on the ground as this unfolded—what a scene!"

        conclusion = f"That’s all for now, folks! What are your thoughts on this {sub_topic} update? Drop a comment below, and let’s keep the conversation going. Until next time, stay curious!"

        # Combine into a single blog post
        blog_post = f"{intro}\n\n{body}\n\n{conclusion}"
        return blog_post

# Example usage (for testing)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    writer = BlogWriter()
    writer.convert_first_article_to_blog()