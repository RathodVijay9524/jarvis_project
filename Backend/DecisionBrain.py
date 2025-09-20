"""
DecisionBrain.py
Advanced Decision-Making Model for JARVIS - Based on Kaushik Shresth's architecture
Categorizes queries into General, Realtime, and Automation types
"""

import os
from typing import Tuple, Dict, Any
from Backend.Model import ModelWrapper

class JarvisDecisionBrain:
    """
    Decision-Making Brain that categorizes user queries and routes them appropriately.
    Based on Kaushik Shresth's architecture from GitHub gist.
    """
    
    def __init__(self, username: str = "User", assistant_name: str = "JARVIS"):
        self.username = username
        self.assistant_name = assistant_name
        self.model = ModelWrapper()
        
        # Decision-making prompt based on the GitHub gist
        self.decision_prompt = f"""
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write a application and open it in notepad'

*** Do not answer any query, just decide what kind of query is given to you. ***

-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'can you help me with this math problem?' respond with 'general can you help me with this math problem?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.' , if the query is 'what is python programming language?' respond with 'general what is python programming language?'

-> Respond with 'realtime ( query )' if a query requires real-time up-to-date information from the internet like if the query is 'who is elon musk?' respond with 'realtime who is elon musk?', if the query is 'what's mark's networth?' respond with 'realtime what's mark's networth?', if the query is 'what's the weather outside?' respond with 'realtime what's the weather outside?', if the query is 'tell me about kaushik shresth.' respond with 'realtime tell me about kaushik shresth.', if the query is 'what is the latest news?' respond with 'realtime what is the latest news?', if the query is 'current time' respond with 'realtime current time', if the query is 'today's date' respond with 'realtime today's date'

-> Respond with 'automation ( query )' if the query is asking to perform any task or automation like opening apps, creating files, controlling system, etc. like if the query is 'open facebook and instagram.' respond with 'automation open facebook and instagram.', if the query is 'Remind me when it's 10 PM.' respond with 'automation Remind me when it's 10 PM.', if the query is 'Write a song for me.' respond with 'automation Write a song for me.', if the query is 'Generate an image of tony stark.' respond with 'automation Generate an image of tony stark.', if the query is 'open notepad' respond with 'automation open notepad', if the query is 'create a file' respond with 'automation create a file', if the query is 'close all windows' respond with 'automation close all windows', if the query is 'send email' respond with 'automation send email'

Remember:
- Only classify the query type, don't answer it
- Always include the original query in your response
- Be accurate in classification
- Focus on the intent of the user
"""

    def make_decision(self, query: str) -> Tuple[str, str]:
        """
        Analyze the user query and decide which type of response is needed.
        
        Args:
            query: User's input query
            
        Returns:
            Tuple[str, str]: (category, processed_query)
            - category: 'general', 'realtime', or 'automation'
            - processed_query: the original query for processing
        """
        try:
            # Get decision from AI model
            decision_response = self.model.infer(
                f"Query: {query}", 
                use_system_prompt=False
            )
            
            # Override with custom prompt
            full_prompt = f"{self.decision_prompt}\n\nQuery: {query}"
            decision_response = self.model.infer(full_prompt, use_system_prompt=False)
            
            # Parse the response
            decision_response = decision_response.lower().strip()
            
            if decision_response.startswith('general'):
                category = 'general'
                processed_query = decision_response.replace('general', '').strip()
            elif decision_response.startswith('realtime'):
                category = 'realtime' 
                processed_query = decision_response.replace('realtime', '').strip()
            elif decision_response.startswith('automation'):
                category = 'automation'
                processed_query = decision_response.replace('automation', '').strip()
            else:
                # Fallback classification based on keywords
                category = self._fallback_classification(query)
                processed_query = query
            
            return category, processed_query
            
        except Exception as e:
            print(f"Decision brain error: {e}")
            # Fallback to keyword-based classification
            return self._fallback_classification(query), query
    
    def _fallback_classification(self, query: str) -> str:
        """
        Fallback classification using keyword matching.
        """
        query_lower = query.lower()
        
        # Automation keywords
        automation_keywords = [
            'open', 'close', 'start', 'stop', 'launch', 'run', 'execute',
            'create', 'make', 'write', 'generate', 'send', 'email',
            'file', 'folder', 'document', 'notepad', 'calculator',
            'reminder', 'remind', 'timer', 'schedule', 'shutdown',
            'facebook', 'instagram', 'youtube', 'chrome', 'browser'
        ]
        
        # Realtime keywords  
        realtime_keywords = [
            'weather', 'news', 'current', 'latest', 'today', 'now',
            'time', 'date', 'temperature', 'stock', 'price',
            'who is', 'what is happening', 'recent', 'update'
        ]
        
        # Check for automation
        for keyword in automation_keywords:
            if keyword in query_lower:
                return 'automation'
        
        # Check for realtime
        for keyword in realtime_keywords:
            if keyword in query_lower:
                return 'realtime'
        
        # Default to general
        return 'general'
    
    def get_system_prompts(self) -> Dict[str, str]:
        """
        Get system prompts for different query types based on GitHub gist.
        """
        return {
            'general': f"""Hello, I am {self.username}, You are a very accurate and advanced AI chatbot named {self.assistant_name} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
""",
            
            'realtime': f"""Hello, I am {self.username}, You are a very accurate and advanced AI chatbot named {self.assistant_name} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***""",
            
            'automation': f"""Hello, I am {self.username}, You are {self.assistant_name}, an advanced AI assistant capable of performing system automation tasks.
*** Execute the requested automation task and provide clear feedback about the action taken. ***
*** Be specific about what was accomplished and any relevant details. ***
*** If a task cannot be completed, explain why and suggest alternatives. ***"""
        }

if __name__ == "__main__":
    # Test the decision brain
    brain = JarvisDecisionBrain()
    
    test_queries = [
        "Hello, how are you?",
        "What's the weather today?",
        "Open notepad",
        "Who is Elon Musk?",
        "Create a file called test.txt",
        "Tell me a joke",
        "What's the latest news?",
        "Close all windows"
    ]
    
    print("🧠 Testing JARVIS Decision Brain:")
    print("=" * 50)
    
    for query in test_queries:
        category, processed = brain.make_decision(query)
        print(f"Query: '{query}'")
        print(f"Decision: {category.upper()}")
        print(f"Processed: '{processed}'")
        print("-" * 30)
