"""
Model.py
AI Model wrappers and loading utilities for Jarvis.
"""

import os
import time
from typing import Optional
import requests
import json
from dotenv import load_dotenv

# Import performance optimizations
try:
    from .PerformanceOptimizer import get_optimizer, cached
    from .ErrorHandler import get_error_handler, error_handler
    OPTIMIZATIONS_AVAILABLE = True
except ImportError:
    OPTIMIZATIONS_AVAILABLE = False
    print("⚠️ Performance optimizations not available")

load_dotenv()

class ModelWrapper:
    def __init__(self, model_name="groq", api_key: Optional[str] = None):
        self.model_name = model_name
        self.groq_api_key = api_key or os.getenv("GROQ_API_KEY")
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        
        # Initialize performance optimizations
        if OPTIMIZATIONS_AVAILABLE:
            self.optimizer = get_optimizer()
            self.error_handler = get_error_handler()
        else:
            self.optimizer = None
            self.error_handler = None
        
        # Jarvis personality and context
        self.system_prompt = """
        You are JARVIS, an advanced AI assistant inspired by Tony Stark's AI. You are:
        - Intelligent, witty, and sophisticated
        - Capable of controlling systems, searching the web, generating images, and automating tasks
        - Professional yet friendly, with occasional subtle humor
        - Always helpful and efficient in your responses
        - Able to understand context and maintain conversation flow
        
        Your capabilities include:
        - Web searching and real-time information retrieval
        - System automation and app control
        - Image generation and analysis
        - Voice interaction and natural conversation
        - Task scheduling and reminders
        - File management and organization
        
        Respond as JARVIS would - concise, intelligent, and ready to assist.
        """

    def infer(self, prompt: str, use_system_prompt: bool = True) -> str:
        """
        Generate AI response using the configured model with performance optimizations.
        """
        try:
            # Create cache key for this inference
            cache_key = f"inference:{self.model_name}:{hash(prompt + str(use_system_prompt))}"
            
            # Try to get cached result
            if self.optimizer:
                cached_result = self.optimizer.get_cached_result(cache_key)
                if cached_result is not None:
                    print(f"🚀 Cache hit for inference")
                    return cached_result
            
            # Generate fresh response
            start_time = time.time()
            
            if self.model_name == "groq" and self.groq_api_key:
                result = self._groq_inference(prompt, use_system_prompt)
            elif self.model_name == "cohere" and self.cohere_api_key:
                result = self._cohere_inference(prompt, use_system_prompt)
            else:
                result = self._fallback_response(prompt)
            
            # Cache the result
            if self.optimizer:
                self.optimizer.cache_result(cache_key, result, ttl=1800)  # Cache for 30 minutes
                print(f"🌐 Inference completed in {time.time() - start_time:.2f}s")
            
            return result
            
        except Exception as e:
            if self.error_handler:
                error_msg = self.error_handler.handle_error(e, "model_inference")
                return error_msg
            else:
                return f"I apologize, but I'm experiencing some technical difficulties: {str(e)}"

    def _groq_inference(self, prompt: str, use_system_prompt: bool) -> str:
        """
        Use Groq API for inference.
        """
        try:
            import groq
            client = groq.Groq(api_key=self.groq_api_key)
            
            messages = []
            if use_system_prompt:
                messages.append({"role": "system", "content": self.system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Updated to current supported model
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return completion.choices[0].message.content
        except Exception as e:
            return f"Groq API error: {str(e)}"

    def _cohere_inference(self, prompt: str, use_system_prompt: bool) -> str:
        """
        Use Cohere API for inference.
        """
        try:
            import cohere
            co = cohere.Client(self.cohere_api_key)
            
            full_prompt = prompt
            if use_system_prompt:
                full_prompt = f"{self.system_prompt}\n\nUser: {prompt}\nJARVIS:"
            
            response = co.generate(
                model='command',
                prompt=full_prompt,
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.generations[0].text.strip()
        except Exception as e:
            return f"Cohere API error: {str(e)}"

    def _fallback_response(self, prompt: str) -> str:
        """
        Fallback response when no API is available.
        """
        responses = {
            "hello": "Good day! JARVIS at your service. How may I assist you today?",
            "how are you": "All systems operational and ready to assist, thank you for asking.",
            "what can you do": "I can help with web searches, system automation, image generation, voice interaction, and much more. What would you like me to help you with?",
            "initialize": "JARVIS systems initialized. All modules online and ready for operation.",
        }
        
        prompt_lower = prompt.lower().strip()
        for key, response in responses.items():
            if key in prompt_lower:
                return response
        
        return f"I understand you're asking about: {prompt}. However, I need my AI models configured to provide a more detailed response. Please set up your GROQ_API_KEY or COHERE_API_KEY in your environment variables."

class JarvisMemory:
    """
    Simple memory system for context and conversation history.
    """
    def __init__(self, max_history: int = 10):
        self.conversation_history = []
        self.user_preferences = {}
        self.max_history = max_history
        self.personal_info = {}
    
    def add_interaction(self, user_input: str, jarvis_response: str):
        """Add interaction to memory."""
        self.conversation_history.append({
            "user": user_input,
            "jarvis": jarvis_response,
            "timestamp": self._get_timestamp()
        })
        
        # Keep only recent history
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
    
    def get_context(self) -> str:
        """Get recent conversation context."""
        if not self.conversation_history:
            return ""
        
        context = "Recent conversation:\n"
        for interaction in self.conversation_history[-3:]:  # Last 3 interactions
            context += f"User: {interaction['user']}\n"
            context += f"JARVIS: {interaction['jarvis']}\n"
        
        return context
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def store_name(self, name: str):
        """Store user's name."""
        self.personal_info['name'] = name
    
    def get_name(self) -> str:
        """Get user's name."""
        return self.personal_info.get('name', 'User')
    
    def store_personal_info(self, key: str, value: str):
        """Store personal information."""
        self.personal_info[key] = value
    
    def get_personal_info(self, key: str) -> str:
        """Get personal information."""
        return self.personal_info.get(key, '')
    
    def detect_name_from_input(self, user_input: str) -> bool:
        """Detect if user is introducing their name."""
        import re
        patterns = [
            r"my name is (\w+)",
            r"i am (\w+)",
            r"i'm (\w+)",
            r"call me (\w+)",
            r"i go by (\w+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                name = match.group(1).capitalize()
                self.store_name(name)
                return True
        return False
    
    def get_personalized_context(self) -> str:
        """Get personalized context with user's name."""
        name = self.get_name()
        if name != 'User':
            return f"User's name: {name}\n"
        return ""
