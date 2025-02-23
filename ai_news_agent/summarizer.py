import sqlite3
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import random

class Summarizer:
    def __init__(self, db_path="news.db"):
        self.db_path = db_path
        nltk.download("punkt")
        nltk.download("stopwords")

    def create_blog_post(self, raw_texts, topic, sub_topic):
        """Generate a well-structured, engaging blog post."""
        if not raw_texts:
            return "No data available for this topic."

        # Combine raw texts and tokenize
        combined_text = " ".join(raw_texts)
        sentences = sent_tokenize(combined_text)
        stop_words = set(stopwords.words("english"))

        # Extract keywords
        words = [
            w for w in word_tokenize(combined_text.lower())
            if w.isalnum() and w not in stop_words
        ]
        word_freq = nltk.FreqDist(words)
        top_keywords = [word for word, freq in word_freq.most_common(10)]

        # Blog Post Components
        seo_title = f"{sub_topic}: A Deep Dive into {topic} Latest Updates"
        meta_description = f"Explore the latest developments on {sub_topic} in {topic}. "
        meta_description += f"Read insights, expert opinions, and key takeaways from recent reports."

        # Introduction
        intro = (
            f"### {seo_title}\n\n"
            f"📅 **Date**: 2025-02-22  \n"
            f"🔍 **Keywords**: {', '.join(top_keywords[:5])}\n\n"
            f"#### **Introduction**\n"
            f"The city of **{sub_topic}, {topic}**, has been making headlines recently. "
            f"From economic changes to social developments, there's a lot happening. "
            f"This article summarizes the most crucial updates you need to know.\n\n"
        )

        # Extract meaningful content
        body = "#### **Key Highlights**\n"
        selected_sentences = random.sample(sentences, min(10, len(sentences)))
        for i, sent in enumerate(selected_sentences):
            body += f"- **{i+1}.** {sent}\n"

        # Adding a quote for engagement
        quote = (
            "\n> *'Change is the only constant. Understanding these events helps us shape a better future.'* - Unknown\n\n"
        )

        # Adding tweet embed placeholder (can be replaced with real tweets)
        tweet_embed = (
            "#### **Public Reactions**\n"
            "_Here's what people are saying:_\n\n"
            "📢 **[Tweet Embed Placeholder]**\n\n"
        )

        # Adding an image placeholder
        image_embed = "![Illustration](https://via.placeholder.com/800x400?text=News+Image)\n\n"

        # Conclusion
        conclusion = (
            "#### **Conclusion**\n"
            f"As events in **{sub_topic}** continue to unfold, it’s essential to stay informed. "
            "We will keep updating this space with more details as they emerge. "
            "Feel free to share your thoughts in the comments below!\n\n"
        )

        # Full Blog Post
        full_post = intro + image_embed + body + quote + tweet_embed + conclusion
        return seo_title, meta_description, full_post

    def process_articles(self, topic, sub_topic):
        """Process raw articles into a structured blog post."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute(
            "SELECT raw_text FROM articles WHERE topic = ? AND sub_topic = ? AND full_post IS NULL",
            (topic, sub_topic),
        )
        raw_texts = [row[0] for row in c.fetchall()]

        if raw_texts:
            seo_title, meta_description, full_post = self.create_blog_post(
                raw_texts, topic, sub_topic
            )

            # Delete old unprocessed articles
            c.execute("DELETE FROM articles WHERE topic = ? AND sub_topic = ?", (topic, sub_topic))

            # Insert formatted blog post
            c.execute(
                """
                INSERT INTO articles (topic, sub_topic, seo_title, full_post, date, seo_keywords, meta_description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    topic,
                    sub_topic,
                    seo_title,
                    full_post,
                    "2025-02-22",
                    ", ".join(seo_title.split()),
                    meta_description,
                ),
            )

            print(f"Generated blog post for {sub_topic}")

        conn.commit()
        conn.close()


if __name__ == "__main__":
    summarizer = Summarizer()
    summarizer.process_articles("Uttar Pradesh", "Lucknow")
