"""
AdvancedAutomation.py
Advanced automation system for JARVIS with file operations, email creation, and system control.
Based on Kaushik Shresth's requirements.
"""

import os
import subprocess
import platform
import time
import webbrowser
import psutil
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

class JarvisAdvancedAutomation:
    """
    Advanced automation system that can handle:
    - File operations (create, open, close, delete)
    - Folder management
    - Email creation
    - Application control
    - System operations
    """
    
    def __init__(self):
        self.system = platform.system().lower()
        self.desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        self.documents_path = os.path.join(os.path.expanduser("~"), "Documents")
        
        # Ensure directories exist
        os.makedirs(self.desktop_path, exist_ok=True)
        os.makedirs(self.documents_path, exist_ok=True)
        
        # Enhanced application mappings
        self.app_mappings = {
            # Browsers
            "chrome": "chrome",
            "firefox": "firefox", 
            "edge": "msedge",
            "browser": "chrome",
            
            # Social Media (web-based)
            "facebook": "https://facebook.com",
            "instagram": "https://instagram.com", 
            "youtube": "https://youtube.com",
            "twitter": "https://twitter.com",
            "linkedin": "https://linkedin.com",
            
            # Office & Productivity
            "notepad": "notepad",
            "word": "winword",
            "excel": "excel",
            "powerpoint": "powerpnt",
            "calculator": "calc",
            "paint": "mspaint",
            
            # System
            "explorer": "explorer",
            "cmd": "cmd",
            "powershell": "powershell",
            "control": "control",
            "taskmgr": "taskmgr",
        }
    
    def process_automation_query(self, query: str) -> str:
        """
        Process automation queries and execute appropriate actions.
        """
        query_lower = query.lower().strip()
        
        try:
            # File operations
            if "create" in query_lower and ("file" in query_lower or "document" in query_lower):
                return self.create_file(query_lower)
            
            elif "open" in query_lower and "file" in query_lower:
                return self.open_file(query_lower)
            
            # Folder operations
            elif "close" in query_lower and ("folder" in query_lower or "window" in query_lower):
                return self.close_folders()
            
            elif "open" in query_lower and "folder" in query_lower:
                return self.open_folder(query_lower)
            
            # Email operations
            elif "email" in query_lower or "mail" in query_lower:
                return self.create_email(query_lower)
            
            # Application operations
            elif "open" in query_lower:
                return self.open_application(query_lower)
            
            elif "close" in query_lower:
                return self.close_application(query_lower)
            
            # System operations
            elif "shutdown" in query_lower:
                return self.shutdown_system()
            
            elif "restart" in query_lower:
                return self.restart_system()
            
            # Image generation
            elif "generate" in query_lower and "image" in query_lower:
                return self.generate_image(query_lower)
            
            # Reminders and timers
            elif "remind" in query_lower or "reminder" in query_lower:
                return self.set_reminder(query_lower)
            
            else:
                return f"I understand you want automation for: '{query}', but I'm not sure how to handle this specific request. Can you be more specific?"
                
        except Exception as e:
            return f"❌ Automation error: {str(e)}"
    
    def create_file(self, query: str) -> str:
        """
        Create a new file based on the query.
        """
        try:
            # Extract filename if mentioned
            filename = "jarvis_document.txt"
            
            if "email" in query or "mail" in query:
                filename = "email_draft.txt"
                content = f"""To: 
From: 
Subject: 

Dear ,

[Write your email content here]

Best regards,
{os.getenv('USERNAME', 'User')}

---
Created by JARVIS on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            elif "song" in query:
                filename = "song_lyrics.txt"
                content = f"""Song Title: [Your Song Title]
Artist: [Your Name]
Date: {datetime.now().strftime('%Y-%m-%d')}

Verse 1:
[Write your lyrics here]

Chorus:
[Write your chorus here]

Verse 2:
[Continue your lyrics]

---
Created by JARVIS
"""
            elif "note" in query:
                filename = "jarvis_note.txt"
                content = f"""JARVIS Note
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

[Write your notes here]

---
Personal Assistant: JARVIS
"""
            else:
                content = f"""Document created by JARVIS
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

[Your content goes here]

---
JARVIS AI Assistant
"""
            
            # Create file path
            file_path = os.path.join(self.desktop_path, filename)
            
            # Write content to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Open the file in notepad
            if self.system == "windows":
                subprocess.Popen(['notepad', file_path])
            
            return f"✅ Created and opened '{filename}' on your desktop with template content."
            
        except Exception as e:
            return f"❌ Error creating file: {str(e)}"
    
    def open_file(self, query: str) -> str:
        """
        Open a specific file or file type.
        """
        try:
            # Look for common files on desktop
            common_files = []
            
            if os.path.exists(self.desktop_path):
                for file in os.listdir(self.desktop_path):
                    if file.endswith(('.txt', '.docx', '.pdf', '.xlsx')):
                        common_files.append(file)
            
            if common_files:
                # Open the most recent file
                latest_file = max(
                    [os.path.join(self.desktop_path, f) for f in common_files],
                    key=os.path.getmtime
                )
                
                if self.system == "windows":
                    os.startfile(latest_file)
                
                return f"✅ Opened '{os.path.basename(latest_file)}'"
            else:
                return "❌ No suitable files found on desktop. Try creating a file first."
                
        except Exception as e:
            return f"❌ Error opening file: {str(e)}"
    
    def close_folders(self) -> str:
        """
        Close all open folder windows.
        """
        try:
            closed_count = 0
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] == 'explorer.exe':
                        cmdline = proc.info.get('cmdline', [])
                        # Only close folder windows, not the desktop
                        if cmdline and len(cmdline) > 1:
                            proc.terminate()
                            closed_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if closed_count > 0:
                return f"✅ Closed {closed_count} folder window(s)"
            else:
                return "ℹ️ No folder windows were open"
                
        except Exception as e:
            return f"❌ Error closing folders: {str(e)}"
    
    def open_folder(self, query: str) -> str:
        """
        Open a specific folder.
        """
        try:
            if "desktop" in query:
                folder_path = self.desktop_path
            elif "document" in query:
                folder_path = self.documents_path
            elif "download" in query:
                folder_path = os.path.join(os.path.expanduser("~"), "Downloads")
            else:
                folder_path = self.desktop_path  # Default
            
            if self.system == "windows":
                subprocess.Popen(['explorer', folder_path])
            
            return f"✅ Opened {os.path.basename(folder_path)} folder"
            
        except Exception as e:
            return f"❌ Error opening folder: {str(e)}"
    
    def create_email(self, query: str) -> str:
        """
        Create an email draft and open email client.
        """
        try:
            # Create email draft file first
            email_content = f"""To: [Recipient Email]
From: [Your Email]
Subject: [Email Subject]

Dear [Recipient Name],

[Write your email message here]

Best regards,
[Your Name]

---
Email draft created by JARVIS on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            # Save draft to desktop
            draft_path = os.path.join(self.desktop_path, "email_draft.txt")
            with open(draft_path, 'w', encoding='utf-8') as f:
                f.write(email_content)
            
            # Open email client
            webbrowser.open('mailto:')
            
            # Also open the draft file
            if self.system == "windows":
                subprocess.Popen(['notepad', draft_path])
            
            return f"✅ Created email draft on desktop and opened email client. You can compose your email in both places."
            
        except Exception as e:
            return f"❌ Error creating email: {str(e)}"
    
    def open_application(self, query: str) -> str:
        """
        Open applications or websites.
        """
        try:
            # Extract app name from query
            for app_name, command in self.app_mappings.items():
                if app_name in query:
                    if command.startswith('http'):
                        # It's a website
                        webbrowser.open(command)
                        return f"✅ Opened {app_name.title()} in your browser"
                    else:
                        # It's an application
                        if self.system == "windows":
                            subprocess.Popen([command], shell=True)
                        return f"✅ Opened {app_name.title()}"
            
            return f"❌ Could not find application in query: '{query}'"
            
        except Exception as e:
            return f"❌ Error opening application: {str(e)}"
    
    def close_application(self, query: str) -> str:
        """
        Close specific applications.
        """
        try:
            closed_count = 0
            
            # Extract app name from query
            for app_name, command in self.app_mappings.items():
                if app_name in query:
                    for proc in psutil.process_iter(['pid', 'name']):
                        try:
                            if command.lower() in proc.info['name'].lower():
                                proc.terminate()
                                closed_count += 1
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
            
            if closed_count > 0:
                return f"✅ Closed {closed_count} application(s)"
            else:
                return "ℹ️ No matching applications were running"
                
        except Exception as e:
            return f"❌ Error closing application: {str(e)}"
    
    def generate_image(self, query: str) -> str:
        """
        Handle image generation requests.
        """
        try:
            from Backend.ImageGeneration import JarvisImageGen
            
            # Extract image description
            description = query.replace("generate", "").replace("image", "").replace("of", "").strip()
            if not description:
                description = "a beautiful landscape"
            
            image_gen = JarvisImageGen()
            result = image_gen.generate_image(description)
            
            return f"🎨 {result}"
            
        except Exception as e:
            return f"❌ Error generating image: {str(e)}"
    
    def set_reminder(self, query: str) -> str:
        """
        Set reminders and timers.
        """
        try:
            # Simple timer implementation
            if "10 pm" in query.lower() or "10:00" in query.lower():
                # Calculate seconds until 10 PM
                now = datetime.now()
                target = now.replace(hour=22, minute=0, second=0, microsecond=0)
                if target <= now:
                    target = target.replace(day=target.day + 1)
                
                seconds = int((target - now).total_seconds())
                
                def reminder_thread():
                    time.sleep(seconds)
                    print("⏰ REMINDER: It's 10 PM!")
                
                import threading
                thread = threading.Thread(target=reminder_thread, daemon=True)
                thread.start()
                
                return f"⏰ Reminder set for 10 PM (in {seconds//3600} hours and {(seconds%3600)//60} minutes)"
            
            return "⏰ Reminder functionality is available. Try 'remind me at 10 PM'"
            
        except Exception as e:
            return f"❌ Error setting reminder: {str(e)}"
    
    def shutdown_system(self) -> str:
        """
        Shutdown the system.
        """
        try:
            if self.system == "windows":
                os.system("shutdown /s /t 60")  # 60 second delay
                return "🔌 System will shutdown in 60 seconds. Type 'shutdown /a' in cmd to cancel."
            return "🔌 Shutdown command sent"
        except Exception as e:
            return f"❌ Error shutting down: {str(e)}"
    
    def restart_system(self) -> str:
        """
        Restart the system.
        """
        try:
            if self.system == "windows":
                os.system("shutdown /r /t 60")  # 60 second delay
                return "🔄 System will restart in 60 seconds. Type 'shutdown /a' in cmd to cancel."
            return "🔄 Restart command sent"
        except Exception as e:
            return f"❌ Error restarting: {str(e)}"

if __name__ == "__main__":
    # Test the advanced automation
    automation = JarvisAdvancedAutomation()
    
    test_queries = [
        "create a file for email",
        "open facebook and instagram",
        "close all folders", 
        "create email draft",
        "open notepad",
        "generate image of tony stark"
    ]
    
    print("🤖 Testing Advanced Automation:")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        result = automation.process_automation_query(query)
        print(f"Result: {result}")
        print("-" * 30)
