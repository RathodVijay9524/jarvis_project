"""
Chatbot.py
Advanced JARVIS chatbot with Decision-Making Brain and proper query routing.
Based on Kaushik Shresth's architecture.
"""

import re
import json
import os
import time
import threading
from typing import Dict, Any, Optional
from Backend.Model import ModelWrapper, JarvisMemory
from Backend.DecisionBrain import JarvisDecisionBrain
from Backend.AdvancedAutomation import JarvisAdvancedAutomation
from Backend.RealtimeSearchEngine import JarvisSearch
from Backend.ImageGeneration import JarvisImageGen

# Import performance optimizations
try:
    from Backend.PerformanceOptimizer import get_optimizer, cached
    from Backend.ErrorHandler import get_error_handler, error_handler
    OPTIMIZATIONS_AVAILABLE = True
except ImportError:
    OPTIMIZATIONS_AVAILABLE = False
    print("⚠️ Performance optimizations not available")
from Backend.TextToSpeech import speak
import threading

class JarvisChatbot:
    def __init__(self):
        """Initialize JARVIS with all components and performance optimizations."""
        # Initialize performance systems first
        if OPTIMIZATIONS_AVAILABLE:
            self.optimizer = get_optimizer()
            self.error_handler = get_error_handler()
            print("✅ Performance optimizations enabled")
        else:
            self.optimizer = None
            self.error_handler = None
        
        # Initialize core components
        self.model = ModelWrapper()
        self.memory = JarvisMemory()
        self.decision_brain = JarvisDecisionBrain()
        self.automation = JarvisAdvancedAutomation()
        self.search_engine = JarvisSearch()
        self.image_gen = JarvisImageGen()
        
        # Initialize AI Personality system
        try:
            from .AIPersonality import JarvisAIPersonality
            self.ai_personality = JarvisAIPersonality()
            print("✅ AI Personality system initialized")
        except ImportError:
            self.ai_personality = None
            print("⚠️ AI Personality system not available")
        
        # Initialize Hindi command processor
        try:
            from .HindiCommandProcessor import JarvisHindiProcessor
            self.hindi_processor = JarvisHindiProcessor()
            print("✅ Hindi command processor initialized")
        except ImportError:
            self.hindi_processor = None
            print("⚠️ Hindi command processor not available")
        
        # Initialize Hindi response generator
        try:
            from .HindiResponseGenerator import JarvisHindiResponseGenerator
            self.hindi_response_generator = JarvisHindiResponseGenerator()
            print("✅ Hindi response generator initialized")
        except ImportError:
            self.hindi_response_generator = None
            print("⚠️ Hindi response generator not available")
        
        # Command patterns
        self.command_patterns = {
            'search': r'(?:search|find|look up|google)\s+(.+)',
            'open_app': r'(?:open|launch|start)\s+(.+)',
            'generate_image': r'(?:generate|create|make)\s+(?:an?\s+)?image\s+(?:of\s+)?(.+)',
            'weather': r'(?:weather|temperature)\s+(?:in\s+)?(.+)',
            'time': r'(?:what\s+time|current\s+time|time)',
            'date': r'(?:what\s+date|current\s+date|date|today)',
            'joke': r'(?:tell\s+me\s+a\s+)?joke',
            'news': r'(?:news|latest\s+news)\s*(?:about\s+(.+))?',
            'calculate': r'(?:calculate|compute|solve)\s+(.+)',
            'remember': r'(?:remember|save|note)\s+(.+)',
            'recall': r'(?:recall|what\s+did\s+i|remind\s+me)',
        }
    
    def respond(self, prompt: str, use_voice: bool = False) -> str:
        """
        Main response method using Decision-Making Brain architecture with performance optimizations.
        """
        start_time = time.time()
        
        try:
            # Track request for performance metrics
            if self.optimizer:
                self.optimizer.metrics['total_requests'] += 1
            
            # Process Hindi commands first
            original_prompt = prompt
            is_hindi_command = False
            
            if self.hindi_processor:
                processed_prompt, is_hindi_command = self.hindi_processor.process_hindi_command(prompt)
                if is_hindi_command:
                    prompt = processed_prompt
                    print(f"🇮🇳 Hindi command processed: '{original_prompt}' → '{prompt}'")
            
            # Analyze user input with AI Personality system
            user_name = self.memory.get_name()
            analysis = None
            if self.ai_personality:
                analysis = self.ai_personality.analyze_user_input(prompt, user_name)
            
            # Use Decision Brain to categorize the query
            category, processed_query = self.decision_brain.make_decision(prompt)
            
            # Route to appropriate handler based on category
            if category == 'automation':
                response = self.automation.process_automation_query(processed_query)
            elif category == 'realtime':
                response = self._handle_realtime_query(processed_query)
            elif category == 'personality':
                response = self._handle_personality_query(processed_query)
            else:  # general
                response = self._handle_general_query(processed_query)
            
            # Store interaction in memory
            self.memory.add_interaction(prompt, response)
            
            # Speak response if requested
            if use_voice:
                threading.Thread(target=speak, args=(response,), daemon=True).start()
            
            # Enhance response with AI Personality
            if self.ai_personality and analysis:
                response = self.ai_personality.generate_contextual_response(response, analysis)
            
            # Generate Hindi response if user spoke in Hindi
            if self.hindi_response_generator and is_hindi_command:
                # Determine command type for appropriate Hindi response
                command_type = "general"
                if "email" in original_prompt.lower() or "mail" in original_prompt.lower() or "dikhao" in original_prompt.lower():
                    command_type = "email"
                elif "mausam" in original_prompt.lower() or "weather" in original_prompt.lower():
                    command_type = "weather"
                elif "calendar" in original_prompt.lower() or "schedule" in original_prompt.lower():
                    command_type = "calendar"
                elif "madad" in original_prompt.lower() or "help" in original_prompt.lower():
                    command_type = "help"
                elif "namaste" in original_prompt.lower() or "hello" in original_prompt.lower():
                    command_type = "greeting"
                elif "dhanyawad" in original_prompt.lower() or "shukriya" in original_prompt.lower():
                    command_type = "thanks"
                
                hindi_response = self.hindi_response_generator.translate_response_to_hindi(response, command_type)
                print(f"🇮🇳 Generated Hindi response for: {original_prompt}")
                response = hindi_response
            
            # Performance monitoring
            response_time = time.time() - start_time
            if self.optimizer and response_time > 5.0:  # Log slow responses
                print(f"⚠️ Slow response: {response_time:.2f}s for query: {prompt[:50]}...")
            
            return response
            
        except Exception as e:
            # Enhanced error handling
            if self.error_handler:
                error_response = self.error_handler.handle_error(e, "chatbot_response")
            else:
                error_response = f"I apologize, but I encountered an error: {str(e)}"
            
            if use_voice:
                threading.Thread(target=speak, args=(error_response,), daemon=True).start()
            return error_response
    
    def _handle_general_query(self, query: str) -> str:
        """
        Handle general conversational queries.
        """
        try:
            # Get system prompt for general queries
            system_prompts = self.decision_brain.get_system_prompts()
            general_prompt = system_prompts['general']
            
            # Add context from memory
            context = self.memory.get_context()
            full_prompt = f"{context}\nUser: {query}" if context else query
            
            # Use AI model with general system prompt
            response = self.model.infer(full_prompt, use_system_prompt=False)
            
            # Override system prompt
            final_prompt = f"{general_prompt}\n\n{full_prompt}"
            response = self.model.infer(final_prompt, use_system_prompt=False)
            
            return response
            
        except Exception as e:
            return f"General query error: {str(e)}"
    
    def _handle_realtime_query(self, query: str) -> str:
        """
        Handle realtime information queries.
        """
        try:
            query_lower = query.lower()
            
            # Weather queries
            if "weather" in query_lower:
                location = None
                words = query.split()
                
                # Look for location indicators
                for i, word in enumerate(words):
                    if word.lower() in ["in", "at", "for"] and i + 1 < len(words):
                        location = " ".join(words[i+1:])
                        break
                
                # If no location found, try to extract city name after "weather"
                if not location:
                    weather_index = -1
                    for i, word in enumerate(words):
                        if word.lower() == "weather":
                            weather_index = i
                            break
                    
                    if weather_index >= 0 and weather_index + 1 < len(words):
                        # Take the next word as potential location
                        potential_location = words[weather_index + 1]
                        # If it's a single word, use it; otherwise try to get more context
                        if weather_index + 2 < len(words):
                            location = " ".join(words[weather_index + 1:])
                        else:
                            location = potential_location
                
                return self.search_engine.get_weather(location)
            
            # News queries
            elif "news" in query_lower:
                topic = "general"
                if "about" in query_lower:
                    topic = query_lower.split("about")[-1].strip()
                return self.search_engine.get_news(topic)
            
            # Time queries
            elif "time" in query_lower:
                from Backend.Automation import JarvisAutomation
                auto = JarvisAutomation()
                return auto.get_current_time()
            
            # Date queries  
            elif "date" in query_lower or "today" in query_lower:
                from Backend.Automation import JarvisAutomation
                auto = JarvisAutomation()
                return auto.get_current_date()
            
            # General web search
            else:
                return self.search_engine.search_web(query, 3)
                
        except Exception as e:
            return f"Realtime query error: {str(e)}"
    
    def _handle_personality_query(self, query: str) -> str:
        """
        Handle AI personality and conversation context queries.
        """
        try:
            query_lower = query.lower()
            
            # Personality profile queries
            if any(word in query_lower for word in ['personality', 'profile', 'traits', 'tell me about yourself']):
                return self.get_ai_personality_profile()
            
            # Conversation context queries
            elif any(word in query_lower for word in ['conversation', 'context', 'what are you thinking']):
                return self.get_conversation_context()
            
            # Learning insights queries
            elif any(word in query_lower for word in ['learning', 'insights', 'what have you learned']):
                return self.get_learning_insights()
            
            # Mood and emotion queries
            elif any(word in query_lower for word in ['mood', 'emotion', 'feeling', 'how are you']):
                if self.ai_personality:
                    mood = self.ai_personality.conversation_mood
                    return f"I'm feeling {mood} today. How are you doing? I'm here to help with whatever you need!"
                else:
                    return "I'm doing well, thank you for asking! How can I assist you today?"
            
            # Default personality response
            else:
                return "I'm JARVIS, your AI assistant. I'm here to help with tasks, answer questions, and make your day more productive. What would you like to know about me or how can I assist you?"
                
        except Exception as e:
            return f"Personality query error: {str(e)}"
    
    def _process_commands(self, prompt: str) -> Optional[str]:
        """
        Process specific commands and return response if matched.
        """
        prompt_lower = prompt.lower().strip()
        
        # Search command
        search_match = re.search(self.command_patterns['search'], prompt_lower)
        if search_match:
            query = search_match.group(1)
            return self.search_engine.search_web(query)
        
        # Open application command
        app_match = re.search(self.command_patterns['open_app'], prompt_lower)
        if app_match:
            app_name = app_match.group(1)
            return self.automation.open_application(app_name)
        
        # Generate image command
        image_match = re.search(self.command_patterns['generate_image'], prompt_lower)
        if image_match:
            image_prompt = image_match.group(1)
            return self.image_gen.generate_image(image_prompt)
        
        # Weather command
        weather_match = re.search(self.command_patterns['weather'], prompt_lower)
        if weather_match:
            location = weather_match.group(1)
            return self.search_engine.get_weather(location)
        
        # Time command
        if re.search(self.command_patterns['time'], prompt_lower):
            return self.automation.get_current_time()
        
        # Date command
        if re.search(self.command_patterns['date'], prompt_lower):
            return self.automation.get_current_date()
        
        # Joke command
        if re.search(self.command_patterns['joke'], prompt_lower):
            return self._get_joke()
        
        # News command
        news_match = re.search(self.command_patterns['news'], prompt_lower)
        if news_match:
            topic = news_match.group(1) if news_match.group(1) else "general"
            return self.search_engine.get_news(topic)
        
        # Calculate command
        calc_match = re.search(self.command_patterns['calculate'], prompt_lower)
        if calc_match:
            expression = calc_match.group(1)
            return self.automation.calculate(expression)
        
        # Remember command
        remember_match = re.search(self.command_patterns['remember'], prompt_lower)
        if remember_match:
            info = remember_match.group(1)
            return self._remember_info(info)
        
        # Recall command
        if re.search(self.command_patterns['recall'], prompt_lower):
            return self._recall_info()
        
        return None
    
    def _get_joke(self) -> str:
        """Get a random joke."""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my wife she was drawing her eyebrows too high. She seemed surprised.",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "I'm reading a book about anti-gravity. It's impossible to put down!",
            "Why don't eggs tell jokes? They'd crack each other up!"
        ]
        import random
        return f"Here's a joke for you: {random.choice(jokes)}"
    
    def _remember_info(self, info: str) -> str:
        """Store information in memory."""
        # Store in user preferences/notes
        if 'notes' not in self.memory.user_preferences:
            self.memory.user_preferences['notes'] = []
        
        self.memory.user_preferences['notes'].append({
            'info': info,
            'timestamp': self.memory._get_timestamp()
        })
        
        return f"I've remembered that: {info}"
    
    def _recall_info(self) -> str:
        """Recall stored information."""
        notes = self.memory.user_preferences.get('notes', [])
        if not notes:
            return "I don't have any stored information to recall."
        
        recent_notes = notes[-3:]  # Get last 3 notes
        response = "Here's what I remember:\n"
        for i, note in enumerate(recent_notes, 1):
            response += f"{i}. {note['info']} (from {note['timestamp']})\n"
        
        return response.strip()
    
    def get_capabilities(self) -> str:
        """Return a list of JARVIS capabilities."""
        capabilities = [
            "🔍 Web search and real-time information retrieval",
            "🖥️ System automation and application control",
            "🎨 AI image generation",
            "🗣️ Voice interaction and text-to-speech",
            "🧮 Mathematical calculations",
            "📅 Date and time information",
            "🌤️ Weather updates",
            "📰 Latest news retrieval",
            "🧠 Memory and note-taking",
            "💬 Natural conversation and assistance",
            "😄 Entertainment (jokes, fun facts)",
            "⚙️ Task automation and scheduling"
        ]
        
        response = "JARVIS Capabilities:\n" + "\n".join(capabilities)
        return response
    
    def reset_memory(self):
        """Reset conversation memory."""
        self.memory = JarvisMemory()
        return "Memory reset complete. Starting fresh conversation."
    
    def get_performance_stats(self) -> str:
        """Get performance statistics."""
        if not self.optimizer:
            return "Performance monitoring not available."
        
        stats = self.optimizer.get_performance_stats()
        
        response = f"""📊 JARVIS Performance Statistics:

🚀 Cache Performance:
   • Hit Rate: {stats.get('cache_hit_rate', 0)}%
   • Cache Size: {stats.get('cache_size', 0)} items
   • Cache Memory: {stats.get('cache_memory_mb', 0)} MB

⚡ Response Times:
   • Average API Time: {stats.get('avg_api_time', 0)}s
   • Total Requests: {stats.get('total_requests', 0)}

💾 Memory Usage:
   • Current Memory: {stats.get('current_memory_mb', 0)} MB
   • Background Tasks: {stats.get('background_tasks', 0)}

🔧 System Health:
   • Startup Time: {stats.get('startup_time', 0)}s
   • Error Count: {stats.get('error_count', 0)}
"""
        return response
    
    def optimize_system(self) -> str:
        """Optimize system performance."""
        if not self.optimizer:
            return "Performance optimization not available."
        
        try:
            # Force garbage collection
            collected = self.optimizer.optimize_memory()
            
            # Clean up old cache entries
            self.optimizer._cleanup_cache()
            
            return f"✅ System optimized! {collected} objects collected, cache cleaned."
            
        except Exception as e:
            return f"❌ Optimization failed: {e}"
    
    def get_ai_personality_profile(self) -> str:
        """Get AI personality profile."""
        if not self.ai_personality:
            return "❌ AI Personality system not available."
        return self.ai_personality.get_personality_profile()
    
    def get_conversation_context(self) -> str:
        """Get conversation context summary."""
        if not self.ai_personality:
            return "❌ AI Personality system not available."
        return self.ai_personality.get_conversation_summary()
    
    def get_learning_insights(self) -> str:
        """Get AI learning insights."""
        if not self.ai_personality:
            return "❌ AI Personality system not available."
        return self.ai_personality.get_learning_insights()
    
    def update_personality_trait(self, trait: str, value: float) -> str:
        """Update AI personality trait."""
        if not self.ai_personality:
            return "❌ AI Personality system not available."
        return self.ai_personality.update_personality_trait(trait, value)

# Backward compatibility
class Chatbot(JarvisChatbot):
    """Backward compatibility wrapper."""
    pass

if __name__ == "__main__":
    bot = JarvisChatbot()
    print("JARVIS initialized. Type 'quit' to exit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("JARVIS: Goodbye! It was a pleasure assisting you.")
            break
        
        response = bot.respond(user_input)
        print(f"JARVIS: {response}")
