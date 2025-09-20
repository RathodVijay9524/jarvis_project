"""
NewsService.py
News aggregation from multiple sources with comprehensive coverage.
"""

import requests
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import re
from urllib.parse import quote_plus

class JarvisNewsService:
    """
    News aggregation service using multiple free sources:
    - RSS feeds from major news outlets
    - News APIs (free tiers)
    - Web scraping (educational purposes)
    - News categorization and filtering
    """
    
    def __init__(self):
        self.news_cache = {}
        self.cache_duration = 300  # 5 minutes
        
        # News sources and their RSS feeds
        self.news_sources = {
            'bbc': {
                'name': 'BBC News',
                'rss': 'http://feeds.bbci.co.uk/news/rss.xml',
                'categories': ['world', 'uk', 'business', 'technology', 'science', 'health']
            },
            'cnn': {
                'name': 'CNN',
                'rss': 'http://rss.cnn.com/rss/edition.rss',
                'categories': ['world', 'us', 'politics', 'business', 'technology']
            },
            'reuters': {
                'name': 'Reuters',
                'rss': 'https://feeds.reuters.com/reuters/topNews',
                'categories': ['world', 'business', 'technology', 'politics']
            },
            'guardian': {
                'name': 'The Guardian',
                'rss': 'https://www.theguardian.com/world/rss',
                'categories': ['world', 'uk', 'politics', 'business', 'technology']
            },
            'techcrunch': {
                'name': 'TechCrunch',
                'rss': 'https://techcrunch.com/feed/',
                'categories': ['technology', 'startups', 'business']
            },
            'ars_technica': {
                'name': 'Ars Technica',
                'rss': 'https://feeds.arstechnica.com/arstechnica/index/',
                'categories': ['technology', 'science', 'gaming']
            }
        }
        
        # News categories
        self.categories = {
            'world': '🌍 World News',
            'technology': '💻 Technology',
            'business': '💼 Business',
            'science': '🔬 Science',
            'health': '🏥 Health',
            'sports': '⚽ Sports',
            'entertainment': '🎬 Entertainment',
            'politics': '🏛️ Politics',
            'us': '🇺🇸 US News',
            'uk': '🇬🇧 UK News'
        }
    
    def get_latest_news(self, category: str = None, limit: int = 10) -> str:
        """
        Get latest news from multiple sources.
        """
        try:
            # Check cache
            cache_key = f"news:{category or 'all'}:{limit}"
            if cache_key in self.news_cache:
                cached_time, data = self.news_cache[cache_key]
                if time.time() - cached_time < self.cache_duration:
                    return self._format_news_response(data, category)
            
            # Collect news from multiple sources
            all_news = []
            
            for source_id, source_info in self.news_sources.items():
                try:
                    if category and category not in source_info['categories']:
                        continue
                    
                    news_items = self._get_news_from_source(source_id, source_info, limit)
                    all_news.extend(news_items)
                    
                except Exception as e:
                    print(f"⚠️ News source {source_id} failed: {e}")
                    continue
            
            # Sort by date and limit results
            all_news.sort(key=lambda x: x.get('published', ''), reverse=True)
            all_news = all_news[:limit]
            
            # Cache results
            self.news_cache[cache_key] = (time.time(), all_news)
            
            return self._format_news_response(all_news, category)
            
        except Exception as e:
            return f"❌ News error: {str(e)}"
    
    def _get_news_from_source(self, source_id: str, source_info: Dict[str, Any], limit: int) -> List[Dict[str, Any]]:
        """Get news from a specific source."""
        try:
            # Try RSS feed first
            rss_news = self._parse_rss_feed(source_info['rss'], source_info['name'], limit)
            if rss_news:
                return rss_news
            
            # Fallback to web scraping
            return self._scrape_news_website(source_id, source_info, limit)
            
        except Exception as e:
            print(f"⚠️ Failed to get news from {source_id}: {e}")
            return []
    
    def _parse_rss_feed(self, rss_url: str, source_name: str, limit: int) -> List[Dict[str, Any]]:
        """Parse RSS feed for news."""
        try:
            response = requests.get(rss_url, timeout=10)
            response.raise_for_status()
            
            # Simple RSS parsing (for educational purposes)
            content = response.text
            
            # Extract title, description, and link using regex
            title_pattern = r'<title><!\[CDATA\[(.*?)\]\]></title>|<title>(.*?)</title>'
            description_pattern = r'<description><!\[CDATA\[(.*?)\]\]></description>|<description>(.*?)</description>'
            link_pattern = r'<link><!\[CDATA\[(.*?)\]\]></link>|<link>(.*?)</link>'
            pubdate_pattern = r'<pubDate>(.*?)</pubDate>'
            
            titles = re.findall(title_pattern, content)
            descriptions = re.findall(description_pattern, content)
            links = re.findall(link_pattern, content)
            pubdates = re.findall(pubdate_pattern, content)
            
            news_items = []
            
            for i in range(min(limit, len(titles))):
                title = titles[i][0] or titles[i][1] if titles[i] else f"News item {i+1}"
                description = descriptions[i][0] or descriptions[i][1] if descriptions[i] else "No description available"
                link = links[i][0] or links[i][1] if links[i] else ""
                pubdate = pubdates[i] if i < len(pubdates) else ""
                
                # Clean up the content
                title = self._clean_html(title)
                description = self._clean_html(description)
                
                news_items.append({
                    'title': title,
                    'description': description,
                    'link': link,
                    'source': source_name,
                    'published': pubdate,
                    'category': 'general'
                })
            
            return news_items
            
        except Exception as e:
            print(f"⚠️ RSS parsing failed for {source_name}: {e}")
            return []
    
    def _scrape_news_website(self, source_id: str, source_info: Dict[str, Any], limit: int) -> List[Dict[str, Any]]:
        """Scrape news from website (fallback method)."""
        try:
            # This is a simplified example - in practice, you'd need specific selectors for each site
            base_urls = {
                'bbc': 'https://www.bbc.com/news',
                'cnn': 'https://www.cnn.com',
                'reuters': 'https://www.reuters.com',
                'guardian': 'https://www.theguardian.com/world',
                'techcrunch': 'https://techcrunch.com',
                'ars_technica': 'https://arstechnica.com'
            }
            
            base_url = base_urls.get(source_id)
            if not base_url:
                return []
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(base_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Simple headline extraction (this would need to be customized for each site)
            title_pattern = r'<h[1-6][^>]*>(.*?)</h[1-6]>'
            titles = re.findall(title_pattern, response.text)
            
            news_items = []
            for i, title in enumerate(titles[:limit]):
                clean_title = self._clean_html(title)
                if len(clean_title) > 10:  # Filter out very short titles
                    news_items.append({
                        'title': clean_title,
                        'description': f"Latest news from {source_info['name']}",
                        'link': base_url,
                        'source': source_info['name'],
                        'published': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'category': 'general'
                    })
            
            return news_items
            
        except Exception as e:
            print(f"⚠️ Web scraping failed for {source_id}: {e}")
            return []
    
    def _clean_html(self, text: str) -> str:
        """Clean HTML tags from text."""
        if not text:
            return ""
        
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', text)
        
        # Decode HTML entities
        clean = clean.replace('&amp;', '&')
        clean = clean.replace('&lt;', '<')
        clean = clean.replace('&gt;', '>')
        clean = clean.replace('&quot;', '"')
        clean = clean.replace('&#39;', "'")
        clean = clean.replace('&nbsp;', ' ')
        
        # Clean up whitespace
        clean = re.sub(r'\s+', ' ', clean).strip()
        
        return clean
    
    def _format_news_response(self, news_items: List[Dict[str, Any]], category: str = None) -> str:
        """Format news items into a readable response."""
        if not news_items:
            return f"❌ No news found for category: {category or 'all'}"
        
        # Header
        category_name = self.categories.get(category, '📰 All News') if category else '📰 Latest News'
        response = f"**{category_name}**\n\n"
        
        # News items
        for i, item in enumerate(news_items, 1):
            response += f"**{i}. {item['title']}**\n"
            
            if item.get('description'):
                description = item['description'][:200] + "..." if len(item['description']) > 200 else item['description']
                response += f"   📝 {description}\n"
            
            if item.get('source'):
                response += f"   📰 Source: {item['source']}\n"
            
            if item.get('published'):
                response += f"   🕒 Published: {item['published']}\n"
            
            if item.get('link'):
                response += f"   🔗 {item['link']}\n"
            
            response += "\n"
        
        # Footer with tips
        response += "💡 **News Tips:**\n"
        response += "   • Use specific categories: 'news technology', 'news business'\n"
        response += "   • Check multiple sources for balanced coverage\n"
        response += "   • Verify breaking news with official sources\n"
        response += "   • Stay informed but avoid information overload\n"
        
        return response
    
    def get_news_by_category(self, category: str, limit: int = 5) -> str:
        """Get news for a specific category."""
        try:
            if category not in self.categories:
                available_categories = ", ".join(self.categories.keys())
                return f"❌ Unknown category '{category}'. Available categories: {available_categories}"
            
            return self.get_latest_news(category, limit)
            
        except Exception as e:
            return f"❌ Category news error: {str(e)}"
    
    def get_breaking_news(self) -> str:
        """Get breaking news alerts."""
        try:
            # Get latest news with higher priority for breaking news
            news_items = []
            
            # Try to get breaking news from multiple sources
            for source_id, source_info in list(self.news_sources.items())[:3]:  # Top 3 sources
                try:
                    items = self._get_news_from_source(source_id, source_info, 3)
                    news_items.extend(items)
                except:
                    continue
            
            # Filter for potentially breaking news (keywords)
            breaking_keywords = ['breaking', 'urgent', 'alert', 'emergency', 'crisis', 'attack', 'accident', 'disaster']
            breaking_news = []
            
            for item in news_items:
                title_lower = item['title'].lower()
                if any(keyword in title_lower for keyword in breaking_keywords):
                    breaking_news.append(item)
            
            if breaking_news:
                response = "🚨 **BREAKING NEWS** 🚨\n\n"
                for i, item in enumerate(breaking_news[:5], 1):
                    response += f"**{i}. {item['title']}**\n"
                    response += f"   📰 Source: {item['source']}\n"
                    response += f"   🕒 Published: {item['published']}\n"
                    if item.get('link'):
                        response += f"   🔗 {item['link']}\n"
                    response += "\n"
                
                response += "⚠️ **Verify breaking news with official sources**"
                return response
            else:
                return "✅ No breaking news alerts at this time."
                
        except Exception as e:
            return f"❌ Breaking news error: {str(e)}"
    
    def search_news(self, query: str, limit: int = 5) -> str:
        """Search for news articles by keyword."""
        try:
            # Use DuckDuckGo for news search
            search_url = "https://api.duckduckgo.com/"
            params = {
                'q': f"{query} news",
                'format': 'json',
                'no_html': '1'
            }
            
            response = requests.get(search_url, params=params, timeout=10)
            data = response.json()
            
            news_items = []
            
            # Extract news from related topics
            for topic in data.get('RelatedTopics', [])[:limit]:
                if isinstance(topic, dict) and 'Text' in topic:
                    news_items.append({
                        'title': topic.get('FirstURL', '').split('/')[-1].replace('_', ' '),
                        'description': topic.get('Text', ''),
                        'link': topic.get('FirstURL', ''),
                        'source': 'DuckDuckGo News',
                        'published': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'category': 'search'
                    })
            
            if news_items:
                response_text = f"🔍 **News Search Results for: {query}**\n\n"
                for i, item in enumerate(news_items, 1):
                    response_text += f"**{i}. {item['title']}**\n"
                    response_text += f"   📝 {item['description']}\n"
                    response_text += f"   🔗 {item['link']}\n\n"
                return response_text
            else:
                return f"❌ No news found for query: {query}"
                
        except Exception as e:
            return f"❌ News search error: {str(e)}"
    
    def get_news_summary(self, category: str = None) -> str:
        """Get a summary of top news stories."""
        try:
            news_items = self.get_latest_news(category, 5)
            
            if news_items.startswith("❌"):
                return news_items
            
            # Add summary statistics
            summary = f"📊 **News Summary**\n\n"
            summary += f"📰 **Total Sources:** {len(self.news_sources)}\n"
            summary += f"🌍 **Categories Available:** {', '.join(self.categories.keys())}\n"
            summary += f"🕒 **Last Updated:** {datetime.now().strftime('%H:%M:%S')}\n\n"
            
            summary += news_items
            
            return summary
            
        except Exception as e:
            return f"❌ News summary error: {str(e)}"
    
    def get_available_categories(self) -> str:
        """Get list of available news categories."""
        response = "📰 **Available News Categories:**\n\n"
        
        for category, display_name in self.categories.items():
            response += f"   • **{category}** - {display_name}\n"
        
        response += "\n💡 **Usage:**\n"
        response += "   • 'news technology' - Get technology news\n"
        response += "   • 'news business' - Get business news\n"
        response += "   • 'news world' - Get world news\n"
        response += "   • 'breaking news' - Get breaking news alerts\n"
        response += "   • 'search news [keyword]' - Search for specific news\n"
        
        return response
