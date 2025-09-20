"""
AIPersonality.py
Enhanced AI personality system for smarter conversations and context understanding.
"""

import os
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

class JarvisAIPersonality:
    """
    Enhanced AI personality system with:
    - Context-aware conversations
    - Emotional intelligence
    - Learning from interactions
    - Personality traits and preferences
    - Conversation flow management
    - Smart response generation
    """
    
    def __init__(self, data_dir: str = "Data/personality"):
        self.data_dir = data_dir
        self.personality_file = os.path.join(data_dir, "personality.json")
        self.conversation_context_file = os.path.join(data_dir, "conversation_context.json")
        self.learning_file = os.path.join(data_dir, "learning_data.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Load personality data
        self.personality = self._load_personality()
        self.conversation_context = self._load_conversation_context()
        self.learning_data = self._load_learning_data()
        
        # Conversation state
        self.current_topic = None
        self.conversation_mood = "neutral"
        self.response_style = "professional"
        self.context_memory = []
        
        # Personality traits
        self.traits = {
            'helpfulness': 0.9,
            'friendliness': 0.8,
            'professionalism': 0.9,
            'curiosity': 0.7,
            'empathy': 0.8,
            'humor': 0.6,
            'patience': 0.9,
            'creativity': 0.7
        }
        
        # Learning patterns
        self.user_preferences = {}
        self.conversation_patterns = {}
        self.response_effectiveness = {}
    
    def _load_personality(self) -> Dict[str, Any]:
        """Load personality configuration."""
        try:
            if os.path.exists(self.personality_file):
                with open(self.personality_file, 'r') as f:
                    return json.load(f)
            return self._get_default_personality()
        except Exception as e:
            print(f"⚠️ Error loading personality: {e}")
            return self._get_default_personality()
    
    def _save_personality(self):
        """Save personality configuration."""
        try:
            with open(self.personality_file, 'w') as f:
                json.dump(self.personality, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving personality: {e}")
    
    def _load_conversation_context(self) -> List[Dict[str, Any]]:
        """Load conversation context."""
        try:
            if os.path.exists(self.conversation_context_file):
                with open(self.conversation_context_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"⚠️ Error loading conversation context: {e}")
            return []
    
    def _save_conversation_context(self):
        """Save conversation context."""
        try:
            # Keep only last 50 conversations
            if len(self.conversation_context) > 50:
                self.conversation_context = self.conversation_context[-50:]
            
            with open(self.conversation_context_file, 'w') as f:
                json.dump(self.conversation_context, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving conversation context: {e}")
    
    def _load_learning_data(self) -> Dict[str, Any]:
        """Load learning data."""
        try:
            if os.path.exists(self.learning_file):
                with open(self.learning_file, 'r') as f:
                    return json.load(f)
            return {
                'user_preferences': {},
                'conversation_patterns': {},
                'response_effectiveness': {},
                'topic_interest': {},
                'interaction_count': 0
            }
        except Exception as e:
            print(f"⚠️ Error loading learning data: {e}")
            return {
                'user_preferences': {},
                'conversation_patterns': {},
                'response_effectiveness': {},
                'topic_interest': {},
                'interaction_count': 0
            }
    
    def _save_learning_data(self):
        """Save learning data."""
        try:
            with open(self.learning_file, 'w') as f:
                json.dump(self.learning_data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving learning data: {e}")
    
    def _get_default_personality(self) -> Dict[str, Any]:
        """Get default personality configuration."""
        return {
            'name': 'JARVIS',
            'version': '2.0',
            'personality_type': 'Professional Assistant',
            'traits': {
                'helpfulness': 0.9,
                'friendliness': 0.8,
                'professionalism': 0.9,
                'curiosity': 0.7,
                'empathy': 0.8,
                'humor': 0.6,
                'patience': 0.9,
                'creativity': 0.7
            },
            'communication_style': {
                'formality': 'professional',
                'verbosity': 'concise',
                'tone': 'helpful',
                'response_length': 'medium'
            },
            'specializations': [
                'System Automation',
                'Information Retrieval',
                'Task Management',
                'Technical Support',
                'Productivity Enhancement'
            ],
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
    
    def analyze_user_input(self, user_input: str, user_name: str = None) -> Dict[str, Any]:
        """
        Analyze user input for context and intent.
        
        Args:
            user_input: User's input text
            user_name: User's name (if known)
            
        Returns:
            Analysis results with context and intent
        """
        try:
            analysis = {
                'timestamp': datetime.now().isoformat(),
                'user_input': user_input,
                'user_name': user_name,
                'sentiment': self._analyze_sentiment(user_input),
                'intent': self._analyze_intent(user_input),
                'topic': self._extract_topic(user_input),
                'urgency': self._analyze_urgency(user_input),
                'complexity': self._analyze_complexity(user_input),
                'context_clues': self._extract_context_clues(user_input),
                'emotions': self._detect_emotions(user_input)
            }
            
            # Update conversation context
            self._update_conversation_context(analysis)
            
            # Learn from interaction
            self._learn_from_interaction(analysis)
            
            return analysis
            
        except Exception as e:
            print(f"⚠️ Error analyzing user input: {e}")
            return {'error': str(e)}
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of user input."""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like', 'thanks', 'thank you']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'angry', 'frustrated', 'problem', 'error', 'broken']
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _analyze_intent(self, text: str) -> str:
        """Analyze user intent."""
        text_lower = text.lower()
        
        # Question intent
        if any(text_lower.startswith(q) for q in ['what', 'how', 'when', 'where', 'why', 'who', 'which']):
            return 'question'
        
        # Command intent
        if any(text_lower.startswith(c) for c in ['open', 'close', 'create', 'delete', 'send', 'find', 'search']):
            return 'command'
        
        # Request intent
        if any(text_lower.startswith(r) for r in ['please', 'can you', 'could you', 'would you', 'help me']):
            return 'request'
        
        # Greeting intent
        if any(text_lower.startswith(g) for g in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return 'greeting'
        
        # Complaint intent
        if any(word in text_lower for word in ['problem', 'issue', 'error', 'broken', 'not working', 'trouble']):
            return 'complaint'
        
        # Compliment intent
        if any(word in text_lower for word in ['good job', 'well done', 'excellent', 'great work', 'amazing']):
            return 'compliment'
        
        return 'general'
    
    def _extract_topic(self, text: str) -> str:
        """Extract main topic from user input."""
        # Common topic keywords
        topics = {
            'weather': ['weather', 'temperature', 'rain', 'sunny', 'forecast'],
            'technology': ['computer', 'software', 'programming', 'code', 'app', 'website'],
            'work': ['meeting', 'project', 'deadline', 'work', 'office', 'business'],
            'entertainment': ['movie', 'music', 'game', 'fun', 'entertainment'],
            'health': ['health', 'doctor', 'medicine', 'exercise', 'fitness'],
            'travel': ['travel', 'trip', 'vacation', 'flight', 'hotel'],
            'education': ['learn', 'study', 'school', 'university', 'course'],
            'finance': ['money', 'budget', 'investment', 'bank', 'finance']
        }
        
        text_lower = text.lower()
        
        for topic, keywords in topics.items():
            if any(keyword in text_lower for keyword in keywords):
                return topic
        
        return 'general'
    
    def _analyze_urgency(self, text: str) -> str:
        """Analyze urgency level of user input."""
        urgent_words = ['urgent', 'asap', 'immediately', 'now', 'quickly', 'emergency', 'critical']
        text_lower = text.lower()
        
        if any(word in text_lower for word in urgent_words):
            return 'high'
        elif '?' in text and len(text) < 50:
            return 'medium'
        else:
            return 'low'
    
    def _analyze_complexity(self, text: str) -> str:
        """Analyze complexity of user input."""
        word_count = len(text.split())
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        
        if word_count > 50 or sentence_count > 3:
            return 'complex'
        elif word_count > 20 or sentence_count > 1:
            return 'medium'
        else:
            return 'simple'
    
    def _extract_context_clues(self, text: str) -> List[str]:
        """Extract context clues from user input."""
        clues = []
        text_lower = text.lower()
        
        # Time references
        time_words = ['today', 'tomorrow', 'yesterday', 'now', 'later', 'soon']
        for word in time_words:
            if word in text_lower:
                clues.append(f"time:{word}")
        
        # Location references
        location_words = ['here', 'there', 'home', 'office', 'work']
        for word in location_words:
            if word in text_lower:
                clues.append(f"location:{word}")
        
        # Personal references
        personal_words = ['i', 'me', 'my', 'mine', 'we', 'us', 'our']
        for word in personal_words:
            if word in text_lower:
                clues.append(f"personal:{word}")
        
        return clues
    
    def _detect_emotions(self, text: str) -> List[str]:
        """Detect emotions in user input."""
        emotions = []
        text_lower = text.lower()
        
        emotion_words = {
            'happy': ['happy', 'joy', 'excited', 'pleased', 'delighted'],
            'sad': ['sad', 'depressed', 'upset', 'disappointed', 'down'],
            'angry': ['angry', 'mad', 'furious', 'annoyed', 'irritated'],
            'frustrated': ['frustrated', 'stressed', 'overwhelmed', 'tired'],
            'confused': ['confused', 'lost', 'unclear', 'don\'t understand'],
            'grateful': ['thankful', 'grateful', 'appreciate', 'thanks']
        }
        
        for emotion, words in emotion_words.items():
            if any(word in text_lower for word in words):
                emotions.append(emotion)
        
        return emotions
    
    def _update_conversation_context(self, analysis: Dict[str, Any]):
        """Update conversation context with new analysis."""
        self.conversation_context.append(analysis)
        self.current_topic = analysis.get('topic', self.current_topic)
        
        # Update conversation mood based on sentiment and emotions
        sentiment = analysis.get('sentiment', 'neutral')
        emotions = analysis.get('emotions', [])
        
        if sentiment == 'positive' or 'happy' in emotions:
            self.conversation_mood = 'positive'
        elif sentiment == 'negative' or any(e in emotions for e in ['angry', 'frustrated', 'sad']):
            self.conversation_mood = 'concerned'
        elif 'confused' in emotions:
            self.conversation_mood = 'helpful'
        else:
            self.conversation_mood = 'neutral'
    
    def _learn_from_interaction(self, analysis: Dict[str, Any]):
        """Learn from user interaction patterns."""
        self.learning_data['interaction_count'] += 1
        
        # Track topic interests
        topic = analysis.get('topic', 'general')
        if topic not in self.learning_data['topic_interest']:
            self.learning_data['topic_interest'][topic] = 0
        self.learning_data['topic_interest'][topic] += 1
        
        # Track conversation patterns
        intent = analysis.get('intent', 'general')
        if intent not in self.learning_data['conversation_patterns']:
            self.learning_data['conversation_patterns'][intent] = 0
        self.learning_data['conversation_patterns'][intent] += 1
        
        # Save learning data periodically
        if self.learning_data['interaction_count'] % 10 == 0:
            self._save_learning_data()
    
    def generate_contextual_response(self, base_response: str, analysis: Dict[str, Any]) -> str:
        """
        Enhance base response with contextual personality.
        
        Args:
            base_response: Base AI response
            analysis: User input analysis
            
        Returns:
            Enhanced response with personality
        """
        try:
            # Get response style based on context
            response_style = self._determine_response_style(analysis)
            
            # Add contextual elements
            enhanced_response = self._add_contextual_elements(base_response, analysis, response_style)
            
            # Add personality traits
            enhanced_response = self._add_personality_traits(enhanced_response, analysis)
            
            # Add emotional intelligence
            enhanced_response = self._add_emotional_intelligence(enhanced_response, analysis)
            
            return enhanced_response
            
        except Exception as e:
            print(f"⚠️ Error generating contextual response: {e}")
            return base_response
    
    def _determine_response_style(self, analysis: Dict[str, Any]) -> str:
        """Determine appropriate response style based on context."""
        intent = analysis.get('intent', 'general')
        sentiment = analysis.get('sentiment', 'neutral')
        urgency = analysis.get('urgency', 'low')
        
        if urgency == 'high':
            return 'direct'
        elif intent == 'complaint':
            return 'empathetic'
        elif intent == 'compliment':
            return 'grateful'
        elif sentiment == 'positive':
            return 'friendly'
        elif intent == 'question':
            return 'explanatory'
        else:
            return 'professional'
    
    def _add_contextual_elements(self, response: str, analysis: Dict[str, Any], style: str) -> str:
        """Add contextual elements to response."""
        user_name = analysis.get('user_name')
        topic = analysis.get('topic', 'general')
        emotions = analysis.get('emotions', [])
        
        # Add personalization
        if user_name and user_name != 'User':
            if not response.startswith(f"{user_name}"):
                response = f"{user_name}, {response.lower()}"
        
        # Add topic-specific context
        if topic != 'general':
            topic_contexts = {
                'weather': "I hope this weather information helps with your plans.",
                'technology': "Let me help you with that technical task.",
                'work': "I understand work can be demanding.",
                'health': "I hope this information contributes to your wellbeing."
            }
            
            if topic in topic_contexts and style in ['friendly', 'empathetic']:
                response += f" {topic_contexts[topic]}"
        
        return response
    
    def _add_personality_traits(self, response: str, analysis: Dict[str, Any]) -> str:
        """Add personality traits to response."""
        intent = analysis.get('intent', 'general')
        complexity = analysis.get('complexity', 'simple')
        
        # Add helpfulness
        if self.traits['helpfulness'] > 0.8 and intent in ['request', 'question']:
            if not any(word in response.lower() for word in ['help', 'assist', 'support']):
                response += " I'm here to help with anything else you need."
        
        # Add friendliness
        if self.traits['friendliness'] > 0.7 and intent == 'greeting':
            friendly_additions = [
                "Great to see you!",
                "I'm excited to assist you today!",
                "How can I make your day better?"
            ]
            if not any(word in response.lower() for word in ['hello', 'hi', 'hey']):
                response = f"Hello! {response}"
        
        # Add curiosity
        if self.traits['curiosity'] > 0.7 and complexity == 'simple':
            if intent == 'question' and '?' not in response:
                response += " Would you like me to elaborate on any particular aspect?"
        
        return response
    
    def _add_emotional_intelligence(self, response: str, analysis: Dict[str, Any]) -> str:
        """Add emotional intelligence to response."""
        emotions = analysis.get('emotions', [])
        sentiment = analysis.get('sentiment', 'neutral')
        
        # Respond to detected emotions
        if 'frustrated' in emotions:
            response = f"I understand this might be frustrating. {response} Let me know if you need any clarification."
        elif 'confused' in emotions:
            response = f"I can see this might be confusing. {response} Feel free to ask for more details."
        elif 'grateful' in emotions:
            response = f"You're very welcome! {response}"
        elif sentiment == 'negative':
            response = f"I'm sorry to hear about the issue. {response} I'm here to help resolve this."
        
        return response
    
    def get_conversation_summary(self) -> str:
        """Get summary of recent conversation context."""
        if not self.conversation_context:
            return "No recent conversation context available."
        
        recent_contexts = self.conversation_context[-5:]  # Last 5 interactions
        
        topics = [ctx.get('topic', 'general') for ctx in recent_contexts]
        intents = [ctx.get('intent', 'general') for ctx in recent_contexts]
        sentiments = [ctx.get('sentiment', 'neutral') for ctx in recent_contexts]
        
        summary = f"📊 **Recent Conversation Context**\n\n"
        summary += f"🔄 **Current Topic:** {self.current_topic or 'General'}\n"
        summary += f"😊 **Conversation Mood:** {self.conversation_mood}\n"
        summary += f"📝 **Recent Topics:** {', '.join(set(topics))}\n"
        summary += f"🎯 **Recent Intents:** {', '.join(set(intents))}\n"
        summary += f"💭 **Sentiment Trend:** {max(set(sentiments), key=sentiments.count)}\n"
        summary += f"📈 **Total Interactions:** {self.learning_data['interaction_count']}\n"
        
        return summary
    
    def get_personality_profile(self) -> str:
        """Get current personality profile."""
        profile = f"🤖 **JARVIS Personality Profile**\n\n"
        profile += f"👤 **Name:** {self.personality['name']}\n"
        profile += f"🎭 **Type:** {self.personality['personality_type']}\n"
        profile += f"📅 **Created:** {self.personality['created_at']}\n"
        profile += f"🔄 **Last Updated:** {self.personality['last_updated']}\n\n"
        
        profile += f"🎯 **Personality Traits:**\n"
        for trait, value in self.traits.items():
            percentage = int(value * 100)
            bar = "█" * (percentage // 10) + "░" * (10 - percentage // 10)
            profile += f"   • {trait.title()}: {bar} {percentage}%\n"
        
        profile += f"\n💬 **Communication Style:**\n"
        style = self.personality['communication_style']
        profile += f"   • Formality: {style['formality']}\n"
        profile += f"   • Verbosity: {style['verbosity']}\n"
        profile += f"   • Tone: {style['tone']}\n"
        profile += f"   • Response Length: {style['response_length']}\n"
        
        profile += f"\n🔧 **Specializations:**\n"
        for spec in self.personality['specializations']:
            profile += f"   • {spec}\n"
        
        return profile
    
    def update_personality_trait(self, trait: str, value: float) -> str:
        """Update a personality trait."""
        if trait not in self.traits:
            available_traits = ', '.join(self.traits.keys())
            return f"❌ Unknown trait '{trait}'. Available traits: {available_traits}"
        
        if not 0.0 <= value <= 1.0:
            return "❌ Trait value must be between 0.0 and 1.0"
        
        old_value = self.traits[trait]
        self.traits[trait] = value
        self.personality['traits'] = self.traits
        self.personality['last_updated'] = datetime.now().isoformat()
        
        self._save_personality()
        
        return f"✅ Updated {trait} from {old_value:.2f} to {value:.2f}"
    
    def get_learning_insights(self) -> str:
        """Get insights from learning data."""
        insights = f"🧠 **Learning Insights**\n\n"
        
        # Topic interests
        if self.learning_data['topic_interest']:
            insights += f"📊 **Most Discussed Topics:**\n"
            sorted_topics = sorted(
                self.learning_data['topic_interest'].items(),
                key=lambda x: x[1], reverse=True
            )[:5]
            
            for topic, count in sorted_topics:
                insights += f"   • {topic.title()}: {count} discussions\n"
        
        # Conversation patterns
        if self.learning_data['conversation_patterns']:
            insights += f"\n🎯 **Interaction Patterns:**\n"
            sorted_patterns = sorted(
                self.learning_data['conversation_patterns'].items(),
                key=lambda x: x[1], reverse=True
            )[:5]
            
            for pattern, count in sorted_patterns:
                insights += f"   • {pattern.title()}: {count} times\n"
        
        insights += f"\n📈 **Total Interactions:** {self.learning_data['interaction_count']}\n"
        
        return insights
