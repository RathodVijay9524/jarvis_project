"""
JARVIS Demo with your Groq API Key
This demonstrates JARVIS capabilities without requiring all optional dependencies.
"""

import os

# Configure your API key
os.environ["GROQ_API_KEY"] = ""

def demo_jarvis():
    """Demonstrate JARVIS capabilities."""
    print("🤖 JARVIS AI Assistant Demo")
    print("=" * 50)
    
    try:
        # Import core JARVIS components
        from Backend.Model import ModelWrapper
        from Backend.Automation import JarvisAutomation
        
        # Initialize JARVIS brain
        jarvis_brain = ModelWrapper(model_name="groq")
        automation = JarvisAutomation()
        
        print("✅ JARVIS initialized with your Groq API key")
        print("🧠 AI Model: Groq LLaMA 3.1 8B")
        print("🎯 Status: All systems operational\n")
        
        # Demo commands
        demo_commands = [
            {
                "input": "Hello JARVIS, introduce yourself",
                "type": "chat"
            },
            {
                "input": "What's the current time?",
                "type": "automation",
                "function": lambda: automation.get_current_time()
            },
            {
                "input": "Calculate the square root of 144",
                "type": "automation", 
                "function": lambda: automation.calculate("sqrt(144)")
            },
            {
                "input": "Show me system information",
                "type": "automation",
                "function": lambda: automation.get_system_info()
            },
            {
                "input": "Tell me a joke about artificial intelligence",
                "type": "chat"
            },
            {
                "input": "What are your capabilities?",
                "type": "chat"
            }
        ]
        
        print("🎯 JARVIS Demo - Interactive Commands:")
        print("-" * 50)
        
        for i, cmd in enumerate(demo_commands, 1):
            print(f"\n[{i}] 👤 User: {cmd['input']}")
            
            if cmd['type'] == 'chat':
                # Use AI for general chat
                response = jarvis_brain.infer(cmd['input'])
            else:
                # Use automation functions
                response = cmd['function']()
            
            # Format response nicely
            if len(response) > 200:
                response = response[:200] + "..."
            
            print(f"🤖 JARVIS: {response}")
        
        print("\n" + "=" * 50)
        print("🎉 Demo Complete! JARVIS is ready for use.")
        print("\nTo start JARVIS:")
        print("• Console: python Main.py")
        print("• GUI: python Main.py gui (requires PyQt5)")
        print("• Voice: python Main.py voice (requires speech packages)")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")

def interactive_chat():
    """Simple interactive chat with JARVIS."""
    print("\n🗣️ Interactive Chat Mode")
    print("Type 'quit' to exit, 'time' for current time, 'calc [expression]' for calculations")
    print("-" * 50)
    
    try:
        from Backend.Model import ModelWrapper
        from Backend.Automation import JarvisAutomation
        
        jarvis = ModelWrapper(model_name="groq")
        automation = JarvisAutomation()
        
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("🤖 JARVIS: Goodbye! It was a pleasure assisting you.")
                break
            
            if user_input.lower() == 'time':
                response = automation.get_current_time()
            elif user_input.lower().startswith('calc '):
                expr = user_input[5:]
                response = automation.calculate(expr)
            else:
                response = jarvis.infer(user_input)
            
            print(f"🤖 JARVIS: {response}")
    
    except Exception as e:
        print(f"❌ Chat error: {e}")

if __name__ == "__main__":
    demo_jarvis()
    
    # Ask if user wants interactive chat
    while True:
        choice = input("\n🤔 Would you like to try interactive chat? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            interactive_chat()
            break
        elif choice in ['n', 'no']:
            print("👋 Thanks for trying JARVIS!")
            break
        else:
            print("Please enter 'y' for yes or 'n' for no")
