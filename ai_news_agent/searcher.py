# # # searcher.py
# # import sqlite3
# # import requests
# # from bs4 import BeautifulSoup


# # class Searcher:
# #     def __init__(self, db_path="news.db"):
# #         self.db_path = db_path

# #     def store_article(self, topic, sub_topic, title, url, raw_text, date):
# #         """Store an article in the database."""
# #         conn = sqlite3.connect(self.db_path)
# #         c = conn.cursor()
# #         c.execute(
# #             """
# #             INSERT INTO articles (topic, sub_topic, title, url, raw_text, date)
# #             VALUES (?, ?, ?, ?, ?, ?)
# #         """,
# #             (topic, sub_topic, title, url, raw_text, date),
# #         )
# #         conn.commit()
# #         conn.close()
# #         print(f"Stored article: {title}")

# #     # def fetch_hardcoded_data(self):
# #     #     """Insert hardcoded sample data for testing."""
# #     #     hardcoded_articles = [
# #     #         (
# #     #             "Uttar Pradesh",
# #     #             "Lucknow",
# #     #             "Floods Disrupt Life in Lucknow",
# #     #             "http://example.com/floods",
# #     #             "Heavy rains caused flooding in Lucknow today. Roads were blocked, and schools closed.",
# #     #             "2025-02-21",
# #     #         ),
# #     #         (
# #     #             "Sports",
# #     #             "Global",
# #     #             "Tennis Star Wins Championship",
# #     #             "http://example.com/tennis",
# #     #             "A thrilling match ended with a surprising victory in the global tennis championship.",
# #     #             "2025-02-21",
# #     #         ),
# #     #     ]

# #     #     for article in hardcoded_articles:
# #     #         self.store_article(*article)

# #     def crawl_web(self, keyword, max_articles=2):
# #         """Simple web crawler to fetch articles based on a keyword."""
# #         # Using a search engine-like approach (DuckDuckGo as an example)
# #         search_url = f"https://www.google.com/search?q={keyword}+news&tbm=nws"
# #         headers = {"User-Agent": "Mozilla/5.0"}  # Basic user-agent to avoid blocks

# #         try:
# #             response = requests.get(search_url, headers=headers)
# #             response.raise_for_status()
# #             soup = BeautifulSoup(response.text, "html.parser")

# #             # Extract links from search results (simplified)
# #             links = soup.find_all("a", class_="result__a")[:max_articles]
# #             for link in links:
# #                 url = link.get("href")
# #                 title = link.text.strip()

# #                 # Fetch the article page
# #                 article_response = requests.get(url, headers=headers)
# #                 article_soup = BeautifulSoup(article_response.text, "html.parser")

# #                 # Extract raw text (simplified: grab all <p> tags)
# #                 paragraphs = article_soup.find_all("p")
# #                 raw_text = " ".join(
# #                     p.text.strip() for p in paragraphs[:3]
# #                 )  # Limit to first 3 paragraphs

# #                 # Classify based on keyword (basic logic)
# #                 topic = keyword.split()[0]  # e.g., "Uttar" from "Uttar Pradesh"
# #                 sub_topic = (
# #                     " ".join(keyword.split()[1:]) if len(keyword.split()) > 1 else None
# #                 )

# #                 # Store in database
# #                 self.store_article(topic, sub_topic, title, url, raw_text, "2025-02-21")

# #         except Exception as e:
# #             print(f"Error crawling web: {e}")


# # if __name__ == "__main__":
# #     # Test the Searcher
# #     searcher = Searcher()
# #     # print("Testing hardcoded data...")
# #     # searcher.fetch_hardcoded_data()
# #     print("\nTesting web crawler...")
# #     searcher.crawl_web("Uttar Pradesh")


import sqlite3
import requests
from bs4 import BeautifulSoup


class Searcher:
    def __init__(self, db_path="news.db"):
        self.db_path = db_path

    def store_article(self, topic, sub_topic, title, url, raw_text, date):
        """Store an article in the database."""
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
        print(f"Stored article: {title}")

    def crawl_web(self, max_articles=3):
        """Fetch and store news articles for Uttar Pradesh and Lucknow."""
        topics = [("Uttar Pradesh", "Global"), ("Lucknow", "Local")]
        headers = {"User-Agent": "Mozilla/5.0"}

        for keyword, sub_topic in topics:
            print(f"Fetching news for: {keyword}")

            search_url = (
                f"https://www.bing.com/news/search?q={keyword.replace(' ', '+')}"
            )
            try:
                response = requests.get(search_url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

                articles = soup.find_all("a", class_="title")[:max_articles]
                for article in articles:
                    title = article.text.strip()
                    url = article["href"]

                    # Fetch full article text
                    article_response = requests.get(url, headers=headers)
                    article_soup = BeautifulSoup(article_response.text, "html.parser")
                    paragraphs = article_soup.find_all("p")
                    raw_text = " ".join(
                        p.text.strip() for p in paragraphs[:3]
                    )  # Get first 3 paragraphs

                    # Store in database
                    self.store_article(
                        keyword, sub_topic, title, url, raw_text, "2025-02-22"
                    )

            except Exception as e:
                print(f"Error fetching news for {keyword}: {e}")


if __name__ == "__main__":
    searcher = Searcher()
    searcher.crawl_web()


# # searcher.py
# import sqlite3
# import requests
# from bs4 import BeautifulSoup


# class Searcher:
#     def __init__(self, db_path="news.db"):
#         self.db_path = db_path

#     def store_article(self, topic, sub_topic, title, url, raw_text, date):
#         """Store an article in the database."""
#         conn = sqlite3.connect(self.db_path)
#         c = conn.cursor()
#         c.execute(
#             """
#             INSERT INTO articles (topic, sub_topic, title, url, raw_text, date)
#             VALUES (?, ?, ?, ?, ?, ?)
#             """,
#             (topic, sub_topic, title, url, raw_text, date),
#         )
#         conn.commit()
#         conn.close()
#         print(f"Stored article: {title}")

#     def crawl_news(self, keyword, max_articles=5):
#         """Fetch articles for a given keyword."""
#         search_url = f"https://www.google.com/search?q={keyword}+news&tbm=nws"
#         headers = {"User-Agent": "Mozilla/5.0"}

#         try:
#             response = requests.get(search_url, headers=headers)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.text, "html.parser")

#             # Extract news article links
#             news_items = soup.find_all("div", class_="BVG0Nb", limit=max_articles)
#             for item in news_items:
#                 title = item.text
#                 url = item.find_parent("a")["href"]

#                 # Fetch article page
#                 article_response = requests.get(url, headers=headers)
#                 article_soup = BeautifulSoup(article_response.text, "html.parser")

#                 # Extract raw text (first 3 paragraphs)
#                 paragraphs = article_soup.find_all("p")
#                 raw_text = " ".join(p.text.strip() for p in paragraphs[:3])

#                 topic, sub_topic = keyword.split()[0], " ".join(keyword.split()[1:])

#                 # Store in database
#                 self.store_article(topic, sub_topic, title, url, raw_text, "2025-02-21")

#         except Exception as e:
#             print(f"Error crawling news for {keyword}: {e}")


# if __name__ == "__main__":
#     searcher = Searcher()
#     print("\nFetching news for Uttar Pradesh...")
#     searcher.crawl_news("Uttar Pradesh")
#     print("\nFetching news for Lucknow...")
#     searcher.crawl_news("Lucknow")
