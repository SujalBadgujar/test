# seo_optimizer.py
import sqlite3
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

class SEOOptimizer:
    def __init__(self, db_path="news.db"):
        self.db_path = db_path
        nltk.download('punkt')
        nltk.download('stopwords')

    def generate_seo_title(self, original_title, topic, sub_topic):
        return f"{sub_topic} {original_title} - {topic} News 2025"

    def extract_keywords(self, text):
        stop_words = set(stopwords.words('english'))
        words = [w for w in word_tokenize(text.lower()) if w.isalnum() and w not in stop_words]
        word_freq = nltk.FreqDist(words)
        return ", ".join([word for word, freq in word_freq.most_common(5)])

    def optimize_articles(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT id, title, topic, sub_topic, full_post FROM articles WHERE full_post IS NOT NULL AND seo_title IS NULL")
        articles = c.fetchall()
        
        for article_id, title, topic, sub_topic, full_post in articles:
            seo_title = self.generate_seo_title(title, topic, sub_topic)
            seo_keywords = self.extract_keywords(full_post)
            c.execute("UPDATE articles SET seo_title = ?, seo_keywords = ? WHERE id = ?",
                      (seo_title, seo_keywords, article_id))
            print(f"Optimized article ID {article_id}: {seo_title}")
        
        conn.commit()
        conn.close()

if __name__ == "__main__":
    optimizer = SEOOptimizer()
    optimizer.optimize_articles()