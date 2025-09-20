"""
SpeechToText.py
Advanced speech-to-text integration for JARVIS using multiple backends.
"""

import os
import json
import tempfile
import threading
import time
from typing import Optional, Callable
import pyaudio
import wave
import keyboard

class JarvisSpeechToText:
    def __init__(self):
        self.is_listening = False
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 1024
        self.record_seconds = 5
        self.audio = pyaudio.PyAudio()
        
    def transcribe_file(self, audio_path: str) -> str:
        """
        Transcribe audio file to text using available speech recognition services.
        """
        try:
            # Try Groq Whisper API first (if available)
            result = self._transcribe_with_groq(audio_path)
            if result:
                return result
            
            # Fallback to local speech recognition
            return self._transcribe_with_speech_recognition(audio_path)
            
        except Exception as e:
            return f"Transcription error: {str(e)}"
    
    def _transcribe_with_groq(self, audio_path: str) -> Optional[str]:
        """
        Use Groq's Whisper API for transcription.
        """
        try:
            import groq
            from dotenv import load_dotenv
            
            load_dotenv()
            groq_api_key = os.getenv("GROQ_API_KEY")
            
            if not groq_api_key:
                return None
            
            client = groq.Groq(api_key=groq_api_key)
            
            with open(audio_path, "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=(audio_path, file.read()),
                    model="whisper-large-v3",
                    response_format="text"
                )
            
            return transcription
            
        except Exception as e:
            print(f"Groq transcription error: {e}")
            return None
    
    def _transcribe_with_speech_recognition(self, audio_path: str) -> str:
        """
        Fallback transcription using speech_recognition library.
        """
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)
            
            # Try multiple recognition services
            try:
                # Google Speech Recognition (free)
                return recognizer.recognize_google(audio_data)
            except:
                try:
                    # Sphinx (offline)
                    return recognizer.recognize_sphinx(audio_data)
                except:
                    return "Could not understand audio"
                    
        except Exception as e:
            return f"Speech recognition error: {str(e)}"
    
    def listen_once(self, duration: int = 5) -> str:
        """
        Record audio for specified duration and transcribe.
        """
        try:
            print(f"🎤 Listening for {duration} seconds...")
            
            # Record audio
            frames = []
            stream = self.audio.open(
                format=self.audio_format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            for _ in range(0, int(self.rate / self.chunk * duration)):
                data = stream.read(self.chunk)
                frames.append(data)
            
            stream.stop_stream()
            stream.close()
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name
                
                wf = wave.open(temp_path, 'wb')
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.audio_format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(frames))
                wf.close()
            
            # Transcribe
            result = self.transcribe_file(temp_path)
            
            # Cleanup
            os.unlink(temp_path)
            
            return result
            
        except Exception as e:
            return f"Recording error: {str(e)}"
    
    def listen_continuous(self, callback: Callable[[str], None], 
                         wake_word: str = "jarvis", 
                         stop_key: str = "esc"):
        """
        Continuously listen for wake word and transcribe speech.
        """
        print(f"🎤 Continuous listening started. Say '{wake_word}' to activate.")
        print(f"Press '{stop_key}' to stop listening.")
        
        self.is_listening = True
        
        def listen_thread():
            while self.is_listening:
                try:
                    # Listen for short segments
                    text = self.listen_once(duration=3)
                    
                    if text and wake_word.lower() in text.lower():
                        print("🔊 Wake word detected! Listening for command...")
                        
                        # Listen for longer command
                        command = self.listen_once(duration=8)
                        
                        if command and len(command.strip()) > 0:
                            print(f"📝 Heard: {command}")
                            callback(command)
                    
                    time.sleep(0.5)  # Brief pause between listening cycles
                    
                except Exception as e:
                    print(f"Listening error: {e}")
                    time.sleep(1)
        
        # Start listening in background thread
        thread = threading.Thread(target=listen_thread, daemon=True)
        thread.start()
        
        # Monitor for stop key
        try:
            keyboard.wait(stop_key)
        except:
            pass
        
        self.stop_listening()
    
    def stop_listening(self):
        """Stop continuous listening."""
        self.is_listening = False
        print("🔇 Stopped listening.")
    
    def __del__(self):
        """Cleanup audio resources."""
        try:
            if hasattr(self, 'audio'):
                self.audio.terminate()
        except:
            pass

# Convenience functions for backward compatibility
def transcribe(audio_path: str) -> str:
    """Transcribe audio file to text."""
    stt = JarvisSpeechToText()
    return stt.transcribe_file(audio_path)

def listen_for_command(duration: int = 5) -> str:
    """Listen for voice command."""
    stt = JarvisSpeechToText()
    return stt.listen_once(duration)

def start_voice_assistant(callback: Callable[[str], None]):
    """Start voice-activated assistant."""
    stt = JarvisSpeechToText()
    stt.listen_continuous(callback)

if __name__ == "__main__":
    def test_callback(text: str):
        print(f"Command received: {text}")
    
    # Test speech recognition
    stt = JarvisSpeechToText()
    
    print("Testing speech recognition...")
    print("1. Single recording test")
    result = stt.listen_once(5)
    print(f"Result: {result}")
    
    print("\n2. Continuous listening test")
    print("Say 'jarvis' followed by a command")
    stt.listen_continuous(test_callback)
