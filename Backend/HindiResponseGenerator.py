"""
HindiResponseGenerator.py
Generates Hindi responses for JARVIS when user speaks in Hindi.
"""

from typing import Dict, Optional
import re

class JarvisHindiResponseGenerator:
    """
    Generates appropriate Hindi responses for JARVIS based on English responses.
    """
    
    def __init__(self):
        # English to Hindi response mappings
        self.response_mappings = {
            # Email responses
            "INBOX Emails": "📧 **इनबॉक्स ईमेल**",
            "emails": "ईमेल",
            "Business Inquiry": "व्यापारिक पूछताछ",
            "From:": "भेजने वाला:",
            "Date:": "तारीख:",
            "Preview:": "पूर्वावलोकन:",
            
            # Weather responses
            "Weather for": "मौसम",
            "Temperature:": "तापमान:",
            "Condition:": "स्थिति:",
            "Wind:": "हवा:",
            "Forecast:": "पूर्वानुमान:",
            "Source:": "स्रोत:",
            "Last updated:": "अंतिम अपडेट:",
            
            # Calendar responses
            "Calendar Events": "📅 **कैलेंडर कार्यक्रम**",
            "Active Reminders": "📋 **सक्रिय रिमाइंडर**",
            "Today's Schedule": "📅 **आज का कार्यक्रम**",
            "No events scheduled": "कोई कार्यक्रम निर्धारित नहीं",
            "Reminders:": "रिमाइंडर:",
            
            # General responses
            "Hello": "नमस्ते",
            "Thank you": "धन्यवाद",
            "You're welcome": "आपका स्वागत है",
            "How can I help": "मैं आपकी कैसे मदद कर सकता हूँ",
            "I can help you with": "मैं आपकी मदद कर सकता हूँ",
            "Good morning": "सुप्रभात",
            "Good evening": "शुभ संध्या",
            "Good night": "शुभ रात्रि",
            
            # Time responses
            "Today is": "आज है",
            "The time is": "समय है",
            "Current date": "वर्तमान तारीख",
            
            # Error messages
            "Error": "त्रुटि",
            "Not available": "उपलब्ध नहीं",
            "Please try again": "कृपया पुनः प्रयास करें",
            "Unable to": "असमर्थ",
            
            # Status messages
            "Success": "सफल",
            "Completed": "पूर्ण",
            "Working": "काम कर रहा",
            "Ready": "तैयार",
        }
        
        # Common Hindi phrases for responses
        self.hindi_phrases = {
            "greeting": [
                "नमस्ते! मैं JARVIS हूँ, आपका AI सहायक।",
                "आपका स्वागत है! मैं आपकी कैसे मदद कर सकता हूँ?",
                "नमस्कार! मैं यहाँ आपकी सेवा के लिए हूँ।"
            ],
            "help": [
                "मैं आपकी निम्नलिखित चीजों में मदद कर सकता हूँ:",
                "📧 ईमेल पढ़ना और भेजना",
                "🌤️ मौसम की जानकारी",
                "📅 कैलेंडर और रिमाइंडर",
                "🎵 संगीत चलाना",
                "💻 एप्लिकेशन खोलना",
                "🔍 इंटरनेट पर खोज करना"
            ],
            "email_intro": "📧 **आपके ईमेल:**",
            "weather_intro": "🌤️ **मौसम की जानकारी:**",
            "calendar_intro": "📅 **आपका कैलेंडर:**",
            "error": "माफ करें, मुझे समझ नहीं आया। कृपया फिर से कोशिश करें।",
            "thanks": "आपका स्वागत है! और कुछ चाहिए?",
            "goodbye": "अलविदा! अच्छा दिन हो!"
        }
    
    def should_respond_in_hindi(self, original_command: str) -> bool:
        """Check if the response should be in Hindi based on the original command."""
        command_lower = original_command.lower()
        
        # Check for Hindi script
        has_hindi_script = any('\u0900' <= char <= '\u097F' for char in original_command)
        
        # Check for transliterated Hindi words
        hindi_words = [
            "dikhao", "dikha", "batao", "bata", "chalao", "chala", "kholo", "karo",
            "mausam", "email", "calendar", "mera", "naam", "kya", "hai", "aap",
            "kaise", "madad", "kar", "sakte", "ho", "mujhe", "yaad", "namaste",
            "dhanyawad", "shukriya", "kaise", "haal"
        ]
        
        has_hindi_words = any(word in command_lower for word in hindi_words)
        
        return has_hindi_script or has_hindi_words
    
    def translate_response_to_hindi(self, english_response: str, command_type: str = "general") -> str:
        """
        Translate English response to Hindi.
        
        Args:
            english_response: The English response from JARVIS
            command_type: Type of command (email, weather, calendar, general)
            
        Returns:
            str: Hindi version of the response
        """
        try:
            hindi_response = english_response
            
            # Apply basic translations carefully
            for english_text, hindi_text in self.response_mappings.items():
                if english_text in hindi_response:
                    hindi_response = hindi_response.replace(english_text, hindi_text)
            
            # Add Hindi intro based on command type
            if command_type == "email" and "emails" in english_response.lower():
                hindi_response = f"{self.hindi_phrases['email_intro']}\n\n{hindi_response}"
            elif command_type == "weather":
                # Only add intro if it's not already a weather response
                if "Weather for" in english_response and "मौसम की जानकारी" not in hindi_response:
                    hindi_response = f"{self.hindi_phrases['weather_intro']}\n\n{hindi_response}"
            elif command_type == "calendar" and ("calendar" in english_response.lower() or "schedule" in english_response.lower()):
                hindi_response = f"{self.hindi_phrases['calendar_intro']}\n\n{hindi_response}"
            elif command_type == "help":
                hindi_response = "\n".join(self.hindi_phrases['help'])
            elif command_type == "greeting":
                hindi_response = self.hindi_phrases['greeting'][0]
            elif command_type == "thanks":
                hindi_response = self.hindi_phrases['thanks']
            
            # Add Hindi closing
            if not any(phrase in hindi_response for phrase in ["आपका स्वागत", "और कुछ", "कैसे मदद"]):
                hindi_response += "\n\n🇮🇳 और कुछ चाहिए? (Need anything else?)"
            
            return hindi_response
            
        except Exception as e:
            print(f"❌ Error translating to Hindi: {e}")
            return english_response
    
    def get_hindi_help_response(self) -> str:
        """Get comprehensive help response in Hindi."""
        return """🇮🇳 **मैं आपकी कैसे मदद कर सकता हूँ?**

📧 **ईमेल (Email):**
   • "email dikhao" - ईमेल दिखाएं
   • "inbox dikhao" - इनबॉक्स देखें
   • "mail bhejo" - मेल भेजें

🌤️ **मौसम (Weather):**
   • "mausam batao" - मौसम बताएं
   • "aaj ka mausam" - आज का मौसम
   • "pune ka mausam" - पुणे का मौसम

📅 **कैलेंडर (Calendar):**
   • "calendar dikhao" - कैलेंडर दिखाएं
   • "aaj ka schedule" - आज का कार्यक्रम
   • "reminder dikhao" - रिमाइंडर दिखाएं

🎵 **संगीत (Music):**
   • "music chalao" - संगीत चलाएं
   • "gana bajao" - गाना बजाएं

💻 **एप्लिकेशन (Apps):**
   • "calculator kholo" - कैलकुलेटर खोलें
   • "chrome kholo" - क्रोम खोलें

🔍 **खोज (Search):**
   • "google par dhundo" - गूगल पर खोजें
   • "search karo" - सर्च करें

👤 **व्यक्तिगत (Personal):**
   • "mera naam kya hai" - मेरा नाम क्या है
   • "time batao" - समय बताओ
   • "date batao" - तारीख बताओ

💡 **उदाहरण (Examples):**
   • "email dikhao" → आपके ईमेल दिखाता है
   • "mausam batao" → मौसम की जानकारी देता है
   • "calendar dikhao" → आपका कैलेंडर दिखाता है

🇮🇳 **आप हिंदी और अंग्रेजी दोनों में बात कर सकते हैं!**"""

# Global response generator instance
_hindi_generator = None

def get_hindi_generator() -> JarvisHindiResponseGenerator:
    """Get the global Hindi response generator."""
    global _hindi_generator
    if _hindi_generator is None:
        _hindi_generator = JarvisHindiResponseGenerator()
    return _hindi_generator

def generate_hindi_response(english_response: str, original_command: str, command_type: str = "general") -> str:
    """Quick function to generate Hindi response."""
    generator = get_hindi_generator()
    
    if generator.should_respond_in_hindi(original_command):
        return generator.translate_response_to_hindi(english_response, command_type)
    else:
        return english_response

if __name__ == "__main__":
    # Test the Hindi response generator
    generator = JarvisHindiResponseGenerator()
    
    test_cases = [
        ("email dikhao", "📧 **INBOX Emails** (3 emails)\n\n📭 **1. Business Inquiry**", "email"),
        ("mausam batao", "🌤️ **Weather for Pune**\n\n🌡️ Temperature: 25°C", "weather"),
        ("aap meri kaise madad kar sakte ho", "I can help you with various tasks", "help"),
        ("hello", "Hello! How can I help you?", "greeting")
    ]
    
    print("🧪 Testing Hindi Response Generation")
    print("=" * 60)
    
    for command, english_resp, cmd_type in test_cases:
        should_hindi = generator.should_respond_in_hindi(command)
        if should_hindi:
            hindi_resp = generator.translate_response_to_hindi(english_resp, cmd_type)
            print(f"\n🇮🇳 Command: '{command}'")
            print(f"English: {english_resp[:50]}...")
            print(f"Hindi: {hindi_resp[:100]}...")
        else:
            print(f"\n🇺🇸 Command: '{command}' (English response)")
    
    print("\n✅ Test completed!")
