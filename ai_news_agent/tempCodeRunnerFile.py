# main.py
import time
from clear import clear_database
from database import init_db
from searcher import Searcher
from summarizer import Summarizer
from seo_optimizer import SEOOptimizer
from publisher import Publisher


def run_news_agent(topic="Uttar Pradesh", sub_topic="Lucknow"):
    print("Starting the AI News Agent...")

    try:
        # Clear the database
        print("Clearing database...")
        clear_database()

        # Initialize the database
        print("Initializing database...")
        init_db()

        # Fetch news articles
        searcher = Searcher()
        print(f"Fetching news for {topic} - {sub_topic}...")
        searcher.crawl_web(topic, sub_topic)

        # Generate full blog post
        summarizer = Summarizer()
        print("Generating crazy blog post...")
        summarizer.process_articles(topic, sub_topic)

        # Optimize for SEO
        optimizer = SEOOptimizer()
        print("Optimizing for SEO...")
        optimizer.optimize_articles()

        # Publish to blog
        publisher = Publisher()
        print("Publishing to the blog...")
        publisher.start()

        # Give the server time to start
        print("Waiting for server to initialize...")
        time.sleep(5)  # Wait 5 seconds to ensure Flask is up

    except Exception as e:
        print(f"Error in pipeline: {e}")

    print("Pipeline completed. Check http://127.0.0.1:5000")


if __name__ == "__main__":
    run_news_agent()

    # Keep the script alive so Flask doesn't stop
    print("AI News Agent is running... Press Ctrl+C to stop.")
    while True:
        time.sleep(1)
