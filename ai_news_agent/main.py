import time
from clear import clear_database
from database import init_db
from searcher import Searcher
from post_generator import BlogPostGenerator  # Updated to use BlogPostGenerator
from seo_optimizer import SEOOptimizer
from publisher import Publisher

def run_news_agent(topic="Uttar Pradesh", sub_topic="Lucknow"):
    print("🚀 Starting the AI News Agent...")

    try:
        # Step 1: Clear the database
        print("🗑️ Clearing old data...")
        clear_database()

        # Step 2: Initialize the database
        print("📂 Initializing database...")
        init_db()

        # Step 3: Fetch news articles
        searcher = Searcher()
        print(f"📰 Fetching news for {topic} - {sub_topic}...")
        searcher.crawl_web(topic, sub_topic)

        # Step 4: Convert news articles into blog posts
        blog_generator = BlogPostGenerator()
        print("✍️ Generating blog posts...")
        blog_generator.generate_blog_posts()

        # # Step 5: Optimize blog posts for SEO
        # seo_optimizer = SEOOptimizer()
        # print("📈 Optimizing blog posts for SEO...")
        # seo_optimizer.optimize_all()

        # Step 6: Publish to blog
        publisher = Publisher()
        print("📢 Publishing to the blog...")
        publisher.start()

        # Step 7: Give Flask server time to initialize
        print("⏳ Waiting for the server to start...")
        time.sleep(5)

    except Exception as e:
        print(f"❌ Error in pipeline: {e}")

    print("✅ Pipeline completed. Visit http://127.0.0.1:5000 to view the blog.")

if __name__ == "__main__":
    # Run the news agent every 10 minutes
    while True:
        run_news_agent()
        print("🕑 Waiting for 10 minutes before the next run...")
        time.sleep(600)  # 600 seconds = 10 minutes
