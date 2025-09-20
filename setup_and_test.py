"""
JARVIS Setup and Test Script
This script will configure JARVIS with your API key and run tests.
"""

import os
import sys

def setup_environment():
    """Setup environment with the provided Groq API key."""
    api_key = ""
    
    # Set environment variable for this session
    os.environ["GROQ_API_KEY"] = api_key
    os.environ["JARVIS_VOICE"] = "tony"
    os.environ["JARVIS_AI_MODEL"] = "groq"
    
    print("✅ Environment configured with Groq API key")
    return api_key

def test_groq_connection():
    """Test the Groq API connection."""
    try:
        from Backend.Model import ModelWrapper
        
        print("🧪 Testing Groq API connection...")
        
        # Initialize model with your API key
        model = ModelWrapper(model_name="groq", api_key=os.environ.get("GROQ_API_KEY"))
        
        # Test basic inference
        response = model.infer("Hello, are you JARVIS?", use_system_prompt=True)
        
        if response and "JARVIS" in response:
            print("✅ Groq API connection successful!")
            print(f"🤖 JARVIS Response: {response[:100]}...")
            return True
        else:
            print("⚠️ Groq API connected but unexpected response")
            print(f"Response: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Groq API test failed: {str(e)}")
        return False

def test_jarvis_chatbot():
    """Test the full JARVIS chatbot."""
    try:
        from Backend.Chatbot import JarvisChatbot
        
        print("🧪 Testing JARVIS Chatbot...")
        
        jarvis = JarvisChatbot()
        
        # Test basic conversation
        response = jarvis.respond("Initialize systems and tell me you're ready")
        print(f"✅ JARVIS Chatbot working!")
        print(f"🤖 Response: {response}")
        
        # Test a command
        response = jarvis.respond("What can you do?")
        print(f"🤖 Capabilities: {response[:150]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ JARVIS Chatbot test failed: {str(e)}")
        return False

def test_system_components():
    """Test other system components."""
    print("🧪 Testing System Components...")
    
    # Test Automation
    try:
        from Backend.Automation import JarvisAutomation
        automation = JarvisAutomation()
        system_info = automation.get_system_info()
        print("✅ System Automation working")
    except Exception as e:
        print(f"⚠️ Automation test failed: {e}")
    
    # Test Search Engine
    try:
        from Backend.RealtimeSearchEngine import JarvisSearch
        search = JarvisSearch()
        print("✅ Search Engine initialized")
    except Exception as e:
        print(f"⚠️ Search Engine test failed: {e}")
    
    # Test Image Generation
    try:
        from Backend.ImageGeneration import JarvisImageGen
        image_gen = JarvisImageGen()
        print("✅ Image Generation ready")
    except Exception as e:
        print(f"⚠️ Image Generation test failed: {e}")
    
    # Test Text-to-Speech
    try:
        from Backend.TextToSpeech import JarvisTextToSpeech
        tts = JarvisTextToSpeech()
        print("✅ Text-to-Speech ready")
    except Exception as e:
        print(f"⚠️ Text-to-Speech test failed: {e}")

def main():
    """Main setup and test function."""
    print("🚀 JARVIS Setup and Test")
    print("=" * 50)
    
    # Setup environment
    api_key = setup_environment()
    
    # Test Groq connection
    if not test_groq_connection():
        print("❌ Cannot proceed without working Groq API")
        return
    
    # Test JARVIS chatbot
    if not test_jarvis_chatbot():
        print("❌ JARVIS chatbot not working properly")
        return
    
    # Test other components
    test_system_components()
    
    print("\n🎉 JARVIS Setup Complete!")
    print("=" * 50)
    print("Your JARVIS AI Assistant is ready to use!")
    print("\nTo start JARVIS:")
    print("• Console Mode: python Main.py")
    print("• GUI Mode: python Main.py gui")
    print("• Voice Mode: python Main.py voice")
    print("\nNote: Make sure to rename 'jarvis_config.env' to '.env' for persistent configuration")
    
    # Quick demo
    print("\n🎯 Quick Demo:")
    try:
        from Backend.Chatbot import JarvisChatbot
        jarvis = JarvisChatbot()
        
        demo_commands = [
            "Hello JARVIS",
            "What time is it?",
            "Calculate 25 * 47",
            "Tell me a joke"
        ]
        
        for command in demo_commands:
            print(f"\n👤 Demo: {command}")
            response = jarvis.respond(command)
            print(f"🤖 JARVIS: {response}")
    
    except Exception as e:
        print(f"Demo error: {e}")

if __name__ == "__main__":
    main()
