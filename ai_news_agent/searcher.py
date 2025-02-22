import sqlite3
import requests
from bs4 import BeautifulSoup

class Searcher:
    def __init__(self, db_path="news.db"):
        self.db_path = db_path

    def store_article(self, topic, sub_topic, title, url, raw_text, image_url, date):
        """Store an article in the database."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO articles (topic, sub_topic, title, url, raw_text, image_url, summary, seo_title, seo_keywords, date, published)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (topic, sub_topic, title, url, raw_text, image_url, None, None, None, date, 0))
        conn.commit()
        conn.close()
        print(f"✅ Stored article: {title}")

    def fetch_article_content(self, url):
        """Extract article text and image using BeautifulSoup."""
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract text content (only meaningful paragraphs)
            paragraphs = soup.find_all("p")
            raw_text = " ".join(p.get_text(strip=True) for p in paragraphs[:10])  # First 10 paragraphs

            # Extract main image (if available)
            image_tag = soup.find("meta", property="og:image") or soup.find("img")
            image_url = image_tag["content"] if image_tag and image_tag.has_attr("content") else None

            return raw_text[:3000], image_url  # Limit text to avoid overload

        except Exception as e:
            print(f"⚠️ Error fetching article content: {e}")
            return "Could not fetch article content", None

    def crawl_bing_news(self, topic, sub_topic, max_articles=5):
        """Fetch news articles from Bing News."""
        search_query = f"{topic} {sub_topic}"
        search_url = f"https://www.bing.com/news/search?q={search_query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            articles = soup.find_all("a", class_="title")[:max_articles]

            for article in articles:
                title = article.text.strip()
                url = article["href"]

                print(f"🔍 Found Article: {title}")

                # Fetch full article content & image
                raw_text, image_url = self.fetch_article_content(url)

                # Store in database
                self.store_article(topic, sub_topic, title, url, raw_text, image_url, "2025-02-22")

        except Exception as e:
            print(f"❌ Error crawling Bing News: {e}")

if __name__ == "__main__":
    searcher = Searcher()
    searcher.crawl_bing_news("uttar pradesh", "Lucknow")
