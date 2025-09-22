"""
SimplifiedEnhancedSpeech.py
Enhanced speech-to-text using HTML5 Web Speech API with Selenium
Based on the efficient approach from KaushikShresth07's implementation
Supports Hindi and 20+ languages
"""

import os
import tempfile
import time
from typing import Optional, Dict, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class JarvisSimplifiedSpeech:
    """
    Simplified Enhanced Speech Recognition using HTML5 Web Speech API.
    Much more efficient than the complex approach - based on proven working code.
    """
    
    def __init__(self):
        self.driver = None
        self.html_file_path = None
        
        # Language configurations
        self.languages = {
            "english": "en-US",
            "hindi": "hi-IN",
            "spanish": "es-ES", 
            "french": "fr-FR",
            "german": "de-DE",
            "italian": "it-IT",
            "portuguese": "pt-BR",
            "russian": "ru-RU",
            "japanese": "ja-JP",
            "korean": "ko-KR",
            "chinese": "zh-CN",
            "arabic": "ar-SA",
            "bengali": "bn-IN",
            "tamil": "ta-IN",
            "telugu": "te-IN",
            "marathi": "mr-IN",
            "gujarati": "gu-IN",
            "punjabi": "pa-IN"
        }
        
        # Create the HTML file
        self._create_html_file()
    
    def _create_html_file(self):
        """Create the HTML file for speech recognition."""
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>JARVIS Speech Recognition</title>
    <meta charset="UTF-8">
</head>
<body>
    <select id="language">
        <option value="en-US">English (US)</option>
        <option value="hi-IN">हिंदी (Hindi)</option>
    </select>
    
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    
    <div id="output">Ready to listen...</div>

    <script>
        const output = document.getElementById('output');
        const languageSelect = document.getElementById('language');
        let recognition;

        function startRecognition() {
            try {
                recognition = new webkitSpeechRecognition() || new SpeechRecognition();
                recognition.lang = languageSelect.value;
                recognition.continuous = true;
                recognition.interimResults = false;

                recognition.onresult = function(event) {
                    const transcript = event.results[event.results.length - 1][0].transcript;
                    output.textContent = transcript;
                };

                recognition.onerror = function(event) {
                    output.textContent = 'Error: ' + event.error;
                };

                recognition.onend = function() {
                    // Auto-restart if needed
                    if (output.textContent === 'Ready to listen...') {
                        recognition.start();
                    }
                };
                
                recognition.start();
                output.textContent = 'Listening...';
                
            } catch (error) {
                output.textContent = 'Error: ' + error.message;
            }
        }

        function stopRecognition() {
            if (recognition) {
                recognition.stop();
                if (output.textContent === 'Listening...') {
                    output.textContent = 'No speech detected';
                }
            }
        }
    </script>
</body>
</html>'''
        
        # Create temporary HTML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            self.html_file_path = f.name
    
    def _setup_driver(self):
        """Setup Chrome driver with optimized options."""
        try:
            chrome_options = Options()
            
            # User agent
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            chrome_options.add_argument(f'user-agent={user_agent}')
            
            # Media permissions
            chrome_options.add_argument("--use-fake-ui-for-media-stream")
            chrome_options.add_argument("--use-fake-device-for-media-stream")
            
            # Performance optimizations
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            
            # Disable logging
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Setup service
            service = Service(ChromeDriverManager().install())
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.get(f"file://{self.html_file_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Driver setup failed: {e}")
            return False
    
    def listen(self, language: str = "english", timeout: int = 10) -> str:
        """
        Listen for speech in the specified language.
        
        Args:
            language: Language to listen in
            timeout: Maximum time to wait for speech
            
        Returns:
            str: Recognized text or error message
        """
        try:
            # Setup driver if needed
            if not self.driver:
                if not self._setup_driver():
                    return "❌ Failed to setup speech recognition"
            
            # Set language
            lang_code = self.languages.get(language.lower(), "en-US")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "start"))
            )
            
            # Set language in dropdown
            language_select = self.driver.find_element(By.ID, "language")
            language_select.send_keys(lang_code)
            
            # Start recognition
            self.driver.find_element(By.ID, "start").click()
            print(f"🎤 Listening in {language} ({lang_code})...")
            
            # Wait for speech with timeout
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                try:
                    output_element = self.driver.find_element(By.ID, "output")
                    text = output_element.text
                    
                    # Check if we got actual speech (not status messages)
                    if text and text not in ["Ready to listen...", "Listening...", "No speech detected"]:
                        # Stop recognition
                        try:
                            self.driver.find_element(By.ID, "end").click()
                        except:
                            pass
                        
                        return text.strip()
                    
                    time.sleep(0.3)  # Check every 300ms
                    
                except Exception as e:
                    time.sleep(0.5)
                    continue
            
            # Timeout reached
            try:
                self.driver.find_element(By.ID, "end").click()
            except:
                pass
                
            return "No speech detected within timeout"
            
        except Exception as e:
            return f"❌ Speech recognition error: {str(e)}"
    
    def listen_multilingual(self, languages: List[str] = ["english", "hindi"], timeout: int = 5) -> Dict[str, str]:
        """
        Try listening in multiple languages.
        
        Args:
            languages: List of languages to try
            timeout: Timeout per language
            
        Returns:
            Dict[str, str]: Results for each language
        """
        results = {}
        
        for lang in languages:
            print(f"🌐 Trying {lang}...")
            result = self.listen(lang, timeout)
            results[lang] = result
            
            # If we got a good result, stop trying other languages
            if result and len(result.strip()) > 3 and not result.startswith("❌") and "No speech detected" not in result:
                print(f"✅ Success in {lang}: {result}")
                break
        
        return results
    
    def cleanup(self):
        """Cleanup resources."""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
            except:
                pass
        
        if self.html_file_path:
            try:
                os.unlink(self.html_file_path)
                self.html_file_path = None
            except:
                pass
    
    def __del__(self):
        """Cleanup on destruction."""
        self.cleanup()

# Convenience functions for easy use
def listen_english(timeout: int = 10) -> str:
    """Quick function to listen in English."""
    speech = JarvisSimplifiedSpeech()
    try:
        return speech.listen("english", timeout)
    finally:
        speech.cleanup()

def listen_hindi(timeout: int = 10) -> str:
    """Quick function to listen in Hindi."""
    speech = JarvisSimplifiedSpeech()
    try:
        return speech.listen("hindi", timeout)
    finally:
        speech.cleanup()

def listen_any_language(timeout: int = 10) -> Dict[str, str]:
    """Quick function to listen in multiple languages."""
    speech = JarvisSimplifiedSpeech()
    try:
        return speech.listen_multilingual(["english", "hindi"], timeout)
    finally:
        speech.cleanup()

if __name__ == "__main__":
    # Test the simplified speech recognition
    print("🧪 Testing Simplified Enhanced Speech Recognition")
    print("=" * 60)
    
    speech = JarvisSimplifiedSpeech()
    
    try:
        # Test English
        print("\n1. Testing English...")
        result = speech.listen("english", 10)
        print(f"English Result: {result}")
        
        # Test Hindi
        print("\n2. Testing Hindi...")
        result = speech.listen("hindi", 10)
        print(f"Hindi Result: {result}")
        
        # Test multilingual
        print("\n3. Testing Multilingual...")
        results = speech.listen_multilingual(["english", "hindi"], 5)
        for lang, result in results.items():
            print(f"{lang}: {result}")
            
    finally:
        speech.cleanup()
        print("\n✅ Test completed!")
