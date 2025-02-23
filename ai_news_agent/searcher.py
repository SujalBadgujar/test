import requests
from bs4 import BeautifulSoup
import sqlite3
from googlesearch import search  # Google Search API


class Searcher:
    def __init__(self, db_path="news.db"):
        self.db_path = db_path

    def store_article(self, topic, sub_topic, title, url, raw_text, date):
        """Store extracted news articles into the database."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            """
            INSERT INTO articles (topic, sub_topic, title, url, raw_text, date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (topic, sub_topic, title, url, raw_text, date),
        )
        conn.commit()
        conn.close()
        print(f"✅ Stored article: {title} | {url}")

    def google_news_search(self, query, max_results=5):
        """Fetch search results from Google News."""
        print(f"🔍 Searching Google News for '{query}'...")
        search_query = f"{query} site:thehindu.com"

        try:
            results = search(search_query, num_results=max_results)
            return list(results)  # Returns URLs of articles

        except Exception as e:
            print(f"❌ Error fetching search results: {e}")
            return []

    def crawl_web(self, topic, sub_topic, max_articles=5):
        """Scrape news articles from search results."""
        print(f"📡 Fetching news from Google News for {topic} - {sub_topic}...")

        query = f"{topic} {sub_topic} latest news"
        articles = self.google_news_search(query, max_articles)

        if not articles:
            print("⚠️ No articles found!")
            return

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Brave/1.60.114"
        }

        for url in articles:
            print(f"📰 Scraping: {url}")

            try:
                article_response = requests.get(url, headers=headers)
                article_response.raise_for_status()
                article_soup = BeautifulSoup(article_response.text, "html.parser")

                # Extract paragraphs from news websites
                # Extract the main article body
                article_body = article_soup.find("div", itemprop="articleBody")

                if article_body:
                    paragraphs = article_body.find_all(
                        "p"
                    )  # Extract only <p> inside articleBody
                else:
                    paragraphs = article_soup.select(
                        "p"
                    )  # Fallback to selecting all <p> tags

                # Extract and filter text
                raw_text = " ".join(
                    p.text.strip() for p in paragraphs if len(p.text.strip()) > 20
                )

                if raw_text:
                    # Try extracting the title from <h1>
                    title_tag = article_soup.find("h1")
                    if title_tag:
                        title = title_tag.text.strip()
                    else:
                        # Fallback to Open Graph meta tag
                        meta_tag = article_soup.find("meta", property="og:title")
                        title = (
                            meta_tag["content"].strip()
                            if meta_tag
                            else (
                                article_soup.title.text.strip()
                                if article_soup.title
                                else "Untitled"
                            )
                        )

                    print(
                        f"✅ Extracted: {raw_text[:100]}..."
                    )  # Preview first 100 chars
                    self.store_article(
                        topic, sub_topic, title, url, raw_text, "2025-02-22"
                    )
                else:
                    print(f"⚠️ No substantial text found for {url}")

            except Exception as e:
                print(f"❌ Error scraping article: {e}")


if __name__ == "__main__":
    searcher = Searcher()
    searcher.crawl_web("Uttar Pradesh", "Lucknow")
