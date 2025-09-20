"""
EnhancedSearchEngine.py
Enhanced web search with better results formatting and multiple search sources.
"""

import requests
import json
import time
from typing import Dict, List, Any, Optional
from urllib.parse import quote_plus
import re

class JarvisEnhancedSearch:
    """
    Enhanced search engine with:
    - Multiple search sources
    - Better result formatting
    - Rich snippets and summaries
    - Search result ranking
    - Cached results
    """
    
    def __init__(self):
        self.search_sources = [
            'duckduckgo',  # Primary - no API key needed
            'google',      # Fallback - using scraping
            'bing'         # Alternative
        ]
        
        # Search result cache
        self.search_cache = {}
        self.cache_duration = 300  # 5 minutes
        
        # User agents for web scraping
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
    
    def search(self, query: str, max_results: int = 5) -> str:
        """
        Enhanced search with better formatting and multiple sources.
        """
        try:
            # Check cache first
            cache_key = f"search:{hash(query)}"
            if cache_key in self.search_cache:
                cached_time, results = self.search_cache[cache_key]
                if time.time() - cached_time < self.cache_duration:
                    return self._format_search_results(query, results)
            
            # Try multiple search sources
            results = []
            for source in self.search_sources:
                try:
                    if source == 'duckduckgo':
                        results = self._search_duckduckgo(query, max_results)
                    elif source == 'google':
                        results = self._search_google(query, max_results)
                    elif source == 'bing':
                        results = self._search_bing(query, max_results)
                    
                    if results:
                        break
                        
                except Exception as e:
                    print(f"⚠️ Search source {source} failed: {e}")
                    continue
            
            if not results:
                return f"❌ Unable to find results for '{query}'. Please try a different search term."
            
            # Cache results
            self.search_cache[cache_key] = (time.time(), results)
            
            return self._format_search_results(query, results)
            
        except Exception as e:
            return f"❌ Search error: {str(e)}"
    
    def _search_duckduckgo(self, query: str, max_results: int) -> List[Dict[str, str]]:
        """Search using DuckDuckGo (no API key required)."""
        try:
            # DuckDuckGo Instant Answer API
            url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            results = []
            
            # Instant Answer
            if data.get('Abstract'):
                results.append({
                    'title': data.get('Heading', query),
                    'snippet': data.get('Abstract', ''),
                    'url': data.get('AbstractURL', ''),
                    'source': 'DuckDuckGo Instant Answer',
                    'type': 'instant_answer'
                })
            
            # Related Topics
            for topic in data.get('RelatedTopics', [])[:max_results]:
                if isinstance(topic, dict) and 'Text' in topic:
                    results.append({
                        'title': topic.get('FirstURL', '').split('/')[-1].replace('_', ' '),
                        'snippet': topic.get('Text', ''),
                        'url': topic.get('FirstURL', ''),
                        'source': 'DuckDuckGo',
                        'type': 'related_topic'
                    })
            
            return results[:max_results]
            
        except Exception as e:
            print(f"⚠️ DuckDuckGo search failed: {e}")
            return []
    
    def _search_google(self, query: str, max_results: int) -> List[Dict[str, str]]:
        """Search using Google (web scraping)."""
        try:
            # Simple Google search scraping (educational purposes)
            search_url = f"https://www.google.com/search?q={quote_plus(query)}"
            
            headers = {
                'User-Agent': self.user_agents[0],
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            # Parse basic results (simplified)
            results = []
            
            # Extract title and snippet patterns (basic regex)
            title_pattern = r'<h3[^>]*><a[^>]*>([^<]+)</a></h3>'
            snippet_pattern = r'<span[^>]*class="[^"]*st[^"]*"[^>]*>([^<]+)</span>'
            
            titles = re.findall(title_pattern, response.text)
            snippets = re.findall(snippet_pattern, response.text)
            
            for i, title in enumerate(titles[:max_results]):
                snippet = snippets[i] if i < len(snippets) else 'No description available'
                results.append({
                    'title': title,
                    'snippet': snippet,
                    'url': f"https://www.google.com/search?q={quote_plus(query)}",
                    'source': 'Google',
                    'type': 'web_result'
                })
            
            return results
            
        except Exception as e:
            print(f"⚠️ Google search failed: {e}")
            return []
    
    def _search_bing(self, query: str, max_results: int) -> List[Dict[str, str]]:
        """Search using Bing (web scraping)."""
        try:
            search_url = f"https://www.bing.com/search?q={quote_plus(query)}"
            
            headers = {
                'User-Agent': self.user_agents[1],
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            # Parse Bing results (simplified)
            results = []
            
            # Basic parsing for Bing results
            title_pattern = r'<h2><a[^>]*href="([^"]*)"[^>]*>([^<]+)</a></h2>'
            matches = re.findall(title_pattern, response.text)
            
            for i, (url, title) in enumerate(matches[:max_results]):
                results.append({
                    'title': title,
                    'snippet': f'Search result for: {query}',
                    'url': url,
                    'source': 'Bing',
                    'type': 'web_result'
                })
            
            return results
            
        except Exception as e:
            print(f"⚠️ Bing search failed: {e}")
            return []
    
    def _format_search_results(self, query: str, results: List[Dict[str, str]]) -> str:
        """Format search results with rich formatting."""
        if not results:
            return f"❌ No results found for '{query}'"
        
        formatted = f"🔍 **Search Results for: {query}**\n\n"
        
        for i, result in enumerate(results, 1):
            # Format based on result type
            if result.get('type') == 'instant_answer':
                formatted += f"✨ **{result['title']}**\n"
                formatted += f"   {result['snippet']}\n"
                if result.get('url'):
                    formatted += f"   📖 Source: {result['url']}\n"
                formatted += "\n"
            else:
                formatted += f"**{i}. {result['title']}**\n"
                formatted += f"   📝 {result['snippet']}\n"
                if result.get('url'):
                    formatted += f"   🔗 {result['url']}\n"
                formatted += f"   📊 Source: {result['source']}\n\n"
        
        # Add search tips
        formatted += "💡 **Search Tips:**\n"
        formatted += "   • Use quotes for exact phrases: \"artificial intelligence\"\n"
        formatted += "   • Add site: for specific sites: site:github.com python\n"
        formatted += "   • Use - to exclude terms: python -snake\n"
        
        return formatted
    
    def search_news(self, query: str, max_results: int = 5) -> str:
        """Search for news articles."""
        try:
            # Use DuckDuckGo for news
            url = "https://api.duckduckgo.com/"
            params = {
                'q': f"{query} news",
                'format': 'json',
                'no_html': '1'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            results = []
            
            # Check for news in related topics
            for topic in data.get('RelatedTopics', [])[:max_results]:
                if isinstance(topic, dict) and 'Text' in topic:
                    results.append({
                        'title': topic.get('FirstURL', '').split('/')[-1].replace('_', ' '),
                        'snippet': topic.get('Text', ''),
                        'url': topic.get('FirstURL', ''),
                        'source': 'DuckDuckGo News',
                        'type': 'news'
                    })
            
            if results:
                formatted = f"📰 **News Results for: {query}**\n\n"
                for i, result in enumerate(results, 1):
                    formatted += f"**{i}. {result['title']}**\n"
                    formatted += f"   📝 {result['snippet']}\n"
                    formatted += f"   🔗 {result['url']}\n\n"
                return formatted
            else:
                return f"❌ No news found for '{query}'"
                
        except Exception as e:
            return f"❌ News search error: {str(e)}"
    
    def search_images(self, query: str, max_results: int = 5) -> str:
        """Search for images."""
        try:
            # Use DuckDuckGo for images
            url = "https://api.duckduckgo.com/"
            params = {
                'q': f"{query} images",
                'format': 'json',
                'no_html': '1'
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            results = []
            
            # Check for image results
            for topic in data.get('RelatedTopics', [])[:max_results]:
                if isinstance(topic, dict) and 'Text' in topic:
                    results.append({
                        'title': topic.get('FirstURL', '').split('/')[-1].replace('_', ' '),
                        'url': topic.get('FirstURL', ''),
                        'source': 'DuckDuckGo Images'
                    })
            
            if results:
                formatted = f"🖼️ **Image Results for: {query}**\n\n"
                for i, result in enumerate(results, 1):
                    formatted += f"**{i}. {result['title']}**\n"
                    formatted += f"   🔗 {result['url']}\n\n"
                return formatted
            else:
                return f"❌ No images found for '{query}'"
                
        except Exception as e:
            return f"❌ Image search error: {str(e)}"
    
    def get_search_suggestions(self, query: str) -> List[str]:
        """Get search suggestions for a query."""
        try:
            # Use DuckDuckGo for suggestions
            url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1'
            }
            
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            suggestions = []
            
            # Get suggestions from related topics
            for topic in data.get('RelatedTopics', [])[:5]:
                if isinstance(topic, dict) and 'Text' in topic:
                    title = topic.get('FirstURL', '').split('/')[-1].replace('_', ' ')
                    if title and len(title) > 3:
                        suggestions.append(title)
            
            return suggestions[:5]
            
        except Exception as e:
            print(f"⚠️ Search suggestions failed: {e}")
            return []
