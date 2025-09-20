"""
Automation.py
Advanced automation capabilities for JARVIS - app control, system operations, and task scheduling.
"""

import os
import subprocess
import platform
import time
import threading
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import webbrowser
import psutil
import math

class JarvisAutomation:
    def __init__(self):
        self.system = platform.system().lower()
        self.scheduled_tasks = []
        self.running_tasks = {}
        
        # Common application mappings
        self.app_mappings = {
            # Browsers
            "chrome": ["chrome", "google chrome", "google-chrome"],
            "firefox": ["firefox", "mozilla firefox"],
            "edge": ["edge", "microsoft edge", "msedge"],
            "safari": ["safari"],
            
            # Office & Productivity
            "word": ["word", "microsoft word", "winword"],
            "excel": ["excel", "microsoft excel"],
            "powerpoint": ["powerpoint", "microsoft powerpoint"],
            "outlook": ["outlook", "microsoft outlook"],
            "notepad": ["notepad", "notepad++", "notepad.exe"],
            "calculator": ["calculator", "calc", "calc.exe"],
            
            # Development
            "vscode": ["code", "visual studio code", "vscode"],
            "pycharm": ["pycharm"],
            "sublime": ["sublime", "sublime text"],
            "atom": ["atom"],
            
            # Media & Entertainment
            "vlc": ["vlc", "vlc media player"],
            "spotify": ["spotify"],
            "discord": ["discord"],
            "teams": ["teams", "microsoft teams"],
            "zoom": ["zoom"],
            
            # System
            "explorer": ["explorer", "file explorer", "windows explorer"],
            "cmd": ["cmd", "command prompt", "terminal"],
            "powershell": ["powershell", "windows powershell"],
            "control panel": ["control", "control panel"],
            "task manager": ["taskmgr", "task manager"],
        }
    
    def open_application(self, app_name: str) -> str:
        """
        Open an application by name.
        
        Args:
            app_name: Name of the application to open
            
        Returns:
            str: Status message
        """
        app_name_lower = app_name.lower().strip()
        
        try:
            # First, try direct mapping
            for app_key, app_variants in self.app_mappings.items():
                if app_name_lower in app_variants:
                    return self._launch_app(app_key, app_variants[0])
            
            # Try direct launch if no mapping found
            return self._launch_app(app_name, app_name_lower)
            
        except Exception as e:
            return f"Failed to open {app_name}: {str(e)}"
    
    def _launch_app(self, display_name: str, command: str) -> str:
        """
        Launch application using system-specific commands.
        """
        try:
            if self.system == "windows":
                # Try multiple methods for Windows
                methods = [
                    lambda: subprocess.Popen(f"start {command}", shell=True),
                    lambda: subprocess.Popen([command]),
                    lambda: os.system(f"start {command}"),
                ]
                
                for method in methods:
                    try:
                        method()
                        return f"✅ Successfully opened {display_name}"
                    except:
                        continue
                        
            elif self.system == "darwin":  # macOS
                subprocess.Popen(["open", "-a", command])
                return f"✅ Successfully opened {display_name}"
                
            elif self.system == "linux":
                subprocess.Popen([command])
                return f"✅ Successfully opened {display_name}"
            
            return f"❌ Could not open {display_name} on {self.system}"
            
        except Exception as e:
            return f"❌ Error opening {display_name}: {str(e)}"
    
    def get_system_info(self) -> str:
        """
        Get system information.
        
        Returns:
            str: Formatted system information
        """
        try:
            # CPU info
            cpu_count = psutil.cpu_count()
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory info
            memory = psutil.virtual_memory()
            memory_total = memory.total / (1024**3)  # GB
            memory_used = memory.used / (1024**3)   # GB
            memory_percent = memory.percent
            
            # Disk info
            disk = psutil.disk_usage('/')
            disk_total = disk.total / (1024**3)     # GB
            disk_used = disk.used / (1024**3)       # GB
            disk_percent = (disk_used / disk_total) * 100
            
            # System uptime
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            
            result = f"""🖥️ System Information:
📊 CPU: {cpu_count} cores, {cpu_percent}% usage
💾 Memory: {memory_used:.1f}GB / {memory_total:.1f}GB ({memory_percent}%)
💿 Disk: {disk_used:.1f}GB / {disk_total:.1f}GB ({disk_percent:.1f}%)
⏰ Uptime: {str(uptime).split('.')[0]}
🖥️ OS: {platform.system()} {platform.release()}
"""
            
            return result.strip()
            
        except Exception as e:
            return f"❌ Error getting system info: {str(e)}"
    
    def calculate(self, expression: str) -> str:
        """
        Perform mathematical calculations.
        
        Args:
            expression: Mathematical expression
            
        Returns:
            str: Calculation result
        """
        try:
            # Clean and prepare expression
            expression = expression.strip()
            
            # Replace common words with operators
            replacements = {
                ' plus ': '+',
                ' minus ': '-',
                ' times ': '*',
                ' multiplied by ': '*',
                ' divided by ': '/',
                ' to the power of ': '**',
                ' squared': '**2',
                ' cubed': '**3',
                'pi': str(math.pi),
                'e': str(math.e)
            }
            
            for word, symbol in replacements.items():
                expression = expression.replace(word, symbol)
            
            # Safe evaluation (limited to math operations)
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({"abs": abs, "round": round, "min": min, "max": max})
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            
            return f"🧮 {expression} = {result}"
            
        except Exception as e:
            return f"❌ Calculation error: {str(e)}"
    
    def get_current_time(self) -> str:
        """
        Get current time.
        
        Returns:
            str: Current time
        """
        now = datetime.now()
        return f"⏰ Current time: {now.strftime('%I:%M %p on %A, %B %d, %Y')}"
    
    def get_current_date(self) -> str:
        """
        Get current date.
        
        Returns:
            str: Current date
        """
        now = datetime.now()
        return f"📅 Today is {now.strftime('%A, %B %d, %Y')}"
    
    def set_timer(self, seconds: int, message: str = "Timer finished!") -> str:
        """
        Set a timer.
        
        Args:
            seconds: Timer duration in seconds
            message: Message to display when timer finishes
            
        Returns:
            str: Status message
        """
        def timer_thread():
            time.sleep(seconds)
            print(f"⏰ TIMER: {message}")
        
        thread = threading.Thread(target=timer_thread, daemon=True)
        thread.start()
        
        return f"⏰ Timer set for {seconds} seconds: {message}"

# Convenience functions for backward compatibility
def run_automation():
    """Run automation demo."""
    automation = JarvisAutomation()
    print("🤖 JARVIS Automation System Online")
    print(automation.get_system_info())

if __name__ == "__main__":
    # Test automation functionality
    automation = JarvisAutomation()
    
    print("Testing JARVIS Automation...")
    
    # Test system info
    print("\n1. System Information:")
    print(automation.get_system_info())
    
    # Test calculations
    print("\n2. Calculator Test:")
    print(automation.calculate("2 + 2"))
    print(automation.calculate("10 * 5 + 3"))
    
    # Test time/date
    print("\n3. Time/Date Test:")
    print(automation.get_current_time())
    print(automation.get_current_date())
    
    print("\nAutomation testing complete!")