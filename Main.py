"""
Main.py
JARVIS AI Assistant - Main entry point that orchestrates all functionalities.
"""

import sys
import os
import argparse
import time
from typing import Optional

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import performance optimizations
try:
    from Backend.StartupOptimizer import optimize_jarvis_startup
    from Backend.PerformanceMonitor import show_performance_monitor
    OPTIMIZATIONS_AVAILABLE = True
except ImportError:
    OPTIMIZATIONS_AVAILABLE = False
    print("⚠️ Performance optimizations not available")

def run_console_mode():
    """Run JARVIS in console mode."""
    try:
        from Backend.Chatbot import JarvisChatbot
        from Backend.TextToSpeech import jarvis_greeting
        
        print("=" * 60)
        print("🤖 JARVIS AI Assistant - Console Mode")
        print("=" * 60)
        
        # Initialize JARVIS
        jarvis = JarvisChatbot()
        
        # Greeting
        print("\nInitializing JARVIS systems...")
        jarvis_greeting()  # Spoken greeting
        
        print("\n🎯 JARVIS is ready! Type 'help' for commands or 'quit' to exit.")
        print("💡 Tip: Try commands like:")
        print("   - 'search artificial intelligence'")
        print("   - 'open calculator'")
        print("   - 'what's the weather in New York'")
        print("   - 'generate image of a sunset'")
        print("   - 'what can you do'")
        print("-" * 60)
        
        # Main conversation loop
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print("\n🤖 JARVIS: Goodbye! It was a pleasure assisting you.")
                    break
                
                # Help command
                elif user_input.lower() == 'help':
                    print("\n🤖 JARVIS: Here are my capabilities:")
                    print(jarvis.get_capabilities())
                    continue
                
                # Clear command
                elif user_input.lower() in ['clear', 'reset']:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    jarvis.reset_memory()
                    print("🤖 JARVIS: Memory cleared and screen refreshed.")
                    continue
                
                # Process with JARVIS
                print("🤖 JARVIS: ", end="", flush=True)
                response = jarvis.respond(user_input, use_voice=False)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n🤖 JARVIS: Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("🤖 JARVIS: I encountered an error. Please try again.")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please ensure all required packages are installed:")
        print("pip install -r Requirements.txt")
    except Exception as e:
        print(f"❌ Initialization Error: {e}")

def run_gui_mode():
    """Run JARVIS with GUI interface."""
    try:
        # Try modern GUI first
        try:
            from ModernGUI import main as modern_gui_main
            print("🚀 Starting Modern JARVIS GUI...")
            modern_gui_main()
        except ImportError:
            # Fallback to original GUI
            from GUI import start_gui
            print("🚀 Starting JARVIS GUI...")
            start_gui()
    except ImportError as e:
        print(f"❌ GUI Import Error: {e}")
        print("Please ensure PyQt5 is installed: pip install PyQt5")
    except Exception as e:
        print(f"❌ GUI Error: {e}")

def run_modern_gui_mode():
    """Run JARVIS with modern GUI interface."""
    try:
        from WorkingModernGUI import main as working_gui_main
        print("🚀 Starting Working Modern JARVIS GUI...")
        working_gui_main()
    except ImportError as e:
        print(f"❌ Modern GUI Import Error: {e}")
        print("Please ensure PyQt5 is installed: pip install PyQt5")
    except Exception as e:
        print(f"❌ Modern GUI Error: {e}")

def run_voice_mode():
    """Run JARVIS in voice-only mode."""
    try:
        from Backend.Chatbot import JarvisChatbot
        from Backend.SpeechToText import start_voice_assistant
        from Backend.TextToSpeech import jarvis_greeting, speak
        
        print("🎤 Starting JARVIS Voice Mode...")
        print("Say 'JARVIS' followed by your command.")
        print("Press Ctrl+C to exit.")
        
        # Initialize JARVIS
        jarvis = JarvisChatbot()
        jarvis_greeting()
        
        def voice_callback(command: str):
            print(f"👤 Voice Command: {command}")
            response = jarvis.respond(command, use_voice=True)
            print(f"🤖 JARVIS: {response}")
        
        # Start voice assistant
        start_voice_assistant(voice_callback)
        
    except ImportError as e:
        print(f"❌ Voice Import Error: {e}")
        print("Please ensure speech recognition packages are installed.")
    except KeyboardInterrupt:
        print("\n🤖 JARVIS: Voice mode terminated. Goodbye!")
    except Exception as e:
        print(f"❌ Voice Mode Error: {e}")

def run_test_mode():
    """Run JARVIS system tests."""
    try:
        print("🧪 Running JARVIS System Tests...")
        print("=" * 50)
        
        # Test imports
        print("1. Testing imports...")
        try:
            from Backend.Chatbot import JarvisChatbot
            from Backend.Model import ModelWrapper
            from Backend.Automation import JarvisAutomation
            from Backend.RealtimeSearchEngine import JarvisSearch
            from Backend.ImageGeneration import JarvisImageGen
            from Backend.TextToSpeech import JarvisTextToSpeech
            from Backend.SpeechToText import JarvisSpeechToText
            print("   ✅ All backend modules imported successfully")
        except Exception as e:
            print(f"   ❌ Import error: {e}")
            return
        
        # Test core functionality
        print("\n2. Testing core functionality...")
        try:
            jarvis = JarvisChatbot()
            response = jarvis.respond("Hello, are you working?")
            print(f"   ✅ Chat response: {response[:50]}...")
        except Exception as e:
            print(f"   ❌ Chat error: {e}")
        
        # Test automation
        print("\n3. Testing automation...")
        try:
            automation = JarvisAutomation()
            system_info = automation.get_system_info()
            print(f"   ✅ System info retrieved: {len(system_info)} characters")
        except Exception as e:
            print(f"   ❌ Automation error: {e}")
        
        # Test search
        print("\n4. Testing search engine...")
        try:
            search = JarvisSearch()
            # Don't actually perform web search in test
            print("   ✅ Search engine initialized")
        except Exception as e:
            print(f"   ❌ Search error: {e}")
        
        # Test image generation
        print("\n5. Testing image generation...")
        try:
            image_gen = JarvisImageGen()
            # Test placeholder generation
            result = image_gen._generate_placeholder_image("test", 100, 100)
            print("   ✅ Image generation system ready")
        except Exception as e:
            print(f"   ❌ Image generation error: {e}")
        
        print("\n🎉 System test completed!")
        
    except Exception as e:
        print(f"❌ Test Error: {e}")

def show_help():
    """Show help information."""
    help_text = """
🤖 JARVIS AI Assistant

Usage: python Main.py [mode] [options]

Modes:
  console    Run in console/terminal mode (default)
  gui        Run with graphical user interface
  voice      Run in voice-only mode
  test       Run system tests
  help       Show this help message

Examples:
  python Main.py           # Console mode
  python Main.py gui       # GUI mode
  python Main.py voice     # Voice mode
  python Main.py test      # Run tests

Features:
  🗣️  Voice interaction with wake word detection
  🔍  Web search and real-time information
  🖥️  System automation and app control
  🎨  AI image generation
  🧮  Mathematical calculations
  📰  News and weather updates
  💬  Natural conversation with memory
  ⚙️  Task automation and scheduling

Setup:
  1. Install dependencies: pip install -r Requirements.txt
  2. Configure API keys in .env file (optional but recommended)
  3. Run: python Main.py

API Keys (optional):
  GROQ_API_KEY      - For advanced AI chat and speech recognition
  COHERE_API_KEY    - Alternative AI provider
  OPENAI_API_KEY    - For DALL-E image generation
  STABILITY_API_KEY - For Stable Diffusion images
  NEWS_API_KEY      - For news retrieval
  WEATHER_API_KEY   - For weather information
"""
    print(help_text)

def main():
    """Main entry point for JARVIS."""
    parser = argparse.ArgumentParser(description="JARVIS AI Assistant", add_help=False)
    parser.add_argument('mode', nargs='?', default='console', 
                       choices=['console', 'gui', 'modern', 'voice', 'test', 'help'],
                       help='Run mode for JARVIS')
    
    args = parser.parse_args()
    
    # ASCII Art Banner
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗              ║
    ║        ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝              ║
    ║        ██║███████║██████╔╝██║   ██║██║███████╗              ║
    ║   ██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║              ║
    ║   ╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║              ║
    ║    ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝              ║
    ║                                                              ║
    ║              Just A Rather Very Intelligent System           ║
    ║                     AI Assistant v2.0                       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    
    if args.mode != 'help':
        print(banner)
    
    # Route to appropriate mode
    if args.mode == 'console':
        run_console_mode()
    elif args.mode == 'gui':
        run_gui_mode()
    elif args.mode == 'modern':
        run_modern_gui_mode()
    elif args.mode == 'voice':
        run_voice_mode()
    elif args.mode == 'test':
        run_test_mode()
    elif args.mode == 'help':
        show_help()

if __name__ == "__main__":
    main()
