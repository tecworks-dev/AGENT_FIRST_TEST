
# app/services/web_browsing_service.py
"""
Implements web browsing functionality for research.

This module provides a WebBrowsingService class that offers methods for searching the web,
extracting content from webpages, and summarizing the extracted content using AI assistance.
"""

from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from app.utils.api_utils import AsyncAnthropic
import os
import traceback

DEBUG = True

class WebBrowsingService:
    def __init__(self):
        self.anthropic_client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    async def search(self, query: str) -> List[Dict[str, str]]:
        """
        Perform a web search based on the given query.

        Args:
            query (str): The search query.

        Returns:
            List[Dict[str, str]]: A list of search results, each containing 'title' and 'url'.
        """
        try:
            # For demonstration purposes, we'll use a mock search result
            # In a real implementation, you would integrate with a search API
            mock_results = [
                {"title": "Example Result 1", "url": "https://example.com/1"},
                {"title": "Example Result 2", "url": "https://example.com/2"},
                {"title": "Example Result 3", "url": "https://example.com/3"},
            ]
            
            if DEBUG:
                print(f"Search query: {query}")
                print(f"Search results: {mock_results}")
            
            return mock_results
        except Exception as e:
            if DEBUG:
                print(f"Error in search method: {str(e)}")
                print(traceback.format_exc())
            raise

    async def extract_content(self, url: str) -> str:
        """
        Extract the main content from the given URL.

        Args:
            url (str): The URL to extract content from.

        Returns:
            str: The extracted main content.
        """
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # This is a simple extraction method and might need to be improved
            # for better accuracy across different website structures
            main_content = soup.find('body').get_text(strip=True)
            
            if DEBUG:
                print(f"Extracted content from {url}: {main_content[:100]}...")
            
            return main_content
        except Exception as e:
            if DEBUG:
                print(f"Error in extract_content method: {str(e)}")
                print(traceback.format_exc())
            raise

    async def summarize(self, content: str) -> str:
        """
        Summarize the given content using AI assistance.

        Args:
            content (str): The content to summarize.

        Returns:
            str: A summary of the content.
        """
        try:
            prompt = f"Please summarize the following content in a concise manner:\n\n{content}"
            
            response = await self.anthropic_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            
            summary = response.content[0].text
            
            if DEBUG:
                print(f"Generated summary: {summary}")
            
            return summary
        except Exception as e:
            if DEBUG:
                print(f"Error in summarize method: {str(e)}")
                print(traceback.format_exc())
            raise

# Example usage (for demonstration purposes)
if __name__ == "__main__":
    import asyncio

    async def main():
        web_service = WebBrowsingService()
        query = "AI in software development"
        search_results = await web_service.search(query)
        print(f"Search results for '{query}':")
        for result in search_results:
            print(f"- {result['title']}: {result['url']}")
        
        if search_results:
            content = await web_service.extract_content(search_results[0]['url'])
            summary = await web_service.summarize(content)
            print(f"\nSummary of first result:\n{summary}")

    asyncio.run(main())
