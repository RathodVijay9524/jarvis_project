"""
RealtimeSearchEngine.py
Advanced real-time search engine for JARVIS with web search, news, and weather capabilities.
"""

import requests
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
from bs4 import BeautifulSoup
from googlesearch import search
from dotenv import load_dotenv

load_dotenv()

class JarvisSearch:
    def __init__(self):
        self.news_api_key = os.getenv("NEWS_API_KEY")
        self.weather_api_key = os.getenv("WEATHER_API_KEY")
        
        # User agent for web scraping
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search_web(self, query: str, num_results: int = 5) -> str:
        """
        Perform web search and return formatted results.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            str: Formatted search results
        """
        try:
            print(f"🔍 Searching the web for: {query}")
            
            # Use Google search
            search_results = []
            
            for url in search(query, num_results=num_results, stop=num_results):
                try:
                    # Get page title and snippet
                    response = requests.get(url, headers=self.headers, timeout=5)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    title = soup.find('title')
                    title = title.text.strip() if title else "No title"
                    
                    # Get meta description or first paragraph
                    description = soup.find('meta', attrs={'name': 'description'})
                    if description:
                        snippet = description.get('content', '')
                    else:
                        # Try to get first paragraph
                        p_tags = soup.find_all('p')
                        snippet = p_tags[0].text.strip() if p_tags else "No description available"
                    
                    # Limit snippet length
                    snippet = snippet[:200] + "..." if len(snippet) > 200 else snippet
                    
                    search_results.append({
                        'title': title,
                        'url': url,
                        'snippet': snippet
                    })
                    
                except Exception as e:
                    # Skip problematic URLs
                    continue
            
            # Format results
            if search_results:
                result = f"🔍 Web search results for '{query}':\n\n"
                for i, item in enumerate(search_results, 1):
                    result += f"{i}. **{item['title']}**\n"
                    result += f"   {item['snippet']}\n"
                    result += f"   🔗 {item['url']}\n\n"
                
                return result.strip()
            else:
                return f"❌ No search results found for '{query}'"
                
        except Exception as e:
            return f"❌ Search error: {str(e)}"
    
    def get_news(self, topic: str = "general") -> str:
        """
        Get latest news on a topic.
        
        Args:
            topic: News topic or category
            
        Returns:
            str: Formatted news results
        """
        try:
            # Search for news articles
            query = f"{topic} news"
            search_results = []
            
            for url in search(query, num_results=5):
                if any(domain in url for domain in ['news', 'bbc', 'cnn', 'reuters', 'ap']):
                    try:
                        response = requests.get(url, headers=self.headers, timeout=5)
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        title = soup.find('title')
                        title = title.text.strip() if title else "No title"
                        
                        search_results.append({
                            'title': title,
                            'url': url
                        })
                        
                        if len(search_results) >= 3:
                            break
                            
                    except:
                        continue
            
            if search_results:
                result = f"📰 Latest news about '{topic}':\n\n"
                for i, item in enumerate(search_results, 1):
                    result += f"{i}. {item['title']}\n"
                    result += f"   🔗 {item['url']}\n\n"
                
                return result.strip()
            else:
                return f"❌ No news found for '{topic}'"
                
        except Exception as e:
            return f"❌ News retrieval error: {str(e)}"
    
    def get_weather(self, location: str) -> str:
        """
        Get weather information for a location.
        
        Args:
            location: City name or location
            
        Returns:
            str: Weather information
        """
        try:
            # Use weather.com or similar
            query = f"weather {location}"
            for url in search(query, num_results=3):
                if 'weather' in url.lower():
                    try:
                        response = requests.get(url, headers=self.headers, timeout=5)
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Try to extract basic weather info
                        title = soup.find('title')
                        if title and 'weather' in title.text.lower():
                            return f"🌤️ Weather information for {location}:\n🔗 {url}"
                            
                    except:
                        continue
            
            return f"❌ Could not retrieve weather for '{location}'. Please try again or check the location name."
            
        except Exception as e:
            return f"❌ Weather retrieval error: {str(e)}"

# Convenience functions for backward compatibility
def index_documents(path: str):
    """Index documents (placeholder for future implementation)."""
    print(f"📁 Indexing documents in {path}")

def query_index(query: str) -> List[str]:
    """Query document index (placeholder for future implementation)."""
    return [f"Document snippet for '{query}' - Feature coming soon!"]

if __name__ == "__main__":
    # Test search functionality
    search_engine = JarvisSearch()
    
    print("Testing JARVIS Search Engine...")
    
    # Test web search
    print("\n1. Web Search Test:")
    result = search_engine.search_web("artificial intelligence", 3)
    print(result)
    
    # Test weather
    print("\n2. Weather Test:")
    result = search_engine.get_weather("New York")
    print(result)
    
    # Test news
    print("\n3. News Test:")
    result = search_engine.get_news("technology")
    print(result)
    
    print("\nSearch engine testing complete!")