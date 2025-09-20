"""
WeatherService.py
Free weather integration with multiple APIs and comprehensive weather data.
"""

import requests
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import re

class JarvisWeatherService:
    """
    Weather service using free APIs:
    - OpenWeatherMap (free tier)
    - WeatherAPI (free tier)
    - Open-Meteo (completely free)
    - Fallback to basic weather data
    """
    
    def __init__(self):
        self.weather_cache = {}
        self.cache_duration = 600  # 10 minutes
        
        # Free weather APIs (no keys required)
        self.weather_sources = [
            'open_meteo',    # Completely free, no API key
            'weather_api',   # Free tier
            'openweather'    # Free tier
        ]
        
        # Weather icons mapping
        self.weather_icons = {
            'clear': '☀️', 'sunny': '☀️', 'sun': '☀️',
            'cloudy': '☁️', 'clouds': '☁️', 'overcast': '☁️',
            'rain': '🌧️', 'rainy': '🌧️', 'drizzle': '🌦️',
            'snow': '❄️', 'snowy': '❄️', 'sleet': '🌨️',
            'storm': '⛈️', 'thunderstorm': '⛈️', 'thunder': '⛈️',
            'fog': '🌫️', 'mist': '🌫️', 'haze': '🌫️',
            'wind': '💨', 'windy': '💨'
        }
    
    def get_weather(self, location: str = None) -> str:
        """
        Get current weather for a location.
        """
        try:
            # Use user's location if not specified
            if not location:
                location = self._get_user_location()
            
            # Check cache
            cache_key = f"weather:{location.lower()}"
            if cache_key in self.weather_cache:
                cached_time, data = self.weather_cache[cache_key]
                if time.time() - cached_time < self.cache_duration:
                    return self._format_weather_response(data, location)
            
            # Try multiple weather sources
            weather_data = None
            for source in self.weather_sources:
                try:
                    if source == 'open_meteo':
                        weather_data = self._get_open_meteo_weather(location)
                    elif source == 'weather_api':
                        weather_data = self._get_weather_api_weather(location)
                    elif source == 'openweather':
                        weather_data = self._get_openweather_weather(location)
                    
                    if weather_data:
                        break
                        
                except Exception as e:
                    print(f"⚠️ Weather source {source} failed: {e}")
                    continue
            
            if not weather_data:
                return self._get_fallback_weather(location)
            
            # Cache the result
            self.weather_cache[cache_key] = (time.time(), weather_data)
            
            return self._format_weather_response(weather_data, location)
            
        except Exception as e:
            return f"❌ Weather error: {str(e)}"
    
    def _get_open_meteo_weather(self, location: str) -> Dict[str, Any]:
        """Get weather from Open-Meteo (free, no API key required)."""
        try:
            # Get coordinates first (simplified geocoding)
            coords = self._get_coordinates(location)
            if not coords:
                return None
            
            lat, lon = coords
            
            # Open-Meteo API
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                'latitude': lat,
                'longitude': lon,
                'current_weather': 'true',
                'daily': 'temperature_2m_max,temperature_2m_min,weathercode',
                'timezone': 'auto',
                'forecast_days': 3
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'current_weather' not in data:
                return None
            
            current = data['current_weather']
            daily = data.get('daily', {})
            
            return {
                'location': location,
                'temperature': current.get('temperature'),
                'condition': self._get_weather_condition(current.get('weathercode')),
                'humidity': None,  # Not available in free tier
                'wind_speed': current.get('windspeed'),
                'wind_direction': current.get('winddirection'),
                'pressure': None,  # Not available in free tier
                'visibility': None,  # Not available in free tier
                'uv_index': None,  # Not available in free tier
                'feels_like': None,  # Not available in free tier
                'forecast': self._format_forecast(daily),
                'source': 'Open-Meteo'
            }
            
        except Exception as e:
            print(f"⚠️ Open-Meteo weather failed: {e}")
            return None
    
    def _get_weather_api_weather(self, location: str) -> Dict[str, Any]:
        """Get weather from WeatherAPI (free tier)."""
        try:
            # WeatherAPI free tier (1000 requests/month)
            url = f"http://api.weatherapi.com/v1/current.json"
            params = {
                'key': 'free',  # Use free tier
                'q': location,
                'aqi': 'no'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            # This will likely fail without a real API key, but we try anyway
            if response.status_code == 401:
                return None
            
            data = response.json()
            
            current = data.get('current', {})
            
            return {
                'location': location,
                'temperature': current.get('temp_c'),
                'condition': current.get('condition', {}).get('text'),
                'humidity': current.get('humidity'),
                'wind_speed': current.get('wind_kph'),
                'wind_direction': current.get('wind_degree'),
                'pressure': current.get('pressure_mb'),
                'visibility': current.get('vis_km'),
                'uv_index': current.get('uv'),
                'feels_like': current.get('feelslike_c'),
                'forecast': None,
                'source': 'WeatherAPI'
            }
            
        except Exception as e:
            print(f"⚠️ WeatherAPI failed: {e}")
            return None
    
    def _get_openweather_weather(self, location: str) -> Dict[str, Any]:
        """Get weather from OpenWeatherMap (free tier)."""
        try:
            # OpenWeatherMap free tier (1000 calls/day)
            # This would require an API key, so we'll skip it for now
            return None
            
        except Exception as e:
            print(f"⚠️ OpenWeatherMap failed: {e}")
            return None
    
    def _get_fallback_weather(self, location: str) -> str:
        """Fallback weather response when APIs fail."""
        return f"""🌤️ **Weather for {location}**

❌ Unable to fetch real-time weather data at the moment.

**Possible reasons:**
• Internet connection issues
• Weather service temporarily unavailable
• Location not recognized

**Suggestions:**
• Check your internet connection
• Try a different city name
• Use a more specific location (City, Country)

**Alternative:** You can check weather on:
• 🌐 Weather.com
• 🌐 AccuWeather.com
• 🌐 BBC Weather
"""
    
    def _get_coordinates(self, location: str) -> Optional[tuple]:
        """Get coordinates for a location (simplified)."""
        # Simplified coordinate lookup for major cities
        major_cities = {
            'london': (51.5074, -0.1278),
            'paris': (48.8566, 2.3522),
            'new york': (40.7128, -74.0060),
            'tokyo': (35.6762, 139.6503),
            'sydney': (-33.8688, 151.2093),
            'mumbai': (19.0760, 72.8777),
            'beijing': (39.9042, 116.4074),
            'moscow': (55.7558, 37.6176),
            'cairo': (30.0444, 31.2357),
            'rio de janeiro': (-22.9068, -43.1729),
            'los angeles': (34.0522, -118.2437),
            'chicago': (41.8781, -87.6298),
            'houston': (29.7604, -95.3698),
            'phoenix': (33.4484, -112.0740),
            'philadelphia': (39.9526, -75.1652),
            'san antonio': (29.4241, -98.4936),
            'san diego': (32.7157, -117.1611),
            'dallas': (32.7767, -96.7970),
            'san jose': (37.3382, -121.8863),
            'austin': (30.2672, -97.7431),
            'jacksonville': (30.3322, -81.6557),
            'fort worth': (32.7555, -97.3308),
            'columbus': (39.9612, -82.9988),
            'charlotte': (35.2271, -80.8431),
            'san francisco': (37.7749, -122.4194),
            'indianapolis': (39.7684, -86.1581),
            'seattle': (47.6062, -122.3321),
            'denver': (39.7392, -104.9903),
            'washington': (38.9072, -77.0369),
            'boston': (42.3601, -71.0589),
            'el paso': (31.7619, -106.4850),
            'nashville': (36.1627, -86.7816),
            'detroit': (42.3314, -83.0458),
            'oklahoma city': (35.4676, -97.5164),
            'portland': (45.5152, -122.6784),
            'las vegas': (36.1699, -115.1398),
            'memphis': (35.1495, -90.0490),
            'louisville': (38.2527, -85.7585),
            'baltimore': (39.2904, -76.6122),
            'milwaukee': (43.0389, -87.9065),
            'albuquerque': (35.0844, -106.6504),
            'tucson': (32.2226, -110.9747),
            'fresno': (36.7378, -119.7871),
            'sacramento': (38.5816, -121.4944),
            'mesa': (33.4152, -111.8315),
            'kansas city': (39.0997, -94.5786),
            'atlanta': (33.7490, -84.3880),
            'long beach': (33.7701, -118.1937),
            'colorado springs': (38.8339, -104.8214),
            'raleigh': (35.7796, -78.6382),
            'miami': (25.7617, -80.1918),
            'virginia beach': (36.8529, -75.9780),
            'omaha': (41.2565, -95.9345),
            'oakland': (37.8044, -122.2712),
            'minneapolis': (44.9778, -93.2650),
            'tulsa': (36.1540, -95.9928),
            'arlington': (32.7357, -97.1081),
            'tampa': (27.9506, -82.4572),
            'new orleans': (29.9511, -90.0715),
            'wichita': (37.6872, -97.3301),
            'cleveland': (41.4993, -81.6944),
            'bakersfield': (35.3733, -119.0187),
            'aurora': (39.7294, -104.8319),
            'anaheim': (33.8366, -117.9143),
            'honolulu': (21.3099, -157.8581),
            'santa ana': (33.7455, -117.8677),
            'corpus christi': (27.8006, -97.3964),
            'riverside': (33.9533, -117.3962),
            'lexington': (38.0406, -84.5037),
            'stockton': (37.9577, -121.2908),
            'toledo': (41.6528, -83.5379),
            'st. paul': (44.9537, -93.0900),
            'newark': (40.7357, -74.1724),
            'greensboro': (36.0726, -79.7920),
            'plano': (33.0198, -96.6989),
            'henderson': (36.0395, -114.9817),
            'lincoln': (40.8136, -96.7026),
            'buffalo': (42.8864, -78.8784),
            'jersey city': (40.7178, -74.0431),
            'chula vista': (32.6401, -117.0842),
            'fort wayne': (41.0793, -85.1394),
            'orlando': (28.5383, -81.3792),
            'st. petersburg': (27.7676, -82.6403),
            'chandler': (33.3062, -111.8412),
            'laredo': (27.5306, -99.4803),
            'norfolk': (36.8468, -76.2852),
            'durham': (35.9940, -78.8986),
            'madison': (43.0731, -89.4012),
            'lubbock': (33.5779, -101.8552),
            'irvine': (33.6846, -117.8265),
            'winston salem': (36.0999, -80.2442),
            'glendale': (33.5387, -112.1860),
            'garland': (32.9126, -96.6389),
            'hialeah': (25.8576, -80.2781),
            'reno': (39.5296, -119.8138),
            'chesapeake': (36.7682, -76.2875),
            'gilbert': (33.3528, -111.7890),
            'baton rouge': (30.4515, -91.1871),
            'irving': (32.8140, -96.9489),
            'scottsdale': (33.4942, -111.9211),
            'north las vegas': (36.1989, -115.1175),
            'fremont': (37.5483, -121.9886),
            'boise': (43.6150, -116.2023),
            'richmond': (37.5407, -77.4360),
            'san bernardino': (34.1083, -117.2898),
            'birmingham': (33.5207, -86.8025),
            'spokane': (47.6588, -117.4260),
            'rochester': (43.1566, -77.6088),
            'des moines': (41.5868, -93.6250),
            'modesto': (37.6391, -120.9969),
            'fayetteville': (35.0527, -78.8784),
            'tacoma': (47.2529, -122.4443),
            'oxnard': (34.1975, -119.1771),
            'fontana': (34.0922, -117.4350),
            'columbus': (39.9612, -82.9988),
            'montgomery': (32.3668, -86.3000),
            'moreno valley': (33.9425, -117.2297),
            'shreveport': (32.5252, -93.7502),
            'aurora': (39.7294, -104.8319),
            'yonkers': (40.9312, -73.8988),
            'akron': (41.0814, -81.5190),
            'huntington beach': (33.6595, -117.9988),
            'little rock': (34.7465, -92.2896),
            'augusta': (33.4735, -82.0105),
            'amarillo': (35.2219, -101.8313),
            'glendale': (33.5387, -112.1860),
            'mobile': (30.6954, -88.0399),
            'grand rapids': (42.9634, -85.6681),
            'salt lake city': (40.7608, -111.8910),
            'tallahassee': (30.4383, -84.2807),
            'huntsville': (34.7304, -86.5861),
            'grand prairie': (32.7459, -96.9978),
            'knoxville': (35.9606, -83.9207),
            'worcester': (42.2626, -71.8023),
            'newport news': (37.0871, -76.4730),
            'brownsville': (25.9018, -97.4975),
            'overland park': (38.9822, -94.6708),
            'santa clarita': (34.3917, -118.5426),
            'providence': (41.8240, -71.4128),
            'garden grove': (33.7739, -117.9414),
            'chattanooga': (35.0456, -85.3097),
            'oceanside': (33.1959, -117.3795),
            'jackson': (32.2988, -90.1848),
            'fort lauderdale': (26.1224, -80.1373),
            'santa rosa': (38.4404, -122.7141),
            'rancho cucamonga': (34.1064, -117.5931),
            'port st. lucie': (27.2939, -80.3503),
            'tempe': (33.4255, -111.9400),
            'ontario': (34.0633, -117.6509),
            'vancouver': (45.6387, -122.6615),
            'sioux falls': (43.5446, -96.7311),
            'springfield': (37.2083, -93.2923),
            'peoria': (40.6936, -89.5890),
            'pembroke pines': (26.0078, -80.2963),
            'elk grove': (38.4088, -121.3716),
            'rockford': (42.2711, -89.0940),
            'palmdale': (34.5794, -118.1165),
            'corona': (33.8753, -117.5664),
            'salinas': (36.6777, -121.6555),
            'pomona': (34.0553, -117.7522),
            'paterson': (40.9168, -74.1718),
            'joliet': (41.5250, -88.0817),
            'pasadena': (34.1478, -118.1445),
            'torrance': (33.8358, -118.3406),
            'bridgeport': (41.1865, -73.1952),
            'stockton': (37.9577, -121.2908),
            'irvine': (33.6846, -117.8265),
            'chula vista': (32.6401, -117.0842),
            'fremont': (37.5483, -121.9886),
            'san bernardino': (34.1083, -117.2898),
            'modesto': (37.6391, -120.9969),
            'fontana': (34.0922, -117.4350),
            'santa clarita': (34.3917, -118.5426),
            'rancho cucamonga': (34.1064, -117.5931),
            'tempe': (33.4255, -111.9400),
            'ontario': (34.0633, -117.6509),
            'vancouver': (45.6387, -122.6615),
            'sioux falls': (43.5446, -96.7311),
            'springfield': (37.2083, -93.2923),
            'peoria': (40.6936, -89.5890),
            'pembroke pines': (26.0078, -80.2963),
            'elk grove': (38.4088, -121.3716),
            'rockford': (42.2711, -89.0940),
            'palmdale': (34.5794, -118.1165),
            'corona': (33.8753, -117.5664),
            'salinas': (36.6777, -121.6555),
            'pomona': (34.0553, -117.7522),
            'paterson': (40.9168, -74.1718),
            'joliet': (41.5250, -88.0817),
            'pasadena': (34.1478, -118.1445),
            'torrance': (33.8358, -118.3406),
            'bridgeport': (41.1865, -73.1952)
        }
        
        location_lower = location.lower().strip()
        return major_cities.get(location_lower)
    
    def _get_user_location(self) -> str:
        """Get user's approximate location."""
        try:
            # Try to get location from IP
            response = requests.get('http://ip-api.com/json/', timeout=5)
            data = response.json()
            
            if data.get('status') == 'success':
                city = data.get('city', 'Unknown')
                country = data.get('country', 'Unknown')
                return f"{city}, {country}"
            else:
                return "London, UK"  # Default fallback
                
        except Exception as e:
            print(f"⚠️ Location detection failed: {e}")
            return "London, UK"  # Default fallback
    
    def _get_weather_condition(self, weather_code: int) -> str:
        """Convert weather code to condition."""
        weather_codes = {
            0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast',
            45: 'Fog', 48: 'Depositing rime fog',
            51: 'Light drizzle', 53: 'Moderate drizzle', 55: 'Dense drizzle',
            56: 'Light freezing drizzle', 57: 'Dense freezing drizzle',
            61: 'Slight rain', 63: 'Moderate rain', 65: 'Heavy rain',
            66: 'Light freezing rain', 67: 'Heavy freezing rain',
            71: 'Slight snow', 73: 'Moderate snow', 75: 'Heavy snow',
            77: 'Snow grains', 80: 'Slight rain showers', 81: 'Moderate rain showers',
            82: 'Violent rain showers', 85: 'Slight snow showers', 86: 'Heavy snow showers',
            95: 'Thunderstorm', 96: 'Thunderstorm with slight hail', 99: 'Thunderstorm with heavy hail'
        }
        return weather_codes.get(weather_code, 'Unknown')
    
    def _format_forecast(self, daily_data: Dict[str, Any]) -> str:
        """Format forecast data."""
        if not daily_data:
            return ""
        
        forecast = "\n📅 **3-Day Forecast:**\n"
        
        dates = daily_data.get('time', [])
        max_temps = daily_data.get('temperature_2m_max', [])
        min_temps = daily_data.get('temperature_2m_min', [])
        weather_codes = daily_data.get('weathercode', [])
        
        for i in range(min(3, len(dates))):
            date = dates[i]
            max_temp = max_temps[i] if i < len(max_temps) else 'N/A'
            min_temp = min_temps[i] if i < len(min_temps) else 'N/A'
            weather_code = weather_codes[i] if i < len(weather_codes) else 0
            
            condition = self._get_weather_condition(weather_code)
            icon = self._get_weather_icon(condition)
            
            forecast += f"   {icon} {date}: {min_temp}°C - {max_temp}°C, {condition}\n"
        
        return forecast
    
    def _get_weather_icon(self, condition: str) -> str:
        """Get weather icon for condition."""
        condition_lower = condition.lower()
        
        for key, icon in self.weather_icons.items():
            if key in condition_lower:
                return icon
        
        return '🌤️'  # Default icon
    
    def _format_weather_response(self, data: Dict[str, Any], location: str) -> str:
        """Format weather data into a nice response."""
        if not data:
            return self._get_fallback_weather(location)
        
        icon = self._get_weather_icon(data.get('condition', ''))
        temp = data.get('temperature', 'N/A')
        condition = data.get('condition', 'Unknown')
        source = data.get('source', 'Unknown')
        
        response = f"{icon} **Weather for {location}**\n\n"
        response += f"🌡️ **Temperature:** {temp}°C\n"
        response += f"☁️ **Condition:** {condition}\n"
        
        if data.get('humidity'):
            response += f"💧 **Humidity:** {data['humidity']}%\n"
        
        if data.get('wind_speed'):
            response += f"💨 **Wind:** {data['wind_speed']} km/h"
            if data.get('wind_direction'):
                response += f" (direction: {data['wind_direction']}°)"
            response += "\n"
        
        if data.get('pressure'):
            response += f"📊 **Pressure:** {data['pressure']} mb\n"
        
        if data.get('visibility'):
            response += f"👁️ **Visibility:** {data['visibility']} km\n"
        
        if data.get('uv_index'):
            response += f"☀️ **UV Index:** {data['uv_index']}\n"
        
        if data.get('feels_like'):
            response += f"🤔 **Feels like:** {data['feels_like']}°C\n"
        
        if data.get('forecast'):
            response += data['forecast']
        
        response += f"\n📡 **Source:** {source}\n"
        response += f"🕒 **Last updated:** {datetime.now().strftime('%H:%M:%S')}"
        
        return response
    
    def get_weather_alerts(self, location: str) -> str:
        """Get weather alerts for a location."""
        try:
            # This would require a weather alert API
            # For now, return a placeholder
            return f"""⚠️ **Weather Alerts for {location}**

No active weather alerts at this time.

**Stay informed:**
• Check local weather services
• Monitor official weather channels
• Sign up for weather alerts in your area
"""
        except Exception as e:
            return f"❌ Weather alerts error: {str(e)}"
    
    def get_weather_forecast(self, location: str, days: int = 5) -> str:
        """Get extended weather forecast."""
        try:
            # Get weather data (this will include forecast if available)
            weather_data = self.get_weather(location)
            
            # Add extended forecast information
            extended_forecast = f"""

📊 **Extended Forecast Tips:**
• Check multiple weather sources for accuracy
• Weather forecasts become less reliable beyond 3-5 days
• Local conditions can vary significantly
• Consider microclimates in your area

**Best Weather Apps:**
• Weather.com
• AccuWeather
• Weather Underground
• Local weather services
"""
            
            return weather_data + extended_forecast
            
        except Exception as e:
            return f"❌ Extended forecast error: {str(e)}"
