# # summarizer.py
# import sqlite3
# import nltk
# from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.corpus import stopwords
# from heapq import nlargest

# class Summarizer:
#     def __init__(self, db_path="news.db"):
#         self.db_path = db_path
#         nltk.download('punkt')  # Ensure tokenizer is available
#         nltk.download('stopwords')  # Ensure stopwords are available

#     def summarize_text(self, raw_text, summary_length=3):
#         """Generate a summary from raw text using sentence scoring."""
#         if not raw_text or len(raw_text.strip()) == 0:
#             return "No content available to summarize."
        
#         # Tokenize into sentences
#         sentences = sent_tokenize(raw_text)
#         if len(sentences) <= summary_length:
#             return " ".join(sentences)  # Return full text if too short
        
#         # Tokenize into words and remove stopwords
#         stop_words = set(stopwords.words('english'))
#         words = word_tokenize(raw_text.lower())
#         word_freq = {}
#         for word in words:
#             if word not in stop_words and word.isalnum():
#                 word_freq[word] = word_freq.get(word, 0) + 1
        
#         # Score sentences based on word frequency
#         sentence_scores = {}
#         for sentence in sentences:
#             for word, freq in word_freq.items():
#                 if word in sentence.lower():
#                     sentence_scores[sentence] = sentence_scores.get(sentence, 0) + freq
        
#         # Select top N sentences
#         summary_sentences = nlargest(summary_length, sentence_scores, key=sentence_scores.get)
#         summary = " ".join(summary_sentences)
#         return summary

#     def process_articles(self):
#         """Summarize all unsummarized articles in the database."""
#         conn = sqlite3.connect(self.db_path)
#         c = conn.cursor()
        
#         # Fetch articles without summaries
#         c.execute("SELECT id, raw_text FROM articles WHERE summary IS NULL")
#         articles = c.fetchall()
        
#         for article_id, raw_text in articles:
#             summary = self.summarize_text(raw_text)
#             c.execute("UPDATE articles SET summary = ? WHERE id = ?", (summary, article_id))
#             print(f"Summarized article ID {article_id}: {summary[:50]}...")
        
#         conn.commit()
#         conn.close()

# if __name__ == "__main__":
#     # Test the Summarizer
#     summarizer = Summarizer()
#     print("Testing summarizer with sample text...")
#     sample_text = "A daring robbery occurred in Lucknow yesterday. Thieves stole gold from a shop in broad daylight. Police are investigating this shocking crime. The city is on high alert after the incident."
#     summary = summarizer.summarize_text(sample_text)
#     print(f"Summary: {summary}")
    
#     print("\nProcessing articles from database...")
#     summarizer.process_articles()



# summarizer.py
import sqlite3
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from heapq import nlargest

class Summarizer:
    def __init__(self, db_path="news.db"):
        self.db_path = db_path
        nltk.download('punkt')
        nltk.download('stopwords')

    def summarize_text(self, raw_text, summary_length=3):
        """Generate a summary from raw text."""
        if not raw_text or len(raw_text.strip()) == 0:
            return "No content available to summarize."
        
        sentences = sent_tokenize(raw_text)
        if len(sentences) <= summary_length:
            return " ".join(sentences)
        
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(raw_text.lower())
        word_freq = {}
        for word in words:
            if word not in stop_words and word.isalnum():
                word_freq[word] = word_freq.get(word, 0) + 1
        
        sentence_scores = {}
        for sentence in sentences:
            for word, freq in word_freq.items():
                if word in sentence.lower():
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + freq
        
        summary_sentences = nlargest(summary_length, sentence_scores, key=sentence_scores.get)
        return " ".join(summary_sentences)

    def process_articles(self):
        """Summarize all unsummarized articles in the database."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT id, raw_text FROM articles WHERE summary IS NULL OR summary = ''")
        articles = c.fetchall()
        
        for article_id, raw_text in articles:
            summary = self.summarize_text(raw_text)
            c.execute("UPDATE articles SET summary = ? WHERE id = ?", (summary, article_id))
            print(f"Summarized article ID {article_id}: {summary[:50]}...")

        conn.commit()
        conn.close()

if __name__ == "__main__":
    summarizer = Summarizer()
    print("\nSummarizing articles from the database...")
    summarizer.process_articles()
