"""
TranslationService.py
Real-time translation services with multiple language support.
"""

import requests
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

class JarvisTranslationService:
    """
    Translation service using multiple free APIs:
    - Google Translate (free tier)
    - Microsoft Translator (free tier)
    - LibreTranslate (open source)
    - Fallback translation methods
    """
    
    def __init__(self):
        self.translation_cache = {}
        self.cache_duration = 3600  # 1 hour
        
        # Supported languages with their codes
        self.supported_languages = {
            'english': 'en', 'spanish': 'es', 'french': 'fr', 'german': 'de',
            'italian': 'it', 'portuguese': 'pt', 'russian': 'ru', 'chinese': 'zh',
            'japanese': 'ja', 'korean': 'ko', 'arabic': 'ar', 'hindi': 'hi',
            'dutch': 'nl', 'swedish': 'sv', 'norwegian': 'no', 'danish': 'da',
            'finnish': 'fi', 'polish': 'pl', 'czech': 'cs', 'hungarian': 'hu',
            'romanian': 'ro', 'bulgarian': 'bg', 'croatian': 'hr', 'slovak': 'sk',
            'slovenian': 'sl', 'estonian': 'et', 'latvian': 'lv', 'lithuanian': 'lt',
            'greek': 'el', 'turkish': 'tr', 'hebrew': 'he', 'thai': 'th',
            'vietnamese': 'vi', 'indonesian': 'id', 'malay': 'ms', 'tagalog': 'tl',
            'swahili': 'sw', 'afrikaans': 'af', 'albanian': 'sq', 'azerbaijani': 'az',
            'belarusian': 'be', 'bosnian': 'bs', 'catalan': 'ca', 'cyrillic': 'cy',
            'esperanto': 'eo', 'basque': 'eu', 'galician': 'gl', 'georgian': 'ka',
            'icelandic': 'is', 'irish': 'ga', 'macedonian': 'mk', 'maltese': 'mt',
            'moldovan': 'mo', 'montenegrin': 'me', 'persian': 'fa', 'serbian': 'sr',
            'tajik': 'tg', 'turkmen': 'tk', 'ukrainian': 'uk', 'uzbek': 'uz',
            'welsh': 'cy', 'yiddish': 'yi'
        }
        
        # Language flags for display
        self.language_flags = {
            'en': '🇺🇸', 'es': '🇪🇸', 'fr': '🇫🇷', 'de': '🇩🇪',
            'it': '🇮🇹', 'pt': '🇵🇹', 'ru': '🇷🇺', 'zh': '🇨🇳',
            'ja': '🇯🇵', 'ko': '🇰🇷', 'ar': '🇸🇦', 'hi': '🇮🇳',
            'nl': '🇳🇱', 'sv': '🇸🇪', 'no': '🇳🇴', 'da': '🇩🇰',
            'fi': '🇫🇮', 'pl': '🇵🇱', 'cs': '🇨🇿', 'hu': '🇭🇺',
            'ro': '🇷🇴', 'bg': '🇧🇬', 'hr': '🇭🇷', 'sk': '🇸🇰',
            'sl': '🇸🇮', 'et': '🇪🇪', 'lv': '🇱🇻', 'lt': '🇱🇹',
            'el': '🇬🇷', 'tr': '🇹🇷', 'he': '🇮🇱', 'th': '🇹🇭',
            'vi': '🇻🇳', 'id': '🇮🇩', 'ms': '🇲🇾', 'tl': '🇵🇭',
            'sw': '🇹🇿', 'af': '🇿🇦', 'sq': '🇦🇱', 'az': '🇦🇿',
            'be': '🇧🇾', 'bs': '🇧🇦', 'ca': '🇪🇸', 'cy': '🇬🇧',
            'eo': '🌍', 'eu': '🇪🇸', 'gl': '🇪🇸', 'ka': '🇬🇪',
            'is': '🇮🇸', 'ga': '🇮🇪', 'mk': '🇲🇰', 'mt': '🇲🇹',
            'mo': '🇲🇩', 'me': '🇲🇪', 'fa': '🇮🇷', 'sr': '🇷🇸',
            'tg': '🇹🇯', 'tk': '🇹🇲', 'uk': '🇺🇦', 'uz': '🇺🇿',
            'yi': '🇮🇱'
        }
        
        # Translation services
        self.translation_services = [
            'libre_translate',
            'google_translate',
            'microsoft_translate'
        ]
    
    def translate_text(self, text: str, target_language: str, source_language: str = 'auto') -> str:
        """
        Translate text from source language to target language.
        """
        try:
            # Validate and normalize languages
            source_lang = self._normalize_language(source_language)
            target_lang = self._normalize_language(target_language)
            
            if not target_lang:
                return f"❌ Unknown target language: {target_language}. Use 'list languages' to see available languages."
            
            # Check cache
            cache_key = f"translate:{hash(text)}:{source_lang}:{target_lang}"
            if cache_key in self.translation_cache:
                cached_time, result = self.translation_cache[cache_key]
                if time.time() - cached_time < self.cache_duration:
                    return self._format_translation_response(text, result, source_lang, target_lang)
            
            # Try multiple translation services
            translation_result = None
            
            for service in self.translation_services:
                try:
                    if service == 'libre_translate':
                        translation_result = self._translate_libre_translate(text, source_lang, target_lang)
                    elif service == 'google_translate':
                        translation_result = self._translate_google(text, source_lang, target_lang)
                    elif service == 'microsoft_translate':
                        translation_result = self._translate_microsoft(text, source_lang, target_lang)
                    
                    if translation_result:
                        break
                        
                except Exception as e:
                    print(f"⚠️ Translation service {service} failed: {e}")
                    continue
            
            if not translation_result:
                translation_result = self._get_fallback_translation(text, source_lang, target_lang)
            
            # Cache the result
            self.translation_cache[cache_key] = (time.time(), translation_result)
            
            return self._format_translation_response(text, translation_result, source_lang, target_lang)
            
        except Exception as e:
            return f"❌ Translation error: {str(e)}"
    
    def _translate_libre_translate(self, text: str, source_lang: str, target_lang: str) -> Optional[Dict[str, Any]]:
        """Translate using LibreTranslate (free, open source)."""
        try:
            # LibreTranslate public instances
            libre_instances = [
                'https://libretranslate.de/translate',
                'https://translate.argosopentech.com/translate',
                'https://libretranslate.com/translate'
            ]
            
            for instance_url in libre_instances:
                try:
                    payload = {
                        'q': text,
                        'source': source_lang,
                        'target': target_lang,
                        'format': 'text'
                    }
                    
                    response = requests.post(instance_url, data=payload, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if 'translatedText' in data:
                            return {
                                'translated_text': data['translatedText'],
                                'source_language': data.get('detectedLanguage', {}).get('language', source_lang),
                                'confidence': data.get('detectedLanguage', {}).get('confidence', 0),
                                'service': 'LibreTranslate'
                            }
                except:
                    continue
            
            return None
            
        except Exception as e:
            print(f"⚠️ LibreTranslate failed: {e}")
            return None
    
    def _translate_google(self, text: str, source_lang: str, target_lang: str) -> Optional[Dict[str, Any]]:
        """Translate using Google Translate (web scraping)."""
        try:
            # Google Translate URL
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': source_lang,
                'tl': target_lang,
                'dt': 't',
                'q': text
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data and len(data) > 0 and data[0]:
                translated_text = ''.join([item[0] for item in data[0] if item[0]])
                detected_lang = data[2] if len(data) > 2 else source_lang
                
                return {
                    'translated_text': translated_text,
                    'source_language': detected_lang,
                    'confidence': 0.95,  # Google is generally reliable
                    'service': 'Google Translate'
                }
            
            return None
            
        except Exception as e:
            print(f"⚠️ Google Translate failed: {e}")
            return None
    
    def _translate_microsoft(self, text: str, source_lang: str, target_lang: str) -> Optional[Dict[str, Any]]:
        """Translate using Microsoft Translator (would require API key)."""
        try:
            # Microsoft Translator would require an API key
            # This is a placeholder for when an API key is available
            return None
            
        except Exception as e:
            print(f"⚠️ Microsoft Translator failed: {e}")
            return None
    
    def _get_fallback_translation(self, text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """Fallback translation when all services fail."""
        return {
            'translated_text': f"[Translation unavailable] {text}",
            'source_language': source_lang,
            'confidence': 0.0,
            'service': 'Fallback',
            'note': 'Translation service temporarily unavailable'
        }
    
    def _normalize_language(self, language: str) -> str:
        """Normalize language input to language code."""
        if not language or language.lower() == 'auto':
            return 'auto'
        
        language_lower = language.lower().strip()
        
        # Direct code match
        if language_lower in self.supported_languages.values():
            return language_lower
        
        # Name to code mapping
        if language_lower in self.supported_languages:
            return self.supported_languages[language_lower]
        
        # Partial name matching
        for name, code in self.supported_languages.items():
            if language_lower in name or name in language_lower:
                return code
        
        return ''
    
    def _format_translation_response(self, original_text: str, translation_result: Dict[str, Any], source_lang: str, target_lang: str) -> str:
        """Format translation result into a readable response."""
        translated_text = translation_result.get('translated_text', 'Translation failed')
        detected_source = translation_result.get('source_language', source_lang)
        confidence = translation_result.get('confidence', 0)
        service = translation_result.get('service', 'Unknown')
        
        # Get language flags
        source_flag = self.language_flags.get(detected_source, '🌍')
        target_flag = self.language_flags.get(target_lang, '🌍')
        
        response = f"🌍 **Translation**\n\n"
        
        response += f"{source_flag} **Original ({detected_source}):**\n"
        response += f"   {original_text}\n\n"
        
        response += f"{target_flag} **Translated ({target_lang}):**\n"
        response += f"   {translated_text}\n\n"
        
        if confidence > 0:
            confidence_percent = confidence * 100
            response += f"📊 **Confidence:** {confidence_percent:.1f}%\n"
        
        response += f"🔧 **Service:** {service}\n"
        response += f"🕒 **Translated:** {datetime.now().strftime('%H:%M:%S')}\n"
        
        if translation_result.get('note'):
            response += f"\n⚠️ **Note:** {translation_result['note']}\n"
        
        return response
    
    def detect_language(self, text: str) -> str:
        """Detect the language of the input text."""
        try:
            # Use translation service to detect language
            result = self.translate_text(text, 'en', 'auto')
            
            # Extract detected language from result
            if 'Original (' in result:
                import re
                match = re.search(r'Original \(([^)]+)\):', result)
                if match:
                    detected_lang = match.group(1)
                    lang_name = self._get_language_name(detected_lang)
                    lang_flag = self.language_flags.get(detected_lang, '🌍')
                    
                    return f"{lang_flag} **Detected Language:** {lang_name} ({detected_lang})\n\n**Text:** {text}"
            
            return f"❌ Unable to detect language for: {text}"
            
        except Exception as e:
            return f"❌ Language detection error: {str(e)}"
    
    def _get_language_name(self, lang_code: str) -> str:
        """Get language name from language code."""
        for name, code in self.supported_languages.items():
            if code == lang_code:
                return name.title()
        return lang_code.upper()
    
    def get_supported_languages(self) -> str:
        """Get list of supported languages."""
        response = "🌍 **Supported Languages**\n\n"
        
        # Group languages by region
        regions = {
            'Europe': ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'nl', 'sv', 'no', 'da', 'fi', 'pl', 'cs', 'hu', 'ro', 'bg', 'hr', 'sk', 'sl', 'et', 'lv', 'lt', 'el', 'tr', 'cy', 'eu', 'gl', 'is', 'ga', 'mk', 'mt', 'mo', 'me', 'sr', 'yi'],
            'Asia': ['zh', 'ja', 'ko', 'hi', 'th', 'vi', 'id', 'ms', 'tl', 'az', 'ka', 'tg', 'tk', 'uz'],
            'Middle East & Africa': ['ar', 'he', 'sw', 'af', 'sq', 'be', 'bs', 'fa', 'uk'],
            'Americas': ['en', 'es', 'pt', 'fr']  # These overlap with Europe
        }
        
        for region, lang_codes in regions.items():
            response += f"**{region}:**\n"
            for code in lang_codes:
                if code in self.language_flags:
                    flag = self.language_flags[code]
                    name = self._get_language_name(code)
                    response += f"   {flag} {name} ({code})\n"
            response += "\n"
        
        response += "💡 **Usage Examples:**\n"
        response += "   • 'translate hello to spanish'\n"
        response += "   • 'translate bonjour from french to english'\n"
        response += "   • 'detect language hola mundo'\n"
        response += "   • 'list languages'\n"
        
        return response
    
    def translate_phrase(self, phrase: str, target_language: str) -> str:
        """Translate a common phrase."""
        try:
            # Common phrases for quick translation
            common_phrases = {
                'hello': {
                    'es': 'hola', 'fr': 'bonjour', 'de': 'hallo', 'it': 'ciao',
                    'pt': 'olá', 'ru': 'привет', 'zh': '你好', 'ja': 'こんにちは',
                    'ko': '안녕하세요', 'ar': 'مرحبا', 'hi': 'नमस्ते'
                },
                'thank you': {
                    'es': 'gracias', 'fr': 'merci', 'de': 'danke', 'it': 'grazie',
                    'pt': 'obrigado', 'ru': 'спасибо', 'zh': '谢谢', 'ja': 'ありがとう',
                    'ko': '감사합니다', 'ar': 'شكرا', 'hi': 'धन्यवाद'
                },
                'goodbye': {
                    'es': 'adiós', 'fr': 'au revoir', 'de': 'auf wiedersehen', 'it': 'arrivederci',
                    'pt': 'tchau', 'ru': 'до свидания', 'zh': '再见', 'ja': 'さようなら',
                    'ko': '안녕히 가세요', 'ar': 'وداعا', 'hi': 'अलविदा'
                }
            }
            
            phrase_lower = phrase.lower().strip()
            target_lang = self._normalize_language(target_language)
            
            if phrase_lower in common_phrases and target_lang in common_phrases[phrase_lower]:
                translation = common_phrases[phrase_lower][target_lang]
                lang_name = self._get_language_name(target_lang)
                flag = self.language_flags.get(target_lang, '🌍')
                
                return f"🌍 **Quick Translation**\n\n{flag} **{phrase}** → **{translation}** ({lang_name})"
            else:
                # Use regular translation
                return self.translate_text(phrase, target_language)
                
        except Exception as e:
            return f"❌ Phrase translation error: {str(e)}"
    
    def get_translation_tips(self) -> str:
        """Get translation tips and best practices."""
        return """💡 **Translation Tips & Best Practices**

🌍 **For Better Translations:**
   • Use complete sentences rather than fragments
   • Provide context when possible
   • Avoid slang and idioms for better accuracy
   • Break long texts into smaller chunks
   • Verify important translations with multiple sources

🔧 **Translation Services:**
   • LibreTranslate - Free, open source
   • Google Translate - High accuracy, many languages
   • Microsoft Translator - Good for business contexts
   • Always cross-check critical translations

⚠️ **Important Notes:**
   • Machine translation may not be 100% accurate
   • Cultural context can be lost in translation
   • Legal and medical documents need human translation
   • Always verify important information
   • Some languages have regional variations

🎯 **Best Practices:**
   • Use simple, clear language
   • Avoid complex sentence structures
   • Include punctuation for better parsing
   • Test with short phrases first
   • Consider cultural differences

📚 **Learning Languages:**
   • Practice with native speakers
   • Use language learning apps
   • Watch movies with subtitles
   • Read books in the target language
   • Join language exchange communities
"""
