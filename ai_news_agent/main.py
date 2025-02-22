import time
import schedule
import logging
from database import init_db
from searcher import Searcher
from summarizer import Summarizer
from seo_optimizer import SEOOptimizer
from publisher import Publisher

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_pipeline():
    """Run the full AI news agent pipeline."""
    logging.info(f"Starting pipeline run at {time.ctime()}")

    try:
        # Step 1: Fetch and Crawl News Data
        searcher = Searcher()

        logging.info("Crawling the web for news...")
        search_topic = "Uttar Pradesh"  # Change if needed
        searcher.crawl_news(search_topic)

        # Step 2: Summarization
        summarizer = Summarizer()
        logging.info("Summarizing articles...")
        summarizer.process_articles()

        # Step 3: SEO Optimization
        optimizer = SEOOptimizer()
        logging.info("Optimizing articles for SEO...")
        optimizer.optimize_articles()

        # Step 4: Publishing Articles
        logging.info("Publishing articles to the blog...")
        publisher = Publisher()
        publisher.publish_articles()  # Only publishing, no new Flask instance

    except Exception as e:
        logging.error(f"Pipeline execution failed: {e}")


def setup_scheduler(run_interval=10):
    """Set up the pipeline to run periodically."""
    schedule.every(run_interval).minutes.do(run_pipeline)
    logging.info(f"Scheduler set up to run pipeline every {run_interval} minutes.")


def run_news_agent():
    """Initialize and run the AI News Agent."""
    logging.info("Starting the AI News Agent...")

    # Initialize database
    init_db()

    # Run the pipeline once immediately
    run_pipeline()

    # Set up and start the scheduler
    setup_scheduler(run_interval=10)  # Change interval for testing

    # Keep script running for scheduling
    while True:
        schedule.run_pending()
        time.sleep(1)  # Check every second


if __name__ == "__main__":
    run_news_agent()
