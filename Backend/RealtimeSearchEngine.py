"""
RealtimeSearchEngine.py
Advanced real-time search engine for JARVIS with web search, news, and weather capabilities.
"""

import requests
import json
import os
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import re

# Import enhanced services
try:
    from .EnhancedSearchEngine import JarvisEnhancedSearch
    from .WeatherService import JarvisWeatherService
    from .NewsService import JarvisNewsService
    from .FinancialDataService import JarvisFinancialDataService
    from .TranslationService import JarvisTranslationService
    ENHANCED_SERVICES_AVAILABLE = True
except ImportError:
    ENHANCED_SERVICES_AVAILABLE = False
    print("⚠️ Enhanced services not available")
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
        
        # Initialize enhanced services
        if ENHANCED_SERVICES_AVAILABLE:
            self.enhanced_search = JarvisEnhancedSearch()
            self.weather_service = JarvisWeatherService()
            self.news_service = JarvisNewsService()
            self.financial_service = JarvisFinancialDataService()
            self.translation_service = JarvisTranslationService()
            print("✅ Enhanced search services initialized")
        else:
            self.enhanced_search = None
            self.weather_service = None
            self.news_service = None
            self.financial_service = None
            self.translation_service = None
    
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
    
    def get_weather(self, location: str = None) -> str:
        """Get weather information using enhanced weather service."""
        try:
            if self.weather_service:
                return self.weather_service.get_weather(location)
            else:
                return "❌ Weather service not available. Enhanced services not loaded."
        except Exception as e:
            return f"❌ Weather error: {str(e)}"
    
    def get_news(self, category: str = None, limit: int = 10) -> str:
        """Get news using enhanced news service."""
        try:
            if self.news_service:
                if category:
                    return self.news_service.get_news_by_category(category, limit)
                else:
                    return self.news_service.get_latest_news(limit=limit)
            else:
                return "❌ News service not available. Enhanced services not loaded."
        except Exception as e:
            return f"❌ News error: {str(e)}"
    
    def get_stock_price(self, symbol: str) -> str:
        """Get stock price using enhanced financial service."""
        try:
            if self.financial_service:
                return self.financial_service.get_stock_price(symbol)
            else:
                return "❌ Financial service not available. Enhanced services not loaded."
        except Exception as e:
            return f"❌ Stock price error: {str(e)}"
    
    def get_crypto_price(self, symbol: str) -> str:
        """Get cryptocurrency price using enhanced financial service."""
        try:
            if self.financial_service:
                return self.financial_service.get_crypto_price(symbol)
            else:
                return "❌ Financial service not available. Enhanced services not loaded."
        except Exception as e:
            return f"❌ Cryptocurrency price error: {str(e)}"
    
    def get_market_summary(self) -> str:
        """Get market summary using enhanced financial service."""
        try:
            if self.financial_service:
                return self.financial_service.get_market_summary()
            else:
                return "❌ Financial service not available. Enhanced services not loaded."
        except Exception as e:
            return f"❌ Market summary error: {str(e)}"
    
    def get_sports_scores(self, league: str = None, team: str = None) -> str:
        """Get sports scores using enhanced financial service."""
        try:
            if self.financial_service:
                return self.financial_service.get_sports_scores(league, team)
            else:
                return "❌ Sports service not available. Enhanced services not loaded."
        except Exception as e:
            return f"❌ Sports scores error: {str(e)}"
    
    def translate_text(self, text: str, target_language: str, source_language: str = 'auto') -> str:
        """Translate text using enhanced translation service."""
        try:
            if self.translation_service:
                return self.translation_service.translate_text(text, target_language, source_language)
            else:
                return "❌ Translation service not available. Enhanced services not loaded."
        except Exception as e:
            return f"❌ Translation error: {str(e)}"
    
    def detect_language(self, text: str) -> str:
        """Detect language using enhanced translation service."""
        try:
            if self.translation_service:
                return self.translation_service.detect_language(text)
            else:
                return "❌ Translation service not available. Enhanced services not loaded."
        except Exception as e:
            return f"❌ Language detection error: {str(e)}"
    
    def get_enhanced_capabilities(self) -> str:
        """Get list of enhanced capabilities."""
        if not ENHANCED_SERVICES_AVAILABLE:
            return "❌ Enhanced services not available."
        
        capabilities = """🚀 **Enhanced JARVIS Search Capabilities**

🔍 **Enhanced Web Search:**
   • Multiple search sources (DuckDuckGo, Google, Bing)
   • Better result formatting with snippets
   • Rich search results with metadata
   • Search suggestions and autocomplete

🌤️ **Weather Integration:**
   • Real-time weather data from free APIs
   • Multiple weather sources (Open-Meteo, WeatherAPI)
   • 3-day weather forecasts
   • Weather alerts and conditions
   • Location-based weather (auto-detect or specify)

📰 **News Aggregation:**
   • Multiple news sources (BBC, CNN, Reuters, Guardian)
   • Category-based news (technology, business, world)
   • Breaking news alerts
   • News search by keywords
   • RSS feed parsing for latest updates

💰 **Financial Data:**
   • Stock prices and market data
   • Cryptocurrency prices and trends
   • Market summaries (S&P 500, Dow Jones, NASDAQ)
   • Sports scores and schedules
   • Financial tips and information

🌍 **Translation Services:**
   • Real-time text translation
   • 50+ supported languages
   • Language detection
   • Multiple translation services
   • Common phrase translations

💡 **Usage Examples:**
   • 'search artificial intelligence'
   • 'weather in London'
   • 'news technology'
   • 'stock price AAPL'
   • 'crypto price bitcoin'
   • 'translate hello to spanish'
   • 'sports scores nfl'
   • 'market summary'
"""
        return capabilities
    
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