import sqlite3
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class SEOOptimizer:
    def __init__(self, db_path="news.db"):
        self.db_path = db_path
        nltk.download('punkt')  # Ensure tokenizer is available
        nltk.download('stopwords')  # Ensure stopwords are available

    def generate_seo_title(self, original_title, topic, sub_topic=None):
        """Create an SEO-friendly title."""
        base_title = original_title.strip()
        if sub_topic:
            seo_title = f"{sub_topic} {base_title} - Latest {topic} News 2025"
        else:
            seo_title = f"{base_title} - Latest {topic} News 2025"
        return seo_title[:60]  # Limit to 60 characters for SEO best practice

    def extract_keywords(self, text):
        """Extract top keywords from text."""
        if not text:
            return ""

        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text.lower())

        # Count word frequency, ignoring stopwords and non-alphanumeric words
        word_freq = {}
        for word in words:
            if word not in stop_words and word.isalnum():
                word_freq[word] = word_freq.get(word, 0) + 1

        # Get top 5 keywords
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        return ", ".join([word for word, freq in top_keywords])

    def optimize_articles(self):
        """Optimize all summarized articles in the database."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Fetch articles that have summaries but no SEO data
        c.execute("SELECT id, title, topic, sub_topic, summary FROM articles WHERE summary IS NOT NULL AND seo_title IS NULL")
        articles = c.fetchall()

        if not articles:
            print("No articles found for SEO optimization.")
            conn.close()
            return

        for article_id, title, topic, sub_topic, summary in articles:
            seo_title = self.generate_seo_title(title, topic, sub_topic)
            seo_keywords = self.extract_keywords(summary)

            c.execute("UPDATE articles SET seo_title = ?, seo_keywords = ? WHERE id = ?",
                      (seo_title, seo_keywords, article_id))
            print(f"Optimized article ID {article_id}: {seo_title} | Keywords: {seo_keywords}")

        conn.commit()
        conn.close()

if __name__ == "__main__":
    # Test the SEO Optimizer
    optimizer = SEOOptimizer()
    print("Testing SEO optimization...")
    
    sample_title = "Floods Disrupt Life"
    sample_topic = "Uttar Pradesh"
    sample_sub_topic = "Lucknow"
    sample_summary = "Heavy rains caused flooding in Lucknow today. Roads were blocked, and schools closed."

    seo_title = optimizer.generate_seo_title(sample_title, sample_topic, sample_sub_topic)
    seo_keywords = optimizer.extract_keywords(sample_summary)

    print(f"SEO Title: {seo_title}")
    print(f"SEO Keywords: {seo_keywords}")

    print("\nOptimizing articles from database...")
    optimizer.optimize_articles()
