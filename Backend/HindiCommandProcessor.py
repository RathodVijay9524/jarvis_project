"""
HindiCommandProcessor.py
Processes Hindi voice commands and translates them to English for JARVIS execution.
"""

import re
from typing import Dict, Optional, Tuple

class JarvisHindiProcessor:
    """
    Processes Hindi commands and translates them to equivalent English commands
    that JARVIS can understand and execute.
    """
    
    def __init__(self):
        # Hindi to English command mappings
        self.hindi_commands = {
            # Email commands
            "ईमेल दिखाओ": "read my emails",
            "ईमेल पढ़ो": "read my emails", 
            "इनबॉक्स दिखाओ": "check inbox",
            "मेल दिखाओ": "read my emails",
            "नया ईमेल": "unread emails",
            "अनपढ़ ईमेल": "unread emails",
            
            # Weather commands
            "मौसम बताओ": "what's the weather",
            "आज का मौसम": "weather today",
            "मौसम कैसा है": "how's the weather",
            "तापमान बताओ": "what's the temperature",
            "बारिश होगी": "will it rain",
            
            # Calendar commands
            "कैलेंडर दिखाओ": "show my calendar",
            "आज का कार्यक्रम": "show my schedule for today",
            "कल का कार्यक्रम": "show my schedule for tomorrow",
            "रिमाइंडर दिखाओ": "what reminders do I have",
            "याददाश्त दिखाओ": "what reminders do I have",
            
            # Application commands
            "खोलो": "open",
            "बंद करो": "close",
            "चलाओ": "start",
            "रोको": "stop",
            
            # Music commands
            "संगीत चलाओ": "play music",
            "गाना चलाओ": "play song",
            "संगीत बंद करो": "stop music",
            "आवाज़ तेज़ करो": "volume up",
            "आवाज़ धीमी करो": "volume down",
            
            # General commands
            "नमस्ते": "hello",
            "धन्यवाद": "thank you",
            "अलविदा": "goodbye",
            "हाँ": "yes",
            "नहीं": "no",
            "रुको": "wait",
            "मदद करो": "help me",
            
            # Personal commands
            "मेरा नाम क्या है": "what's my name",
            "मैं कौन हूँ": "who am I",
            "तुम कौन हो": "who are you",
            "तुम्हारा नाम क्या है": "what's your name",
            
            # Time and date
            "समय बताओ": "what time is it",
            "आज कौन सा दिन है": "what day is today",
            "तारीख बताओ": "what's the date",
            
            # Search commands
            "खोजो": "search",
            "ढूंढो": "find",
            "बताओ": "tell me about",
            
            # File operations
            "फाइल बनाओ": "create file",
            "फोल्डर खोलो": "open folder",
            "डॉक्यूमेंट बनाओ": "create document",
        }
        
        # Mixed language patterns (Hindi words with English structure)
        self.mixed_patterns = {
            # Email commands
            r"email\s*dikhao": "read my emails",
            r"mail\s*dikhao": "read my emails",
            r"inbox\s*dikhao": "check inbox",
            r"email\s*dikha": "read my emails",
            r"mail\s*dikha": "read my emails",
            
            # Calendar commands  
            r"calendar\s*dikhao": "show my calendar",
            r"calendar\s*dikha": "show my calendar",
            r"schedule\s*dikhao": "show my schedule",
            r"reminder\s*dikhao": "what reminders do I have",
            
            # Weather commands
            r"mausam\s*batao": "weather in Pune",  # Default to Pune for Hindi users
            r"mausam\s*bata": "weather in Pune", 
            r"weather\s*batao": "weather in Pune",
            r"weather\s*bata": "weather in Pune",
            r"pune\s*ka\s*mausam": "weather in Pune",
            r"mumbai\s*ka\s*mausam": "weather in Mumbai",
            r"delhi\s*ka\s*mausam": "weather in Delhi",
            
            # Music commands
            r"music\s*chalao": "play music",
            r"music\s*chala": "play music",
            r"song\s*chalao": "play song",
            r"gana\s*chalao": "play song",
            
            # Application commands
            r"app\s*kholo": "open application",
            r"application\s*kholo": "open application",
            r"\w+\s*kholo": "open",
            
            # Personal commands - Name setting vs asking
            r"mera\s*naam\s+\w+\s*hai": "my name is",  # "mera naam Vijay hai"
            r"naam\s*kya\s*hai": "what's my name",     # "naam kya hai"
            r"mera\s*naam\s*kya\s*hai": "what's my name",  # "mera naam kya hai"
            r"mera\s*naam(?!\s+\w+\s*hai)": "what's my name",  # "mera naam" alone
            
            # Help commands
            r"aap\s*meri\s*kaise\s*madad": "how can you help me",
            r"kaise\s*madad\s*kar\s*sakte": "how can you help me", 
            r"madad\s*kar\s*sakte\s*ho": "how can you help me",
            r"kya\s*kar\s*sakte\s*ho": "what can you do",
            r"aap\s*kya\s*kar\s*sakte": "what can you do",
            
            # Reminder commands
            r"mujhe\s*yaad\s*dilana": "remind me",
            r"reminder\s*set\s*karo": "set reminder",
            r"yaad\s*rakhna": "remember this",
            
            # General conversation
            r"kaise\s*ho": "how are you",
            r"kya\s*haal\s*hai": "how are you",
            r"namaste": "hello",
            r"dhanyawad": "thank you",
            r"shukriya": "thank you",
            
            # File operations
            r"file\s*banao": "create file",
            r"document\s*banao": "create document",
            
            # Time and date commands
            r"time\s*batao": "what time is it",
            r"samay\s*batao": "what time is it",
            r"date\s*batao": "what's the date",
            r"tarikh\s*batao": "what's the date",
            r"aaj\s*ka\s*din": "what day is today",
            r"aaj\s*kaun\s*sa\s*din": "what day is today",
            r"din\s*kaun\s*sa\s*hai": "what day is today",
            r"aaj\s*ka\s*din\s*kaun\s*sa\s*hai": "what day is today",
        }
        
        # Location mappings for weather
        self.location_mappings = {
            "पुणे": "Pune",
            "मुंबई": "Mumbai", 
            "दिल्ली": "Delhi",
            "बेंगलुरु": "Bangalore",
            "चेन्नई": "Chennai",
            "कोलकाता": "Kolkata",
            "हैदराबाद": "Hyderabad",
            "अहमदाबाद": "Ahmedabad",
            "जयपुर": "Jaipur",
            "लखनऊ": "Lucknow"
        }
    
    def process_hindi_command(self, command: str) -> Tuple[str, bool]:
        """
        Process a Hindi command and convert it to English equivalent.
        
        Args:
            command: Hindi command text
            
        Returns:
            Tuple[str, bool]: (processed_command, is_hindi_command)
        """
        try:
            command = command.strip()
            command_lower = command.lower()
            
            # Remove language flags if present
            if command.startswith(("🇮🇳", "🇺🇸")):
                command = command[2:].strip()
                command_lower = command.lower()
            
            # Check for exact Hindi command matches
            for hindi_cmd, english_cmd in self.hindi_commands.items():
                if hindi_cmd.lower() in command_lower or command_lower in hindi_cmd.lower():
                    print(f"🇮🇳 Hindi command detected: '{command}' → '{english_cmd}'")
                    return english_cmd, True
            
            # Check for partial Hindi word matches (more robust)
            hindi_keywords = {
                "ईमेल": "read my emails",
                "मेल": "read my emails", 
                "इनबॉक्स": "check inbox",
                "मौसम": "what's the weather",
                "कैलेंडर": "show my calendar",
                "समय": "what time is it",
                "तारीख": "what's the date",
                "संगीत": "play music",
                "गाना": "play song",
                "रिमाइंडर": "what reminders do I have",
                "याददाश्त": "what reminders do I have",
                "मदद": "help me",
                "सहायता": "help me",
                "कैसे": "how can you help me",
                "क्या": "what can you do",
                "हैलो": "hello",
                "नमस्ते": "hello",
                "धन्यवाद": "thank you",
                "शुक्रिया": "thank you",
                "दिन": "what day is today",
                "आज": "today",
                "कल": "tomorrow",
                "कैसे": "how",
                "क्या": "what",
                "कौन": "who",
                "कहाँ": "where",
                "कब": "when"
            }
            
            for hindi_word, english_cmd in hindi_keywords.items():
                if hindi_word in command:
                    print(f"🇮🇳 Hindi keyword detected: '{command}' contains '{hindi_word}' → '{english_cmd}'")
                    return english_cmd, True
            
            # Check for mixed language patterns
            for pattern, english_cmd in self.mixed_patterns.items():
                if re.search(pattern, command_lower):
                    # Special handling for name setting
                    if "mera naam" in command_lower and "hai" in command_lower:
                        # Extract the name and create proper command
                        name_match = re.search(r'mera\s*naam\s+(\w+)\s*hai', command_lower)
                        if name_match:
                            name = name_match.group(1)
                            english_cmd = f"my name is {name}"
                    
                    print(f"🌐 Mixed language detected: '{command}' → '{english_cmd}'")
                    return english_cmd, True
            
            # Check for location mappings in weather queries
            for hindi_location, english_location in self.location_mappings.items():
                if hindi_location in command:
                    # Replace Hindi location with English
                    processed_command = command.replace(hindi_location, english_location)
                    print(f"🗺️ Location translated: '{command}' → '{processed_command}'")
                    return processed_command, True
            
            # Check if command contains Hindi characters
            has_hindi = any('\u0900' <= char <= '\u097F' for char in command)
            
            if has_hindi:
                # Try to find partial matches
                for hindi_word in self.hindi_commands.keys():
                    for word in hindi_word.split():
                        if word in command:
                            english_equivalent = self.hindi_commands[hindi_word]
                            print(f"🔍 Partial Hindi match: '{command}' → '{english_equivalent}'")
                            return english_equivalent, True
                
                # If no match found but contains Hindi, try common patterns
                if "दिखाओ" in command or "बताओ" in command:
                    if "ईमेल" in command or "मेल" in command:
                        return "read my emails", True
                    elif "मौसम" in command:
                        return "what's the weather", True
                    elif "कैलेंडर" in command:
                        return "show my calendar", True
                    elif "समय" in command:
                        return "what time is it", True
                    elif "तारीख" in command:
                        return "what's the date", True
                
                print(f"❓ Hindi command not recognized: '{command}'")
                return f"I heard you say '{command}' in Hindi, but I'm not sure what you want me to do. Can you try saying it in English or use one of these Hindi commands: ईमेल दिखाओ, मौसम बताओ, कैलेंडर दिखाओ", True
            
            # Not a Hindi command
            return command, False
            
        except Exception as e:
            print(f"❌ Error processing Hindi command: {e}")
            return command, False
    
    def get_hindi_help(self) -> str:
        """Get help for Hindi commands."""
        return """🇮🇳 **हिंदी कमांड्स (Hindi Commands)**

📧 **ईमेल (Email):**
   • "ईमेल दिखाओ" - Show emails
   • "इनबॉक्स दिखाओ" - Check inbox
   • "नया ईमेल" - Unread emails

🌤️ **मौसम (Weather):**
   • "मौसम बताओ" - Tell weather
   • "आज का मौसम" - Today's weather
   • "पुणे का मौसम" - Pune weather

📅 **कैलेंडर (Calendar):**
   • "कैलेंडर दिखाओ" - Show calendar
   • "आज का कार्यक्रम" - Today's schedule
   • "रिमाइंडर दिखाओ" - Show reminders

🎵 **संगीत (Music):**
   • "संगीत चलाओ" - Play music
   • "गाना चलाओ" - Play song
   • "संगीत बंद करो" - Stop music

💻 **एप्लिकेशन (Applications):**
   • "खोलो" - Open
   • "बंद करो" - Close
   • "चलाओ" - Start

🕒 **समय (Time):**
   • "समय बताओ" - Tell time
   • "तारीख बताओ" - Tell date
   • "आज कौन सा दिन है" - What day is today

🌐 **Mixed Commands Also Work:**
   • "email dikhao"
   • "calendar dikhao" 
   • "mausam batao"
   • "music chalao"

💡 **Examples:**
   • "ईमेल दिखाओ" → Shows your emails
   • "पुणे का मौसम बताओ" → Shows Pune weather
   • "कल का कार्यक्रम दिखाओ" → Shows tomorrow's schedule
"""

# Global processor instance
_hindi_processor = None

def get_hindi_processor() -> JarvisHindiProcessor:
    """Get the global Hindi processor instance."""
    global _hindi_processor
    if _hindi_processor is None:
        _hindi_processor = JarvisHindiProcessor()
    return _hindi_processor

def process_command(command: str) -> Tuple[str, bool]:
    """Quick function to process a command."""
    processor = get_hindi_processor()
    return processor.process_hindi_command(command)

if __name__ == "__main__":
    # Test the Hindi processor
    processor = JarvisHindiProcessor()
    
    test_commands = [
        "ईमेल दिखाओ",
        "मौसम बताओ", 
        "कैलेंडर दिखाओ",
        "email dikhao",
        "mausam batao",
        "पुणे का मौसम",
        "aaj ka din kaun sa hai",
        "mera naam Vijay hai",
        "check inbox",
        "hello"
    ]
    
    print("🧪 Testing Hindi Command Processor")
    print("=" * 50)
    
    for cmd in test_commands:
        processed, is_hindi = processor.process_hindi_command(cmd)
        flag = "🇮🇳" if is_hindi else "🇺🇸"
        print(f"{flag} '{cmd}' → '{processed}'")
    
    print("\n✅ Test completed!")
