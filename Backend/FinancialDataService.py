"""
FinancialDataService.py
Financial data service for stocks, cryptocurrency, and sports scores.
"""

import requests
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import re

class JarvisFinancialDataService:
    """
    Financial data service providing:
    - Stock prices and market data
    - Cryptocurrency prices and trends
    - Sports scores and schedules
    - Market summaries and analysis
    """
    
    def __init__(self):
        self.data_cache = {}
        self.cache_duration = 300  # 5 minutes
        
        # Free financial data APIs
        self.financial_apis = {
            'yahoo_finance': 'https://query1.finance.yahoo.com/v8/finance/chart/',
            'alpha_vantage': 'https://www.alphavantage.co/query',
            'coinbase': 'https://api.coinbase.com/v2/exchange-rates',
            'coinmarketcap': 'https://api.coinmarketcap.com/v1/ticker/',
            'finnhub': 'https://finnhub.io/api/v1/quote'
        }
        
        # Popular stocks and their symbols
        self.popular_stocks = {
            'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOGL', 'amazon': 'AMZN',
            'tesla': 'TSLA', 'meta': 'META', 'netflix': 'NFLX', 'nvidia': 'NVDA',
            'disney': 'DIS', 'uber': 'UBER', 'spotify': 'SPOT', 'twitter': 'TWTR',
            'paypal': 'PYPL', 'zoom': 'ZM', 'shopify': 'SHOP', 'square': 'SQ',
            'amd': 'AMD', 'intel': 'INTC', 'cisco': 'CSCO', 'ibm': 'IBM',
            'oracle': 'ORCL', 'salesforce': 'CRM', 'adobe': 'ADBE', 'mongo': 'MDB'
        }
        
        # Popular cryptocurrencies
        self.popular_crypto = {
            'bitcoin': 'BTC', 'ethereum': 'ETH', 'binance': 'BNB', 'cardano': 'ADA',
            'solana': 'SOL', 'polkadot': 'DOT', 'dogecoin': 'DOGE', 'ripple': 'XRP',
            'litecoin': 'LTC', 'chainlink': 'LINK', 'uniswap': 'UNI', 'avalanche': 'AVAX',
            'polygon': 'MATIC', 'cosmos': 'ATOM', 'algorand': 'ALGO', 'vechain': 'VET'
        }
        
        # Sports leagues and teams
        self.sports_data = {
            'nfl': {
                'name': 'National Football League',
                'teams': ['patriots', 'chiefs', 'packers', 'bills', 'cowboys', 'rams', 'bucs', 'saints']
            },
            'nba': {
                'name': 'National Basketball Association',
                'teams': ['lakers', 'warriors', 'celtics', 'heat', 'nets', 'bucks', 'suns', '76ers']
            },
            'mlb': {
                'name': 'Major League Baseball',
                'teams': ['yankees', 'red sox', 'dodgers', 'giants', 'astros', 'braves', 'mets', 'cubs']
            },
            'nhl': {
                'name': 'National Hockey League',
                'teams': ['lightning', 'avalanche', 'bruins', 'leafs', 'oilers', 'penguins', 'rangers', 'canadiens']
            }
        }
    
    def get_stock_price(self, symbol: str) -> str:
        """
        Get current stock price and information.
        """
        try:
            # Normalize symbol
            symbol = symbol.upper()
            
            # Check cache
            cache_key = f"stock:{symbol}"
            if cache_key in self.data_cache:
                cached_time, data = self.data_cache[cache_key]
                if time.time() - cached_time < self.cache_duration:
                    return self._format_stock_response(data)
            
            # Try multiple sources for stock data
            stock_data = None
            
            # Try Yahoo Finance first (free, no API key)
            stock_data = self._get_yahoo_finance_data(symbol)
            
            if not stock_data:
                # Fallback to basic data
                stock_data = self._get_fallback_stock_data(symbol)
            
            if stock_data:
                # Cache the result
                self.data_cache[cache_key] = (time.time(), stock_data)
                return self._format_stock_response(stock_data)
            else:
                return f"❌ Unable to fetch stock data for {symbol}. Please check the symbol and try again."
                
        except Exception as e:
            return f"❌ Stock data error: {str(e)}"
    
    def _get_yahoo_finance_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get stock data from Yahoo Finance."""
        try:
            url = f"{self.financial_apis['yahoo_finance']}{symbol}"
            params = {
                'range': '1d',
                'interval': '1m',
                'includePrePost': 'true',
                'useYfid': 'true',
                'corsDomain': 'finance.yahoo.com'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'chart' not in data or 'result' not in data['chart']:
                return None
            
            result = data['chart']['result'][0]
            meta = result.get('meta', {})
            
            current_price = meta.get('regularMarketPrice', 0)
            previous_close = meta.get('previousClose', 0)
            change = current_price - previous_close
            change_percent = (change / previous_close * 100) if previous_close else 0
            
            return {
                'symbol': symbol,
                'price': current_price,
                'change': change,
                'change_percent': change_percent,
                'previous_close': previous_close,
                'high': meta.get('regularMarketDayHigh', 0),
                'low': meta.get('regularMarketDayLow', 0),
                'volume': meta.get('regularMarketVolume', 0),
                'market_cap': meta.get('marketCap', 0),
                'source': 'Yahoo Finance'
            }
            
        except Exception as e:
            print(f"⚠️ Yahoo Finance data failed for {symbol}: {e}")
            return None
    
    def _get_fallback_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Fallback stock data when APIs fail."""
        return {
            'symbol': symbol,
            'price': 0,
            'change': 0,
            'change_percent': 0,
            'previous_close': 0,
            'high': 0,
            'low': 0,
            'volume': 0,
            'market_cap': 0,
            'source': 'Fallback Data',
            'note': 'Real-time data unavailable'
        }
    
    def _format_stock_response(self, data: Dict[str, Any]) -> str:
        """Format stock data into a readable response."""
        symbol = data.get('symbol', 'Unknown')
        price = data.get('price', 0)
        change = data.get('change', 0)
        change_percent = data.get('change_percent', 0)
        
        # Determine trend emoji
        if change > 0:
            trend_emoji = '📈'
            trend_text = 'UP'
        elif change < 0:
            trend_emoji = '📉'
            trend_text = 'DOWN'
        else:
            trend_emoji = '➡️'
            trend_text = 'UNCHANGED'
        
        response = f"{trend_emoji} **{symbol} Stock Price**\n\n"
        response += f"💰 **Current Price:** ${price:.2f}\n"
        response += f"📊 **Change:** {change:+.2f} ({change_percent:+.2f}%)\n"
        response += f"📈 **Trend:** {trend_text}\n"
        
        if data.get('previous_close'):
            response += f"🔄 **Previous Close:** ${data['previous_close']:.2f}\n"
        
        if data.get('high') and data.get('low'):
            response += f"📊 **Day Range:** ${data['low']:.2f} - ${data['high']:.2f}\n"
        
        if data.get('volume'):
            volume = data['volume']
            if volume >= 1_000_000:
                volume_str = f"{volume/1_000_000:.1f}M"
            elif volume >= 1_000:
                volume_str = f"{volume/1_000:.1f}K"
            else:
                volume_str = str(volume)
            response += f"📊 **Volume:** {volume_str}\n"
        
        if data.get('market_cap'):
            market_cap = data['market_cap']
            if market_cap >= 1_000_000_000_000:
                cap_str = f"${market_cap/1_000_000_000_000:.2f}T"
            elif market_cap >= 1_000_000_000:
                cap_str = f"${market_cap/1_000_000_000:.2f}B"
            elif market_cap >= 1_000_000:
                cap_str = f"${market_cap/1_000_000:.2f}M"
            else:
                cap_str = f"${market_cap:.2f}"
            response += f"🏢 **Market Cap:** {cap_str}\n"
        
        response += f"\n📡 **Source:** {data.get('source', 'Unknown')}\n"
        response += f"🕒 **Last Updated:** {datetime.now().strftime('%H:%M:%S')}\n"
        
        if data.get('note'):
            response += f"\n⚠️ **Note:** {data['note']}\n"
        
        return response
    
    def get_crypto_price(self, symbol: str) -> str:
        """
        Get current cryptocurrency price and information.
        """
        try:
            # Normalize symbol
            symbol = symbol.upper()
            
            # Check cache
            cache_key = f"crypto:{symbol}"
            if cache_key in self.data_cache:
                cached_time, data = self.data_cache[cache_key]
                if time.time() - cached_time < self.cache_duration:
                    return self._format_crypto_response(data)
            
            # Try multiple sources for crypto data
            crypto_data = None
            
            # Try Coinbase API first (free, no API key)
            crypto_data = self._get_coinbase_data(symbol)
            
            if not crypto_data:
                # Fallback to basic data
                crypto_data = self._get_fallback_crypto_data(symbol)
            
            if crypto_data:
                # Cache the result
                self.data_cache[cache_key] = (time.time(), crypto_data)
                return self._format_crypto_response(crypto_data)
            else:
                return f"❌ Unable to fetch cryptocurrency data for {symbol}. Please check the symbol and try again."
                
        except Exception as e:
            return f"❌ Cryptocurrency data error: {str(e)}"
    
    def _get_coinbase_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get crypto data from Coinbase."""
        try:
            url = f"{self.financial_apis['coinbase']}?currency={symbol}"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' not in data or 'rates' not in data['data']:
                return None
            
            rates = data['data']['rates']
            usd_rate = rates.get('USD', '0')
            
            return {
                'symbol': symbol,
                'price': float(usd_rate),
                'source': 'Coinbase'
            }
            
        except Exception as e:
            print(f"⚠️ Coinbase data failed for {symbol}: {e}")
            return None
    
    def _get_fallback_crypto_data(self, symbol: str) -> Dict[str, Any]:
        """Fallback crypto data when APIs fail."""
        return {
            'symbol': symbol,
            'price': 0,
            'source': 'Fallback Data',
            'note': 'Real-time data unavailable'
        }
    
    def _format_crypto_response(self, data: Dict[str, Any]) -> str:
        """Format crypto data into a readable response."""
        symbol = data.get('symbol', 'Unknown')
        price = data.get('price', 0)
        
        response = f"₿ **{symbol} Cryptocurrency Price**\n\n"
        response += f"💰 **Current Price:** ${price:.2f}\n"
        
        response += f"\n📡 **Source:** {data.get('source', 'Unknown')}\n"
        response += f"🕒 **Last Updated:** {datetime.now().strftime('%H:%M:%S')}\n"
        
        if data.get('note'):
            response += f"\n⚠️ **Note:** {data['note']}\n"
        
        return response
    
    def get_market_summary(self) -> str:
        """
        Get a summary of major market indices.
        """
        try:
            major_indices = ['^GSPC', '^DJI', '^IXIC', '^RUT']  # S&P 500, Dow Jones, NASDAQ, Russell 2000
            index_names = {
                '^GSPC': 'S&P 500',
                '^DJI': 'Dow Jones Industrial Average',
                '^IXIC': 'NASDAQ Composite',
                '^RUT': 'Russell 2000'
            }
            
            summary_data = []
            
            for index in major_indices:
                try:
                    data = self._get_yahoo_finance_data(index)
                    if data:
                        summary_data.append({
                            'name': index_names.get(index, index),
                            'price': data.get('price', 0),
                            'change': data.get('change', 0),
                            'change_percent': data.get('change_percent', 0)
                        })
                except:
                    continue
            
            if summary_data:
                response = "📊 **Market Summary**\n\n"
                
                for index in summary_data:
                    trend_emoji = '📈' if index['change'] > 0 else '📉' if index['change'] < 0 else '➡️'
                    response += f"{trend_emoji} **{index['name']}:** {index['price']:.2f} ({index['change']:+.2f}, {index['change_percent']:+.2f}%)\n"
                
                response += f"\n🕒 **Last Updated:** {datetime.now().strftime('%H:%M:%S')}\n"
                response += "📡 **Source:** Yahoo Finance\n"
                
                return response
            else:
                return "❌ Unable to fetch market summary at this time."
                
        except Exception as e:
            return f"❌ Market summary error: {str(e)}"
    
    def get_sports_scores(self, league: str = None, team: str = None) -> str:
        """
        Get sports scores and schedules.
        """
        try:
            if not league:
                return self._get_sports_overview()
            
            league = league.lower()
            if league not in self.sports_data:
                available_leagues = ", ".join(self.sports_data.keys())
                return f"❌ Unknown league '{league}'. Available leagues: {available_leagues}"
            
            if team:
                return self._get_team_scores(league, team)
            else:
                return self._get_league_scores(league)
                
        except Exception as e:
            return f"❌ Sports scores error: {str(e)}"
    
    def _get_sports_overview(self) -> str:
        """Get overview of available sports leagues."""
        response = "⚽ **Sports Scores & Schedules**\n\n"
        
        for league_id, league_info in self.sports_data.items():
            response += f"🏈 **{league_info['name']} ({league_id.upper()})**\n"
            response += f"   Teams: {', '.join(league_info['teams'][:4])}...\n\n"
        
        response += "💡 **Usage:**\n"
        response += "   • 'sports scores nfl' - Get NFL scores\n"
        response += "   • 'sports scores nba' - Get NBA scores\n"
        response += "   • 'sports scores mlb' - Get MLB scores\n"
        response += "   • 'sports scores nhl' - Get NHL scores\n"
        response += "   • 'sports scores [league] [team]' - Get specific team scores\n"
        
        return response
    
    def _get_league_scores(self, league: str) -> str:
        """Get scores for a specific league."""
        league_info = self.sports_data[league]
        
        response = f"🏈 **{league_info['name']} Scores**\n\n"
        response += "📊 **Recent Games:**\n"
        response += "   • Game 1: Team A vs Team B - Final Score\n"
        response += "   • Game 2: Team C vs Team D - Final Score\n"
        response += "   • Game 3: Team E vs Team F - Final Score\n\n"
        
        response += "📅 **Upcoming Games:**\n"
        response += "   • Tomorrow: Team G vs Team H\n"
        response += "   • Weekend: Team I vs Team J\n\n"
        
        response += "ℹ️ **Note:** Real-time sports data requires specialized APIs.\n"
        response += "For live scores, visit ESPN, NFL.com, NBA.com, or MLB.com\n"
        
        return response
    
    def _get_team_scores(self, league: str, team: str) -> str:
        """Get scores for a specific team."""
        league_info = self.sports_data[league]
        
        if team.lower() not in league_info['teams']:
            available_teams = ", ".join(league_info['teams'])
            return f"❌ Unknown team '{team}' in {league_info['name']}. Available teams: {available_teams}"
        
        response = f"🏈 **{team.title()} - {league_info['name']}**\n\n"
        response += "📊 **Recent Games:**\n"
        response += f"   • {team.title()} vs Team A - Final Score\n"
        response += f"   • {team.title()} vs Team B - Final Score\n"
        response += f"   • {team.title()} vs Team C - Final Score\n\n"
        
        response += "📅 **Upcoming Games:**\n"
        response += f"   • Tomorrow: {team.title()} vs Team D\n"
        response += f"   • Weekend: {team.title()} vs Team E\n\n"
        
        response += "ℹ️ **Note:** Real-time sports data requires specialized APIs.\n"
        response += "For live scores, visit ESPN, NFL.com, NBA.com, or MLB.com\n"
        
        return response
    
    def get_financial_tips(self) -> str:
        """Get financial tips and information."""
        return """💡 **Financial Tips & Information**

📈 **Investment Tips:**
   • Diversify your portfolio across different asset classes
   • Invest for the long term, not short-term gains
   • Research companies before investing
   • Consider dollar-cost averaging
   • Don't invest more than you can afford to lose

💰 **Budgeting Tips:**
   • Track your expenses monthly
   • Create a 50/30/20 budget (needs/wants/savings)
   • Build an emergency fund (3-6 months expenses)
   • Pay off high-interest debt first
   • Automate your savings

📊 **Market Information:**
   • Markets are volatile - don't panic sell
   • Past performance doesn't guarantee future results
   • Consider your risk tolerance
   • Stay informed but avoid over-trading
   • Consider professional financial advice

⚠️ **Important Disclaimers:**
   • This is not financial advice
   • Always do your own research
   • Consult with financial professionals
   • Markets can go up or down
   • Cryptocurrency is highly volatile

🔗 **Useful Resources:**
   • SEC.gov - Securities and Exchange Commission
   • FINRA.org - Financial Industry Regulatory Authority
   • Investopedia.com - Financial education
   • Yahoo Finance - Market data
   • Bloomberg.com - Financial news
"""
    
    def get_popular_stocks(self) -> str:
        """Get list of popular stocks."""
        response = "📈 **Popular Stocks**\n\n"
        
        for name, symbol in list(self.popular_stocks.items())[:20]:  # Show first 20
            response += f"   • **{name.title()}** ({symbol})\n"
        
        response += "\n💡 **Usage:** 'stock price AAPL' or 'stock price apple'\n"
        
        return response
    
    def get_popular_crypto(self) -> str:
        """Get list of popular cryptocurrencies."""
        response = "₿ **Popular Cryptocurrencies**\n\n"
        
        for name, symbol in list(self.popular_crypto.items())[:15]:  # Show first 15
            response += f"   • **{name.title()}** ({symbol})\n"
        
        response += "\n💡 **Usage:** 'crypto price BTC' or 'crypto price bitcoin'\n"
        
        return response
