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
            # Use Decision Brain to categorize the query
            category, processed_query = self.decision_brain.make_decision(prompt)
            
            # Route to appropriate handler based on category
            if category == 'automation':
                response = self.automation.process_automation_query(processed_query)
            elif category == 'realtime':
                response = self._handle_realtime_query(processed_query)
            else:  # general
                response = self._handle_general_query(processed_query)
            
            # Store interaction in memory
            self.memory.add_interaction(prompt, response)
            
            # Speak response if requested
            if use_voice:
                threading.Thread(target=speak, args=(response,), daemon=True).start()
            
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
                location = "your location"  # Default
                words = query.split()
                for i, word in enumerate(words):
                    if word.lower() in ["in", "at", "for"] and i + 1 < len(words):
                        location = " ".join(words[i+1:])
                        break
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
