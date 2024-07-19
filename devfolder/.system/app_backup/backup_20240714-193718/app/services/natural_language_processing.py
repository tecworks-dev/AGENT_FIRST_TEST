
# app/services/natural_language_processing.py
"""
This module handles natural language processing tasks for the AI Software Factory application.
It provides services for keyword extraction, sentiment analysis, and text summarization.
"""

from typing import List, Dict
from app.utils.api_utils import AsyncAnthropic
import os
import traceback

# Set DEBUG to True for development purposes
DEBUG = True

class NLPService:
    def __init__(self):
        self.anthropic = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def extract_keywords(self, text: str) -> List[str]:
        """
        Extracts keywords from the given text using AI assistance.

        Args:
            text (str): The input text to extract keywords from.

        Returns:
            List[str]: A list of extracted keywords.
        """
        try:
            prompt = f"Extract the most important keywords from the following text:\n\n{text}\n\nKeywords:"
            response = await self.anthropic.completion(prompt=prompt, max_tokens_to_sample=100)
            keywords = response.completion.strip().split(', ')
            
            if DEBUG:
                print(f"Extracted keywords: {keywords}")
            
            return keywords
        except Exception as e:
            if DEBUG:
                print(f"Error in extract_keywords: {str(e)}")
                print(traceback.format_exc())
            return []

    async def sentiment_analysis(self, text: str) -> Dict[str, float]:
        """
        Performs sentiment analysis on the given text using AI assistance.

        Args:
            text (str): The input text to analyze for sentiment.

        Returns:
            Dict[str, float]: A dictionary containing sentiment scores (positive, negative, neutral).
        """
        try:
            prompt = f"Perform sentiment analysis on the following text and return scores for positive, negative, and neutral sentiments (values should sum to 1.0):\n\n{text}\n\nSentiment scores:"
            response = await self.anthropic.completion(prompt=prompt, max_tokens_to_sample=100)
            sentiment_scores = eval(response.completion.strip())
            
            if DEBUG:
                print(f"Sentiment analysis results: {sentiment_scores}")
            
            return sentiment_scores
        except Exception as e:
            if DEBUG:
                print(f"Error in sentiment_analysis: {str(e)}")
                print(traceback.format_exc())
            return {"positive": 0.0, "negative": 0.0, "neutral": 0.0}

    async def summarize_text(self, text: str, max_length: int) -> str:
        """
        Summarizes the given text using AI assistance, limiting the summary to the specified maximum length.

        Args:
            text (str): The input text to summarize.
            max_length (int): The maximum length of the summary in characters.

        Returns:
            str: The summarized text.
        """
        try:
            prompt = f"Summarize the following text in no more than {max_length} characters:\n\n{text}\n\nSummary:"
            response = await self.anthropic.completion(prompt=prompt, max_tokens_to_sample=max_length // 4)  # Assuming average token length of 4 characters
            summary = response.completion.strip()
            
            if DEBUG:
                print(f"Generated summary (length {len(summary)}): {summary}")
            
            return summary[:max_length]  # Ensure the summary doesn't exceed the max_length
        except Exception as e:
            if DEBUG:
                print(f"Error in summarize_text: {str(e)}")
                print(traceback.format_exc())
            return ""

# Example usage (for demonstration purposes)
if __name__ == "__main__":
    import asyncio

    async def main():
        nlp_service = NLPService()
        
        sample_text = "The AI Software Factory is an innovative project that combines artificial intelligence with software development processes. It aims to streamline coding, testing, and deployment tasks."
        
        keywords = await nlp_service.extract_keywords(sample_text)
        print("Keywords:", keywords)
        
        sentiment = await nlp_service.sentiment_analysis(sample_text)
        print("Sentiment:", sentiment)
        
        summary = await nlp_service.summarize_text(sample_text, max_length=100)
        print("Summary:", summary)

    asyncio.run(main())
