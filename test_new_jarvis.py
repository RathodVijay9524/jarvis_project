"""
Test the new JARVIS with Decision-Making Brain architecture
"""

import os

# Set your API key
os.environ["GROQ_API_KEY"] = ""

def test_decision_brain():
    """Test the decision-making brain."""
    print("🧠 Testing JARVIS Decision-Making Brain")
    print("=" * 60)
    
    try:
        from Backend.DecisionBrain import JarvisDecisionBrain
        
        brain = JarvisDecisionBrain()
        
        test_queries = [
            # General queries
            ("Hello JARVIS", "general"),
            ("How are you?", "general"), 
            ("Tell me a joke", "general"),
            
            # Realtime queries
            ("What's the weather today?", "realtime"),
            ("Latest news about AI", "realtime"),
            ("What time is it?", "realtime"),
            
            # Automation queries
            ("Open notepad", "automation"),
            ("Create a file", "automation"),
            ("Close all folders", "automation"),
            ("Open facebook and instagram", "automation"),
            ("Send email", "automation"),
            ("Generate image of robot", "automation")
        ]
        
        for query, expected in test_queries:
            category, processed = brain.make_decision(query)
            status = "✅" if category == expected else "❌"
            print(f"{status} '{query}' -> {category.upper()} (expected: {expected.upper()})")
        
        return True
        
    except Exception as e:
        print(f"❌ Decision brain error: {e}")
        return False

def test_automation_system():
    """Test the advanced automation system."""
    print("\n🤖 Testing Advanced Automation System")
    print("=" * 60)
    
    try:
        from Backend.AdvancedAutomation import JarvisAdvancedAutomation
        
        automation = JarvisAdvancedAutomation()
        
        test_queries = [
            "create a file for email",
            "open facebook",
            "create email draft",
            "close all folders"
        ]
        
        for query in test_queries:
            print(f"\n📝 Testing: '{query}'")
            result = automation.process_automation_query(query)
            print(f"🔧 Result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Automation error: {e}")
        return False

def test_full_jarvis():
    """Test the complete JARVIS system."""
    print("\n🚀 Testing Complete JARVIS System")
    print("=" * 60)
    
    try:
        from Backend.Chatbot import JarvisChatbot
        
        jarvis = JarvisChatbot()
        
        test_queries = [
            "Hello JARVIS, how are you?",
            "What time is it?", 
            "Create a file called test.txt",
            "Open notepad",
            "Search for AI news",
            "Tell me a joke"
        ]
        
        for query in test_queries:
            print(f"\n👤 User: {query}")
            response = jarvis.respond(query)
            print(f"🤖 JARVIS: {response[:150]}{'...' if len(response) > 150 else ''}")
        
        return True
        
    except Exception as e:
        print(f"❌ Full JARVIS error: {e}")
        return False

def main():
    """Main test function."""
    print("🔧 JARVIS New Architecture Test")
    print("Based on Kaushik Shresth's Decision-Making Brain")
    print("=" * 70)
    
    success_count = 0
    
    # Test decision brain
    if test_decision_brain():
        success_count += 1
    
    # Test automation
    if test_automation_system():
        success_count += 1
    
    # Test full system
    if test_full_jarvis():
        success_count += 1
    
    print(f"\n🎯 Test Results: {success_count}/3 systems working")
    
    if success_count == 3:
        print("🎉 All systems operational! JARVIS is ready with the new architecture.")
        print("\nTo use JARVIS:")
        print("• python Main.py           # Console mode")
        print("• python Main.py gui       # GUI mode")
    else:
        print("⚠️ Some systems need attention. Check the errors above.")

if __name__ == "__main__":
    main()
