"""
ClipboardService.py
Clipboard management service for JARVIS.
"""

import os
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import threading

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    print("⚠️ pyperclip not available. Install with: pip install pyperclip")

class JarvisClipboardService:
    """
    Clipboard management service with:
    - Clipboard history tracking
    - Clipboard content management
    - Quick paste operations
    - Clipboard monitoring
    - Content formatting
    """
    
    def __init__(self, data_dir: str = "Data/clipboard"):
        self.data_dir = data_dir
        self.clipboard_file = os.path.join(data_dir, "clipboard_history.json")
        self.snippets_file = os.path.join(data_dir, "snippets.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Load existing data
        self.clipboard_history = self._load_clipboard_history()
        self.snippets = self._load_snippets()
        
        # Clipboard monitoring
        self.last_clipboard_content = ""
        self.monitoring = False
        self.monitor_thread = None
        
        if CLIPBOARD_AVAILABLE:
            self.last_clipboard_content = self._get_clipboard_content()
    
    def _load_clipboard_history(self) -> List[Dict[str, Any]]:
        """Load clipboard history from file."""
        try:
            if os.path.exists(self.clipboard_file):
                with open(self.clipboard_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"⚠️ Error loading clipboard history: {e}")
            return []
    
    def _save_clipboard_history(self):
        """Save clipboard history to file."""
        try:
            with open(self.clipboard_file, 'w', encoding='utf-8') as f:
                json.dump(self.clipboard_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Error saving clipboard history: {e}")
    
    def _load_snippets(self) -> Dict[str, str]:
        """Load snippets from file."""
        try:
            if os.path.exists(self.snippets_file):
                with open(self.snippets_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return self._get_default_snippets()
        except Exception as e:
            print(f"⚠️ Error loading snippets: {e}")
            return self._get_default_snippets()
    
    def _save_snippets(self):
        """Save snippets to file."""
        try:
            with open(self.snippets_file, 'w', encoding='utf-8') as f:
                json.dump(self.snippets, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Error saving snippets: {e}")
    
    def _get_default_snippets(self) -> Dict[str, str]:
        """Get default text snippets."""
        return {
            'email': 'Please find the attached document for your review.\n\nBest regards,\n[Your Name]',
            'meeting': 'Meeting Agenda:\n1. \n2. \n3. \n\nAction Items:\n- \n- \n- ',
            'phone': 'Hi, this is [Your Name] calling about [Topic]. Please call me back at [Your Number].',
            'signature': 'Best regards,\n[Your Name]\n[Your Title]\n[Company Name]\n[Phone] [Email]',
            'todo': 'TODO List:\n□ \n□ \n□ \n□ ',
            'code': '# Code snippet\n',
            'html': '<html>\n<head>\n    <title></title>\n</head>\n<body>\n    \n</body>\n</html>',
            'python': '#!/usr/bin/env python3\n"""\nDocstring\n"""\n\ndef main():\n    pass\n\nif __name__ == "__main__":\n    main()',
            'json': '{\n    "key": "value",\n    "array": [\n        "item1",\n        "item2"\n    ]\n}',
            'markdown': '# Heading\n\n## Subheading\n\n**Bold text**\n\n*Italic text*\n\n- List item 1\n- List item 2'
        }
    
    def _get_clipboard_content(self) -> str:
        """Get current clipboard content."""
        if not CLIPBOARD_AVAILABLE:
            return ""
        
        try:
            return pyperclip.paste()
        except Exception as e:
            print(f"⚠️ Error getting clipboard content: {e}")
            return ""
    
    def _set_clipboard_content(self, content: str) -> bool:
        """Set clipboard content."""
        if not CLIPBOARD_AVAILABLE:
            return False
        
        try:
            pyperclip.copy(content)
            return True
        except Exception as e:
            print(f"⚠️ Error setting clipboard content: {e}")
            return False
    
    def copy_text(self, text: str, add_to_history: bool = True) -> str:
        """
        Copy text to clipboard and optionally add to history.
        
        Args:
            text: Text to copy
            add_to_history: Whether to add to clipboard history
        """
        try:
            if not CLIPBOARD_AVAILABLE:
                return "❌ Clipboard not available. Install pyperclip: pip install pyperclip"
            
            # Copy to clipboard
            if self._set_clipboard_content(text):
                # Add to history if requested
                if add_to_history:
                    self._add_to_history(text)
                
                return f"✅ Copied to clipboard: {text[:50]}{'...' if len(text) > 50 else ''}"
            else:
                return "❌ Failed to copy to clipboard"
                
        except Exception as e:
            return f"❌ Error copying text: {str(e)}"
    
    def paste_text(self) -> str:
        """Get current clipboard content."""
        try:
            if not CLIPBOARD_AVAILABLE:
                return "❌ Clipboard not available. Install pyperclip: pip install pyperclip"
            
            content = self._get_clipboard_content()
            if content:
                return f"📋 **Clipboard Content:**\n\n{content}"
            else:
                return "📋 Clipboard is empty"
                
        except Exception as e:
            return f"❌ Error getting clipboard content: {str(e)}"
    
    def _add_to_history(self, content: str):
        """Add content to clipboard history."""
        try:
            # Avoid duplicates
            if self.clipboard_history and self.clipboard_history[-1]['content'] == content:
                return
            
            entry = {
                'content': content,
                'timestamp': datetime.now().isoformat(),
                'length': len(content),
                'type': self._detect_content_type(content)
            }
            
            self.clipboard_history.append(entry)
            
            # Keep only last 100 entries
            if len(self.clipboard_history) > 100:
                self.clipboard_history = self.clipboard_history[-100:]
            
            self._save_clipboard_history()
            
        except Exception as e:
            print(f"⚠️ Error adding to history: {e}")
    
    def _detect_content_type(self, content: str) -> str:
        """Detect the type of clipboard content."""
        content_lower = content.lower().strip()
        
        # Email
        if '@' in content and '.' in content.split('@')[-1]:
            return 'email'
        
        # URL
        if content.startswith(('http://', 'https://', 'www.')):
            return 'url'
        
        # Phone number
        if any(char.isdigit() for char in content) and len([c for c in content if c.isdigit()]) >= 10:
            return 'phone'
        
        # Code
        if any(content.startswith(prefix) for prefix in ['def ', 'class ', 'import ', 'from ', '#!/', '<?php', '<html']):
            return 'code'
        
        # JSON
        if content.strip().startswith('{') and content.strip().endswith('}'):
            return 'json'
        
        # HTML
        if content.strip().startswith('<') and content.strip().endswith('>'):
            return 'html'
        
        # Markdown
        if content.startswith('#') or '**' in content or '*' in content:
            return 'markdown'
        
        # Default to text
        return 'text'
    
    def get_clipboard_history(self, limit: int = 10, content_type: str = None) -> str:
        """
        Get clipboard history.
        
        Args:
            limit: Number of entries to show
            content_type: Filter by content type
        """
        try:
            if not self.clipboard_history:
                return "📋 No clipboard history found"
            
            # Filter by content type if specified
            filtered_history = self.clipboard_history
            if content_type:
                filtered_history = [entry for entry in self.clipboard_history if entry['type'] == content_type]
            
            if not filtered_history:
                return f"📋 No {content_type} entries in clipboard history"
            
            # Get recent entries
            recent_entries = filtered_history[-limit:]
            recent_entries.reverse()  # Show newest first
            
            response = f"📋 **Clipboard History** ({len(recent_entries)} entries)\n\n"
            
            for i, entry in enumerate(recent_entries, 1):
                timestamp = datetime.fromisoformat(entry['timestamp'])
                content_preview = entry['content'][:100] + "..." if len(entry['content']) > 100 else entry['content']
                
                response += f"**{i}. [{entry['type'].upper()}]** {timestamp.strftime('%H:%M:%S')}\n"
                response += f"   📏 {entry['length']} characters\n"
                response += f"   📝 {content_preview}\n\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting clipboard history: {str(e)}"
    
    def clear_clipboard_history(self) -> str:
        """Clear clipboard history."""
        try:
            self.clipboard_history = []
            self._save_clipboard_history()
            return "✅ Clipboard history cleared"
        except Exception as e:
            return f"❌ Error clearing clipboard history: {str(e)}"
    
    def add_snippet(self, name: str, content: str) -> str:
        """Add a text snippet."""
        try:
            self.snippets[name] = content
            self._save_snippets()
            return f"✅ Added snippet: {name}"
        except Exception as e:
            return f"❌ Error adding snippet: {str(e)}"
    
    def get_snippet(self, name: str) -> str:
        """Get a text snippet."""
        try:
            if name not in self.snippets:
                available_snippets = ', '.join(self.snippets.keys())
                return f"❌ Snippet '{name}' not found. Available snippets: {available_snippets}"
            
            snippet = self.snippets[name]
            
            # Copy to clipboard
            if self._set_clipboard_content(snippet):
                return f"✅ Copied snippet '{name}' to clipboard:\n\n{snippet}"
            else:
                return f"📝 **Snippet: {name}**\n\n{snippet}"
                
        except Exception as e:
            return f"❌ Error getting snippet: {str(e)}"
    
    def list_snippets(self) -> str:
        """List all available snippets."""
        try:
            if not self.snippets:
                return "📝 No snippets found"
            
            response = "📝 **Available Snippets**\n\n"
            
            for name, content in self.snippets.items():
                content_preview = content[:50] + "..." if len(content) > 50 else content
                response += f"📋 **{name}**\n"
                response += f"   {content_preview}\n\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error listing snippets: {str(e)}"
    
    def delete_snippet(self, name: str) -> str:
        """Delete a snippet."""
        try:
            if name not in self.snippets:
                return f"❌ Snippet '{name}' not found"
            
            del self.snippets[name]
            self._save_snippets()
            return f"✅ Deleted snippet: {name}"
        except Exception as e:
            return f"❌ Error deleting snippet: {str(e)}"
    
    def format_clipboard(self, format_type: str) -> str:
        """
        Format current clipboard content.
        
        Args:
            format_type: Type of formatting (uppercase, lowercase, title, reverse, etc.)
        """
        try:
            if not CLIPBOARD_AVAILABLE:
                return "❌ Clipboard not available"
            
            content = self._get_clipboard_content()
            if not content:
                return "📋 Clipboard is empty"
            
            # Apply formatting
            if format_type == 'uppercase':
                formatted = content.upper()
            elif format_type == 'lowercase':
                formatted = content.lower()
            elif format_type == 'title':
                formatted = content.title()
            elif format_type == 'reverse':
                formatted = content[::-1]
            elif format_type == 'remove_spaces':
                formatted = content.replace(' ', '')
            elif format_type == 'add_quotes':
                formatted = f'"{content}"'
            elif format_type == 'add_brackets':
                formatted = f'[{content}]'
            elif format_type == 'add_parentheses':
                formatted = f'({content})'
            else:
                return f"❌ Unknown format type: {format_type}"
            
            # Copy formatted content
            if self._set_clipboard_content(formatted):
                self._add_to_history(formatted)
                return f"✅ Formatted and copied: {format_type}\n\n{formatted}"
            else:
                return "❌ Failed to copy formatted content"
                
        except Exception as e:
            return f"❌ Error formatting clipboard: {str(e)}"
    
    def start_monitoring(self) -> str:
        """Start clipboard monitoring."""
        try:
            if not CLIPBOARD_AVAILABLE:
                return "❌ Clipboard monitoring not available. Install pyperclip: pip install pyperclip"
            
            if self.monitoring:
                return "⚠️ Clipboard monitoring is already running"
            
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_clipboard, daemon=True)
            self.monitor_thread.start()
            
            return "✅ Clipboard monitoring started"
            
        except Exception as e:
            return f"❌ Error starting clipboard monitoring: {str(e)}"
    
    def stop_monitoring(self) -> str:
        """Stop clipboard monitoring."""
        try:
            self.monitoring = False
            return "✅ Clipboard monitoring stopped"
        except Exception as e:
            return f"❌ Error stopping clipboard monitoring: {str(e)}"
    
    def _monitor_clipboard(self):
        """Background thread to monitor clipboard changes."""
        while self.monitoring:
            try:
                current_content = self._get_clipboard_content()
                
                if current_content != self.last_clipboard_content and current_content:
                    self.last_clipboard_content = current_content
                    self._add_to_history(current_content)
                    print(f"📋 Clipboard updated: {current_content[:50]}...")
                
                time.sleep(1)  # Check every second
                
            except Exception as e:
                print(f"⚠️ Clipboard monitoring error: {e}")
                time.sleep(5)
    
    def get_clipboard_stats(self) -> str:
        """Get clipboard statistics."""
        try:
            if not self.clipboard_history:
                return "📊 No clipboard statistics available"
            
            # Calculate statistics
            total_entries = len(self.clipboard_history)
            content_types = {}
            total_characters = 0
            
            for entry in self.clipboard_history:
                content_type = entry['type']
                content_types[content_type] = content_types.get(content_type, 0) + 1
                total_characters += entry['length']
            
            avg_length = total_characters / total_entries if total_entries > 0 else 0
            
            response = "📊 **Clipboard Statistics**\n\n"
            response += f"📋 **Total Entries:** {total_entries}\n"
            response += f"📏 **Total Characters:** {total_characters:,}\n"
            response += f"📊 **Average Length:** {avg_length:.1f} characters\n\n"
            
            response += "📈 **Content Types:**\n"
            for content_type, count in sorted(content_types.items(), key=lambda x: x[1], reverse=True):
                response += f"   • {content_type.title()}: {count} entries\n"
            
            if self.monitoring:
                response += f"\n🔄 **Monitoring:** Active\n"
            else:
                response += f"\n🔄 **Monitoring:** Inactive\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting clipboard stats: {str(e)}"
    
    def get_clipboard_help(self) -> str:
        """Get help information for clipboard features."""
        return """📋 **Clipboard Management Help**

🔧 **Basic Operations:**
   • 'copy [text]' - Copy text to clipboard
   • 'paste' - Show current clipboard content
   • 'clipboard history' - Show recent clipboard entries
   • 'clear clipboard history' - Clear clipboard history

📝 **Text Snippets:**
   • 'snippet [name]' - Copy snippet to clipboard
   • 'add snippet [name] [content]' - Add new snippet
   • 'list snippets' - Show all available snippets
   • 'delete snippet [name]' - Remove snippet

🎨 **Text Formatting:**
   • 'format clipboard uppercase' - Convert to uppercase
   • 'format clipboard lowercase' - Convert to lowercase
   • 'format clipboard title' - Convert to title case
   • 'format clipboard reverse' - Reverse text
   • 'format clipboard remove_spaces' - Remove spaces
   • 'format clipboard add_quotes' - Add quotes around text

🔄 **Monitoring:**
   • 'start clipboard monitoring' - Monitor clipboard changes
   • 'stop clipboard monitoring' - Stop monitoring
   • 'clipboard stats' - Show clipboard statistics

📊 **Content Types Detected:**
   • Email addresses
   • URLs
   • Phone numbers
   • Code snippets
   • JSON data
   • HTML content
   • Markdown text
   • Plain text

💡 **Examples:**
   • 'copy Hello World'
   • 'snippet email'
   • 'format clipboard uppercase'
   • 'clipboard history 5'
   • 'add snippet signature Best regards, John'

📋 **Default Snippets Available:**
   • email, meeting, phone, signature
   • todo, code, python, html, json, markdown
"""
