# JARVIS AI Assistant - Setup Guide

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r Requirements.txt
```

### 2. Environment Setup
Create a `.env` file in the project root with your API keys:

```env
# Required: Groq API Key for AI Model
GROQ_API_KEY=your_groq_api_key_here

# Optional: Additional API Keys
COHERE_API_KEY=your_cohere_api_key_here
NEWS_API_KEY=your_news_api_key_here
WEATHER_API_KEY=your_weather_api_key_here

# Optional: User Configuration
USERNAME=User
ASSISTANT_NAME=JARVIS
```

### 3. Get Your Groq API Key
1. Visit [https://console.groq.com/](https://console.groq.com/)
2. Sign up for a free account
3. Generate an API key
4. Copy it to your `.env` file

### 4. Run JARVIS

**Modern GUI (Recommended):**
```bash
python Main.py modern
```

**Console Mode:**
```bash
python Main.py console
```

**Original GUI:**
```bash
python Main.py gui
```

**Voice Mode:**
```bash
python Main.py voice
```

## 🎯 Features

✅ **Modern GUI Interface** - Sleek PyQt5 interface with chat bubbles and voice controls  
✅ **Voice Recognition** - Groq Whisper API integration with wake word detection  
✅ **Text-to-Speech** - High-quality edge-tts voice synthesis  
✅ **Real-time Weather** - Weather data for cities worldwide (Pune, Mumbai, Delhi, etc.)  
✅ **Web Search** - Intelligent search with fallback responses  
✅ **Music Control** - Play music via Spotify, YouTube Music  
✅ **App Control** - Open installed applications, files, and folders  
✅ **Memory System** - Remembers your name and conversation history  
✅ **AI Personality** - Context-aware responses and emotional intelligence  

## 🔧 Troubleshooting

**Voice not working?** - Make sure your microphone is connected and permissions are granted.

**Weather not showing?** - The weather service works without API keys for major cities.

**App opening issues?** - Try using specific app names like "calculator", "notepad", "chrome".

## 📝 Commands to Try

- "weather in Pune"
- "who is elon musk"
- "play some music" 
- "open calculator"
- "my name is [Your Name]"
- "what's the latest news"

Enjoy your JARVIS AI Assistant! 🤖✨
