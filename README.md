# 🤖 JARVIS AI Assistant

**Just A Rather Very Intelligent System** - A comprehensive AI assistant inspired by Tony Stark's JARVIS, featuring voice interaction, web search, system automation, image generation, and much more.

## ✨ Features

### 🗣️ Voice Interaction
- **Wake Word Detection**: Activate with "JARVIS"
- **Natural Speech Recognition**: Powered by Groq Whisper API
- **High-Quality Text-to-Speech**: Multiple voice options with edge-tts
- **Continuous Listening**: Always ready to assist

### 🧠 AI Capabilities
- **Advanced Conversation**: Powered by Groq LLaMA or Cohere models
- **Context Memory**: Remembers conversation history
- **Intelligent Responses**: JARVIS personality with wit and sophistication
- **Command Recognition**: Natural language command processing

### 🔍 Information & Search
- **Real-time Web Search**: Google search integration
- **News Updates**: Latest news on any topic
- **Weather Information**: Current weather for any location
- **Definition Lookup**: Word definitions and explanations

### 🖥️ System Automation
- **Application Control**: Open/close applications by voice or text
- **System Information**: CPU, memory, disk usage monitoring
- **Task Scheduling**: Set timers and schedule tasks
- **Mathematical Calculations**: Complex math operations
- **File Management**: System operations and control

### 🎨 Image Generation
- **AI Image Creation**: Stable Diffusion and DALL-E integration
- **Multiple Styles**: Photographic, digital art, cinematic, and more
- **Image Collages**: Combine multiple images automatically
- **Placeholder Generation**: Works without API keys

### 🖼️ User Interfaces
- **Modern GUI**: Beautiful PyQt5 interface with dark theme
- **Console Mode**: Terminal-based interaction
- **Voice-Only Mode**: Hands-free operation
- **System Tray**: Background operation support

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/your-username/jarvis_project.git
cd jarvis_project

# Install dependencies
pip install -r Requirements.txt
```

### 2. Configuration (Optional but Recommended)

Copy the environment template and configure your API keys:

```bash
# Copy the template
cp env_template.txt .env

# Edit .env with your API keys
# See API Keys section below for details
```

### 3. Run JARVIS

```bash
# Console Mode (Default)
python Main.py

# GUI Mode
python Main.py gui

# Voice-Only Mode
python Main.py voice

# System Test
python Main.py test

# Help
python Main.py help
```

## 🔧 API Keys Configuration

JARVIS works with fallback methods even without API keys, but for full functionality, configure these optional APIs:

### Required for Advanced Features:
- **GROQ_API_KEY**: For advanced AI chat and speech recognition
  - Get from: [Groq Console](https://console.groq.com/)
  - Used for: AI responses, speech-to-text

### Optional Enhancements:
- **OPENAI_API_KEY**: For DALL-E image generation
  - Get from: [OpenAI Platform](https://platform.openai.com/)
- **STABILITY_API_KEY**: For Stable Diffusion images
  - Get from: [Stability AI](https://platform.stability.ai/)
- **NEWS_API_KEY**: For news retrieval
  - Get from: [NewsAPI](https://newsapi.org/)
- **WEATHER_API_KEY**: For weather information
  - Get from: [OpenWeatherMap](https://openweathermap.org/api)

## 💬 Usage Examples

### Console Mode
```
👤 You: Hello JARVIS
🤖 JARVIS: Good day! JARVIS at your service. How may I assist you today?

👤 You: search artificial intelligence news
🤖 JARVIS: 🔍 Web search results for 'artificial intelligence news'...

👤 You: open calculator
🤖 JARVIS: ✅ Successfully opened calculator

👤 You: generate image of a futuristic robot
🤖 JARVIS: 🎨 Generating image: a futuristic robot...

👤 You: what's the weather in New York?
🤖 JARVIS: 🌤️ Weather information for New York...
```

### Voice Commands
- "JARVIS, what time is it?"
- "JARVIS, search for Python tutorials"
- "JARVIS, open Chrome browser"
- "JARVIS, generate an image of a sunset"
- "JARVIS, what's the latest tech news?"
- "JARVIS, calculate 25 times 47"

## 📁 Project Structure

```
jarvis_project/
├── Backend/
│   ├── Model.py              # AI model integration
│   ├── Chatbot.py            # Main JARVIS chatbot
│   ├── SpeechToText.py       # Voice recognition
│   ├── TextToSpeech.py       # Voice synthesis
│   ├── Automation.py         # System automation
│   ├── ImageGeneration.py    # AI image generation
│   └── RealtimeSearchEngine.py # Web search & info
├── Frontend/
│   └── Files/                # Generated files storage
├── Data/                     # Data storage
├── Graphics/                 # Graphics and assets
├── Main.py                   # Main entry point
├── GUI.py                    # PyQt5 GUI interface
├── Requirements.txt          # Python dependencies
├── env_template.txt          # Environment template
└── README.md                 # This file
```

## 🎯 Available Commands

### General Conversation
- Natural conversation with memory
- "Hello", "How are you?", "What can you do?"

### Search & Information
- `search [query]` - Web search
- `news [topic]` - Latest news
- `weather [location]` - Weather information
- `define [word]` - Word definitions

### System Control
- `open [application]` - Launch applications
- `time` - Current time
- `date` - Current date
- `calculate [expression]` - Math calculations
- `system info` - System status

### Image Generation
- `generate image of [description]` - Create AI images
- `create image [description]` - Alternative syntax

### Memory & Utilities
- `remember [information]` - Store information
- `recall` - Retrieve stored information
- `joke` - Tell a joke
- `help` - Show capabilities

## 🛠️ Development

### Running Tests
```bash
python Main.py test
```

### Adding New Features
1. Create new modules in `Backend/`
2. Import in `Backend/Chatbot.py`
3. Add command patterns and handlers
4. Update GUI if needed

### Customization
- Modify voice in `Backend/TextToSpeech.py`
- Add new commands in `Backend/Chatbot.py`
- Customize GUI theme in `GUI.py`
- Add new AI models in `Backend/Model.py`

## 🔧 Troubleshooting

### Common Issues

**Import Errors:**
```bash
pip install -r Requirements.txt
```

**Voice Recognition Not Working:**
- Install PyAudio: `pip install pyaudio`
- On Windows: May need Visual C++ Build Tools
- On Linux: `sudo apt-get install portaudio19-dev python3-pyaudio`

**GUI Not Starting:**
```bash
pip install PyQt5
```

**No Voice Output:**
- Check audio drivers
- Try different TTS voice: Modify `JARVIS_VOICE` in `.env`

### Performance Tips
- Use SSD for faster image generation
- Configure API keys for better responses
- Close unnecessary applications for voice recognition
- Use GUI mode for better resource management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by Tony Stark's JARVIS from Marvel
- Built with modern AI and speech technologies
- Thanks to the open-source community for amazing libraries

## 📞 Support

For support, feature requests, or bug reports:
- Open an issue on GitHub
- Check the troubleshooting section
- Run `python Main.py test` for diagnostics

---

**"Sometimes you gotta run before you can walk."** - Tony Stark

Enjoy your personal AI assistant! 🚀
