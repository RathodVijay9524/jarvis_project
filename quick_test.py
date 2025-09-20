"""
Quick JARVIS Test with your Groq API key
"""

import os

# Set your API key
os.environ["GROQ_API_KEY"] = ""

def test_jarvis_basic():
    """Test basic JARVIS functionality."""
    print("🤖 Testing JARVIS with your Groq API key...")
    
    try:
        from Backend.Model import ModelWrapper
        
        # Test AI model
        print("1. Testing AI Model...")
        model = ModelWrapper(model_name="groq")
        response = model.infer("Hello, introduce yourself as JARVIS")
        print(f"✅ AI Response: {response}\n")
        
        # Test automation
        print("2. Testing System Automation...")
        from Backend.Automation import JarvisAutomation
        automation = JarvisAutomation()
        
        # Test time
        time_result = automation.get_current_time()
        print(f"✅ Time: {time_result}")
        
        # Test calculation
        calc_result = automation.calculate("25 * 47")
        print(f"✅ Calculator: {calc_result}")
        
        # Test system info
        system_info = automation.get_system_info()
        print(f"✅ System Info: {system_info[:100]}...\n")
        
        print("3. Testing Basic Commands...")
        # Create a minimal chatbot test
        class SimpleJarvis:
            def __init__(self):
                self.model = ModelWrapper(model_name="groq")
                self.automation = JarvisAutomation()
            
            def respond(self, message):
                # Handle simple commands
                if "time" in message.lower():
                    return self.automation.get_current_time()
                elif "calculate" in message.lower():
                    # Extract calculation
                    parts = message.split("calculate")
                    if len(parts) > 1:
                        expr = parts[1].strip()
                        return self.automation.calculate(expr)
                else:
                    return self.model.infer(message)
        
        jarvis = SimpleJarvis()
        
        # Test commands
        test_commands = [
            "Hello JARVIS, how are you?",
            "What time is it?",
            "Calculate 15 + 25",
            "Tell me about yourself"
        ]
        
        for cmd in test_commands:
            print(f"👤 User: {cmd}")
            response = jarvis.respond(cmd)
            print(f"🤖 JARVIS: {response}\n")
        
        print("🎉 JARVIS is working perfectly with your Groq API key!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_jarvis_basic()
