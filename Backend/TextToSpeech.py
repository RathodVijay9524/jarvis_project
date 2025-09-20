"""
TextToSpeech.py
Advanced text-to-speech integration for JARVIS using edge-tts and fallback options.
"""

import os
import tempfile
import asyncio
import threading
from typing import Optional
import pygame

class JarvisTextToSpeech:
    def __init__(self, voice: str = "en-US-AriaNeural"):
        self.voice = voice
        self.rate = "+0%"
        self.volume = "+0%"
        pygame.mixer.init()
        
        # Available voices
        self.voices = {
            "aria": "en-US-AriaNeural",           # Female, friendly
            "guy": "en-US-GuyNeural",             # Male, casual
            "jenny": "en-US-JennyNeural",         # Female, professional
            "ryan": "en-US-RyanNeural",           # Male, professional
            "davis": "en-US-DavisNeural",         # Male, deep
            "jane": "en-US-JaneNeural",           # Female, mature
            "jason": "en-US-JasonNeural",         # Male, mature
            "tony": "en-US-TonyNeural",           # Male, authoritative (perfect for JARVIS!)
            "sara": "en-US-SaraNeural",           # Female, warm
            "nancy": "en-US-NancyNeural"          # Female, professional
        }
        
        # Default to Tony for JARVIS personality
        self.voice = self.voices.get("tony", voice)
    
    def speak(self, text: str, async_mode: bool = True) -> bool:
        """
        Convert text to speech and play it.
        
        Args:
            text: Text to speak
            async_mode: Whether to speak asynchronously (non-blocking)
        
        Returns:
            bool: Success status
        """
        if async_mode:
            thread = threading.Thread(target=self._speak_sync, args=(text,), daemon=True)
            thread.start()
            return True
        else:
            return self._speak_sync(text)
    
    def _speak_sync(self, text: str) -> bool:
        """
        Synchronous speech synthesis and playback.
        """
        try:
            # Try edge-tts first (best quality)
            if self._speak_with_edge_tts(text):
                return True
            
            # Fallback to pyttsx3
            return self._speak_with_pyttsx3(text)
            
        except Exception as e:
            print(f"TTS Error: {e}")
            # Ultimate fallback - just print
            print(f"JARVIS: {text}")
            return False
    
    def _speak_with_edge_tts(self, text: str) -> bool:
        """
        Use edge-tts for high-quality speech synthesis.
        """
        try:
            import edge_tts
            
            async def _generate_speech():
                communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, volume=self.volume)
                
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                    temp_path = temp_file.name
                    await communicate.save(temp_path)
                    return temp_path
            
            # Run async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            audio_file = loop.run_until_complete(_generate_speech())
            loop.close()
            
            # Play the audio file
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            # Cleanup
            os.unlink(audio_file)
            
            return True
            
        except Exception as e:
            print(f"Edge-TTS error: {e}")
            return False
    
    def _speak_with_pyttsx3(self, text: str) -> bool:
        """
        Fallback TTS using pyttsx3.
        """
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            
            # Configure voice properties
            voices = engine.getProperty('voices')
            if voices:
                # Try to find a male voice for JARVIS
                for voice in voices:
                    if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
            
            # Set rate and volume
            engine.setProperty('rate', 180)  # Speed
            engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
            
            engine.say(text)
            engine.runAndWait()
            
            return True
            
        except Exception as e:
            print(f"Pyttsx3 error: {e}")
            return False
    
    def set_voice(self, voice_name: str) -> bool:
        """
        Set the TTS voice.
        
        Args:
            voice_name: Voice name (key from self.voices or full voice string)
        
        Returns:
            bool: Success status
        """
        if voice_name in self.voices:
            self.voice = self.voices[voice_name]
            return True
        elif voice_name.endswith("Neural"):
            self.voice = voice_name
            return True
        else:
            print(f"Unknown voice: {voice_name}")
            print(f"Available voices: {list(self.voices.keys())}")
            return False
    
    def set_speech_rate(self, rate: str) -> bool:
        """
        Set speech rate.
        
        Args:
            rate: Rate string like "+10%", "-20%", "+0%"
        
        Returns:
            bool: Success status
        """
        try:
            self.rate = rate
            return True
        except:
            return False
    
    def set_volume(self, volume: str) -> bool:
        """
        Set speech volume.
        
        Args:
            volume: Volume string like "+10%", "-20%", "+0%"
        
        Returns:
            bool: Success status
        """
        try:
            self.volume = volume
            return True
        except:
            return False
    
    def get_available_voices(self) -> dict:
        """
        Get available voice options.
        
        Returns:
            dict: Available voices with descriptions
        """
        return {
            "tony": "Male, authoritative (perfect for JARVIS)",
            "aria": "Female, friendly",
            "guy": "Male, casual", 
            "jenny": "Female, professional",
            "ryan": "Male, professional",
            "davis": "Male, deep",
            "jane": "Female, mature",
            "jason": "Male, mature",
            "sara": "Female, warm",
            "nancy": "Female, professional"
        }
    
    def speak_with_emotion(self, text: str, emotion: str = "neutral") -> bool:
        """
        Speak with emotional context (experimental).
        
        Args:
            text: Text to speak
            emotion: Emotion type (happy, sad, excited, serious, etc.)
        
        Returns:
            bool: Success status
        """
        # Modify speech parameters based on emotion
        original_rate = self.rate
        original_volume = self.volume
        
        try:
            if emotion == "excited":
                self.rate = "+20%"
                self.volume = "+10%"
            elif emotion == "serious":
                self.rate = "-10%"
                self.volume = "+0%"
            elif emotion == "sad":
                self.rate = "-20%"
                self.volume = "-10%"
            elif emotion == "happy":
                self.rate = "+10%"
                self.volume = "+5%"
            
            result = self.speak(text, async_mode=False)
            
            # Restore original settings
            self.rate = original_rate
            self.volume = original_volume
            
            return result
            
        except Exception as e:
            # Restore original settings on error
            self.rate = original_rate
            self.volume = original_volume
            print(f"Emotional TTS error: {e}")
            return False

# Global TTS instance
_tts_instance = None

def get_tts_instance() -> JarvisTextToSpeech:
    """Get or create global TTS instance."""
    global _tts_instance
    if _tts_instance is None:
        _tts_instance = JarvisTextToSpeech()
    return _tts_instance

# Convenience functions for backward compatibility
def speak(text: str, async_mode: bool = True) -> bool:
    """
    Speak text using JARVIS TTS.
    
    Args:
        text: Text to speak
        async_mode: Whether to speak asynchronously
    
    Returns:
        bool: Success status
    """
    tts = get_tts_instance()
    return tts.speak(text, async_mode)

def speak_with_voice(text: str, voice: str = "tony") -> bool:
    """
    Speak text with specific voice.
    
    Args:
        text: Text to speak
        voice: Voice name
    
    Returns:
        bool: Success status
    """
    tts = get_tts_instance()
    tts.set_voice(voice)
    return tts.speak(text, async_mode=False)

def jarvis_greeting() -> bool:
    """Speak JARVIS greeting."""
    greetings = [
        "JARVIS systems online and ready to assist.",
        "Good day! JARVIS at your service.",
        "All systems operational. How may I help you today?",
        "JARVIS initialized and ready for commands."
    ]
    
    import random
    greeting = random.choice(greetings)
    return speak(greeting, async_mode=False)

if __name__ == "__main__":
    # Test TTS functionality
    tts = JarvisTextToSpeech()
    
    print("Testing JARVIS Text-to-Speech...")
    print("Available voices:", tts.get_available_voices())
    
    # Test basic speech
    print("\n1. Basic speech test")
    tts.speak("Hello, I am JARVIS, your personal AI assistant.", async_mode=False)
    
    # Test different voices
    print("\n2. Voice test")
    for voice in ["tony", "aria", "guy"]:
        tts.set_voice(voice)
        tts.speak(f"This is the {voice} voice speaking.", async_mode=False)
    
    # Test emotional speech
    print("\n3. Emotional speech test")
    tts.set_voice("tony")
    tts.speak_with_emotion("I'm excited to help you today!", "excited")
    tts.speak_with_emotion("This is a serious matter that requires attention.", "serious")
    
    print("TTS testing complete!")
