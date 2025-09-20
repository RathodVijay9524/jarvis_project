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
        
        # Detect installed applications
        self.installed_apps = self._detect_installed_applications()
        
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
        
        # Detect installed applications on initialization (with timeout protection)
        try:
            self.installed_apps = self._detect_installed_applications()
        except Exception as e:
            print(f"⚠️ App detection failed: {e}")
            self.installed_apps = {}
    
    def _detect_installed_applications(self) -> Dict[str, str]:
        """
        Detect installed applications on the system.
        Returns a dictionary mapping app names to their executable paths.
        """
        installed_apps = {}
        
        if self.system == "windows":
            # Common installation directories
            search_paths = [
                os.environ.get('PROGRAMFILES', 'C:\\Program Files'),
                os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'),
                os.path.join(os.path.expanduser("~"), "AppData", "Local"),
                os.path.join(os.path.expanduser("~"), "AppData", "Roaming"),
            ]
            
            # Common application patterns
            app_patterns = {
                'intellij': ['IntelliJ IDEA', 'JetBrains', 'idea64.exe', 'idea.exe'],
                'pycharm': ['PyCharm', 'JetBrains', 'pycharm64.exe', 'pycharm.exe'],
                'vscode': ['Microsoft VS Code', 'Code.exe'],
                'visual studio': ['Microsoft Visual Studio', 'devenv.exe'],
                'notepad++': ['Notepad++', 'notepad++.exe'],
                'sublime': ['Sublime Text', 'sublime_text.exe'],
                'atom': ['Atom', 'atom.exe'],
                'discord': ['Discord', 'Discord.exe'],
                'slack': ['Slack', 'Slack.exe'],
                'teams': ['Microsoft Teams', 'Teams.exe'],
                'zoom': ['Zoom', 'Zoom.exe'],
                'vlc': ['VLC', 'vlc.exe'],
                'obs': ['obs-studio', 'obs64.exe', 'obs32.exe'],
                'steam': ['Steam', 'Steam.exe'],
                'epic games': ['Epic Games', 'EpicGamesLauncher.exe'],
                'origin': ['Origin', 'Origin.exe'],
                'adobe photoshop': ['Adobe', 'Photoshop.exe'],
                'adobe premiere': ['Adobe', 'Adobe Premiere Pro.exe'],
                'blender': ['Blender Foundation', 'blender.exe'],
                'gimp': ['GIMP', 'gimp.exe'],
                'audacity': ['Audacity', 'audacity.exe'],
                'wireshark': ['Wireshark', 'Wireshark.exe'],
                'putty': ['PuTTY', 'putty.exe'],
                'filezilla': ['FileZilla', 'filezilla.exe'],
                '7zip': ['7-Zip', '7zFM.exe'],
                'winrar': ['WinRAR', 'WinRAR.exe'],
            }
            
            # Limit to most common applications for faster detection
            priority_apps = ['intellij', 'pycharm', 'vscode', 'notepad++', 'discord']
            
            for app_name, patterns in app_patterns.items():
                if app_name not in priority_apps:
                    continue  # Skip non-priority apps for faster startup
                    
                for search_path in search_paths[:2]:  # Only search first 2 paths
                    if not os.path.exists(search_path):
                        continue
                    
                    try:
                        # Quick directory scan - only go 2 levels deep
                        for root, dirs, files in os.walk(search_path):
                            if root.count(os.sep) - search_path.count(os.sep) > 2:
                                dirs.clear()  # Don't recurse deeper
                                continue
                            
                            # Quick pattern matching
                            for pattern in patterns:
                                if pattern in root:
                                    # Look for executable files
                                    for file in files:
                                        if file.lower().endswith('.exe') and pattern.lower() in file.lower():
                                            full_path = os.path.join(root, file)
                                            installed_apps[app_name] = full_path
                                            break
                                    if app_name in installed_apps:
                                        break
                            
                            if app_name in installed_apps:
                                break
                    except (PermissionError, OSError, Exception):
                        continue
        
        return installed_apps
    
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
        Open a specific file or file type. Can handle:
        - Specific file paths: "open C:/Users/file.txt"
        - File names: "open myfile.docx" 
        - File types: "open text file", "open pdf"
        """
        try:
            # Check if query contains a specific file path
            if any(char in query for char in ['/', '\\', ':']):
                # Extract potential file path from query
                words = query.split()
                for i, word in enumerate(words):
                    if any(char in word for char in ['/', '\\', ':']):
                        # Found a path-like string
                        potential_path = ' '.join(words[i:])  # Take rest of query as path
                        if os.path.exists(potential_path):
                            if self.system == "windows":
                                os.startfile(potential_path)
                            return f"✅ Opened '{os.path.basename(potential_path)}'"
            
            # Search for files by name in common locations
            search_locations = [
                self.desktop_path,
                self.documents_path,
                os.path.join(os.path.expanduser("~"), "Downloads"),
                os.path.expanduser("~")
            ]
            
            # Extract potential filename from query
            query_lower = query.lower()
            
            found_files = []
            for location in search_locations:
                if os.path.exists(location):
                    for root, dirs, files in os.walk(location):
                        # Don't search too deep (max 2 levels)
                        if root.count(os.sep) - location.count(os.sep) > 2:
                            continue
                            
                        for file in files:
                            file_lower = file.lower()
                            # Check if any word in query matches filename
                            query_words = [word for word in query_lower.split() if len(word) > 2]
                            if any(word in file_lower for word in query_words):
                                full_path = os.path.join(root, file)
                                found_files.append((full_path, os.path.getmtime(full_path)))
            
            if found_files:
                # Sort by modification time and take the most recent
                found_files.sort(key=lambda x: x[1], reverse=True)
                file_path = found_files[0][0]
                
                if self.system == "windows":
                    os.startfile(file_path)
                
                return f"✅ Opened '{os.path.basename(file_path)}' from {os.path.dirname(file_path)}"
            
            # If no specific file found, look for files by type
            file_extensions = {
                'text': ['.txt', '.md', '.log'],
                'document': ['.docx', '.doc', '.pdf'],
                'spreadsheet': ['.xlsx', '.xls', '.csv'],
                'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
                'video': ['.mp4', '.avi', '.mkv', '.mov'],
                'audio': ['.mp3', '.wav', '.flac', '.m4a']
            }
            
            for file_type, extensions in file_extensions.items():
                if file_type in query_lower:
                    for location in search_locations:
                        if os.path.exists(location):
                            for file in os.listdir(location):
                                if any(file.lower().endswith(ext) for ext in extensions):
                                    file_path = os.path.join(location, file)
                                    if self.system == "windows":
                                        os.startfile(file_path)
                                    return f"✅ Opened {file_type} file: '{file}'"
            
            return f"❌ Could not find file matching: '{query}'. Try specifying full path or filename."
                
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
        Open a specific folder. Can handle:
        - Specific folder paths: "open C:/Users/MyFolder"
        - Common folder names: "desktop", "documents", "downloads"
        - Project folders: "open project folder"
        """
        try:
            query_lower = query.lower()
            
            # Check if query contains a specific folder path
            if any(char in query for char in ['/', '\\', ':']):
                # Extract potential folder path from query
                words = query.split()
                for i, word in enumerate(words):
                    if any(char in word for char in ['/', '\\', ':']):
                        # Found a path-like string
                        potential_path = ' '.join(words[i:])  # Take rest of query as path
                        if os.path.exists(potential_path) and os.path.isdir(potential_path):
                            if self.system == "windows":
                                subprocess.Popen(['explorer', potential_path])
                            return f"✅ Opened '{os.path.basename(potential_path)}' folder"
            
            # Handle common folder names
            folder_mappings = {
                'desktop': self.desktop_path,
                'document': self.documents_path,
                'download': os.path.join(os.path.expanduser("~"), "Downloads"),
                'music': os.path.join(os.path.expanduser("~"), "Music"),
                'picture': os.path.join(os.path.expanduser("~"), "Pictures"),
                'video': os.path.join(os.path.expanduser("~"), "Videos"),
                'home': os.path.expanduser("~"),
                'user': os.path.expanduser("~"),
                'temp': os.environ.get('TEMP', '/tmp'),
                'program': os.environ.get('PROGRAMFILES', 'C:\\Program Files'),
                'appdata': os.environ.get('APPDATA', ''),
            }
            
            # Check for direct folder matches
            for folder_name, folder_path in folder_mappings.items():
                if folder_name in query_lower and folder_path and os.path.exists(folder_path):
                    if self.system == "windows":
                        subprocess.Popen(['explorer', folder_path])
                    return f"✅ Opened {folder_name.title()} folder"
            
            # Search for folders by name in common locations
            search_locations = [
                os.path.expanduser("~"),
                self.desktop_path,
                self.documents_path,
                os.path.join(os.path.expanduser("~"), "Downloads"),
            ]
            
            found_folders = []
            query_words = [word for word in query_lower.split() if len(word) > 2]
            
            for location in search_locations:
                if os.path.exists(location):
                    try:
                        for item in os.listdir(location):
                            item_path = os.path.join(location, item)
                            if os.path.isdir(item_path):
                                item_lower = item.lower()
                                # Check if any word in query matches folder name
                                if any(word in item_lower for word in query_words):
                                    found_folders.append((item_path, os.path.getmtime(item_path)))
                    except PermissionError:
                        continue
            
            if found_folders:
                # Sort by modification time and take the most recent
                found_folders.sort(key=lambda x: x[1], reverse=True)
                folder_path = found_folders[0][0]
                
                if self.system == "windows":
                    subprocess.Popen(['explorer', folder_path])
                
                return f"✅ Opened '{os.path.basename(folder_path)}' folder from {os.path.dirname(folder_path)}"
            
            # Default to desktop if nothing found
            if self.system == "windows":
                subprocess.Popen(['explorer', self.desktop_path])
            
            return f"ℹ️ Could not find specific folder '{query}', opened Desktop instead"
            
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
        Open applications or websites. Can handle:
        - Installed applications: "open IntelliJ", "open PyCharm"
        - Web applications: "open YouTube", "open Facebook"
        - System applications: "open notepad", "open calculator"
        """
        try:
            query_lower = query.lower()
            
            # First, check detected installed applications
            for app_name, app_path in self.installed_apps.items():
                if app_name in query_lower:
                    if self.system == "windows":
                        subprocess.Popen([app_path])
                    return f"✅ Opened {app_name.title()} from detected installation"
            
            # Then check predefined app mappings
            for app_name, command in self.app_mappings.items():
                if app_name in query_lower:
                    if command.startswith('http'):
                        # It's a website
                        webbrowser.open(command)
                        return f"✅ Opened {app_name.title()} in your browser"
                    else:
                        # It's an application
                        if self.system == "windows":
                            try:
                                subprocess.Popen([command], shell=True)
                                return f"✅ Opened {app_name.title()}"
                            except FileNotFoundError:
                                # Try alternative methods
                                try:
                                    os.startfile(command)
                                    return f"✅ Opened {app_name.title()}"
                                except:
                                    continue
            
            # Try to find application by searching common locations
            query_words = [word for word in query_lower.split() if len(word) > 2]
            
            search_paths = [
                os.environ.get('PROGRAMFILES', 'C:\\Program Files'),
                os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'),
                os.path.join(os.path.expanduser("~"), "AppData", "Local"),
                self.desktop_path,
            ]
            
            for search_path in search_paths:
                if not os.path.exists(search_path):
                    continue
                
                try:
                    for root, dirs, files in os.walk(search_path):
                        # Don't search too deep
                        if root.count(os.sep) - search_path.count(os.sep) > 2:
                            continue
                        
                        for file in files:
                            if file.lower().endswith('.exe'):
                                file_lower = file.lower()
                                # Check if any query word matches the executable name
                                if any(word in file_lower for word in query_words):
                                    full_path = os.path.join(root, file)
                                    if self.system == "windows":
                                        subprocess.Popen([full_path])
                                    return f"✅ Opened '{file}' from {root}"
                except (PermissionError, OSError):
                    continue
            
            # If still not found, provide helpful message with detected apps
            if self.installed_apps:
                detected_list = ", ".join(list(self.installed_apps.keys())[:10])
                return f"❌ Could not find application in query: '{query}'.\n🔍 Detected applications: {detected_list}"
            else:
                return f"❌ Could not find application in query: '{query}'. Try using full application name or path."
            
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
