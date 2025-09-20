"""
GUI.py
Modern PyQt5 GUI for JARVIS AI Assistant with voice interaction and chat interface.
"""

import sys
import os
import threading
from datetime import datetime

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                            QLabel, QFrame, QScrollArea, QTabWidget)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

# Import JARVIS components
try:
    from Backend.Chatbot import JarvisChatbot
    from Backend.SpeechToText import JarvisSpeechToText
    from Backend.TextToSpeech import speak
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all backend modules are properly installed")

class VoiceThread(QThread):
    """Thread for handling voice input."""
    voice_command = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        try:
            self.stt = JarvisSpeechToText()
        except:
            self.stt = None
        self.listening = False
    
    def start_listening(self):
        if self.stt:
            self.listening = True
            self.start()
    
    def stop_listening(self):
        """Stop listening with better cleanup."""
        self.listening = False
        if self.stt:
            self.stt.stop_listening()
        print("🔇 Voice thread stop_listening called")
    
    def run(self):
        def voice_callback(command):
            self.voice_command.emit(command)
        
        try:
            if self.stt:
                self.stt.listen_continuous(voice_callback)
        except Exception as e:
            print(f"Voice thread error: {e}")

class ChatMessage(QFrame):
    """Custom widget for chat messages."""
    
    def __init__(self, message: str, is_user: bool = False):
        super().__init__()
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(1)
        
        # Set style based on sender
        if is_user:
            self.setStyleSheet("""
                QFrame {
                    background-color: #2196F3;
                    border: 1px solid #1976D2;
                    border-radius: 10px;
                    margin: 5px;
                    padding: 10px;
                }
                QLabel {
                    color: white;
                    background-color: transparent;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: #424242;
                    border: 1px solid #616161;
                    border-radius: 10px;
                    margin: 5px;
                    padding: 10px;
                }
                QLabel {
                    color: #E0E0E0;
                    background-color: transparent;
                }
            """)
        
        # Layout
        layout = QVBoxLayout()
        
        # Message content
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setFont(QFont("Segoe UI", 11))
        
        # Timestamp
        timestamp = datetime.now().strftime("%H:%M")
        time_label = QLabel(timestamp)
        time_label.setFont(QFont("Segoe UI", 8))
        time_label.setStyleSheet("color: #BDBDBD;")
        time_label.setAlignment(Qt.AlignRight)
        
        layout.addWidget(message_label)
        layout.addWidget(time_label)
        
        self.setLayout(layout)

class JarvisGUI(QMainWindow):
    """Main JARVIS GUI Application."""
    
    def __init__(self):
        super().__init__()
        try:
            self.jarvis = JarvisChatbot()
        except:
            self.jarvis = None
            
        self.voice_thread = None
        self.is_voice_active = False
        
        self.init_ui()
        
        # Welcome message
        if self.jarvis:
            self.add_jarvis_message("JARVIS systems online and ready to assist. How may I help you today?")
        else:
            self.add_jarvis_message("JARVIS initialization error. Please check backend modules.")
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("JARVIS - AI Assistant")
        self.setGeometry(100, 100, 1000, 700)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QTextEdit {
                background-color: #2d2d2d;
                border: 1px solid #555555;
                border-radius: 5px;
                color: #ffffff;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                padding: 10px;
            }
            QLineEdit {
                background-color: #2d2d2d;
                border: 1px solid #555555;
                border-radius: 5px;
                color: #ffffff;
                font-size: 14px;
                padding: 8px;
            }
            QPushButton {
                background-color: #0078d4;
                border: none;
                border-radius: 5px;
                color: white;
                font-size: 12px;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QLabel {
                color: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #2d2d2d;
            }
            QTabBar::tab {
                background-color: #3d3d3d;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #0078d4;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Create tabs
        self.tab_widget = QTabWidget()
        
        # Chat tab
        self.chat_tab = self.create_chat_tab()
        self.tab_widget.addTab(self.chat_tab, "💬 Chat")
        
        # System tab
        self.system_tab = self.create_system_tab()
        self.tab_widget.addTab(self.system_tab, "🖥️ System")
        
        main_layout.addWidget(self.tab_widget)
        
        # Status bar
        self.statusBar().showMessage("JARVIS Ready")
    
    def create_chat_tab(self):
        """Create the main chat interface tab."""
        chat_widget = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("🤖 JARVIS AI Assistant")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setStyleSheet("color: #0078d4; margin: 10px;")
        
        # Voice button
        self.voice_btn = QPushButton("🎤 Voice Chat")
        self.voice_btn.clicked.connect(self.toggle_voice)
        self.voice_btn.setCheckable(True)
        
        # Force stop voice button
        self.force_stop_btn = QPushButton("⛔ Force Stop Voice")
        self.force_stop_btn.clicked.connect(self.force_stop_voice)
        self.force_stop_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; }")
        
        # Clear button
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.clicked.connect(self.clear_chat)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.force_stop_btn)
        header_layout.addWidget(self.voice_btn)
        header_layout.addWidget(clear_btn)
        
        layout.addLayout(header_layout)
        
        # Chat area
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.addStretch()
        self.chat_widget.setLayout(self.chat_layout)
        
        self.chat_scroll.setWidget(self.chat_widget)
        layout.addWidget(self.chat_scroll)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message to JARVIS...")
        self.input_field.returnPressed.connect(self.send_message)
        
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(send_btn)
        
        layout.addLayout(input_layout)
        
        chat_widget.setLayout(layout)
        return chat_widget
    
    def create_system_tab(self):
        """Create system information tab."""
        system_widget = QWidget()
        layout = QVBoxLayout()
        
        # System info display
        self.system_info = QTextEdit()
        self.system_info.setReadOnly(True)
        self.system_info.setPlainText("System information will be displayed here...")
        
        # Update system info
        self.update_system_info()
        
        layout.addWidget(QLabel("System Information:"))
        layout.addWidget(self.system_info)
        
        system_widget.setLayout(layout)
        return system_widget
    
    def add_user_message(self, message: str):
        """Add user message to chat."""
        msg_widget = ChatMessage(message, is_user=True)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, msg_widget)
        self.scroll_to_bottom()
    
    def add_jarvis_message(self, message: str):
        """Add JARVIS message to chat."""
        msg_widget = ChatMessage(f"JARVIS: {message}", is_user=False)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, msg_widget)
        self.scroll_to_bottom()
    
    def scroll_to_bottom(self):
        """Scroll chat to bottom."""
        QTimer.singleShot(100, lambda: self.chat_scroll.verticalScrollBar().setValue(
            self.chat_scroll.verticalScrollBar().maximum()
        ))
    
    def send_message(self):
        """Send message to JARVIS."""
        message = self.input_field.text().strip()
        if not message:
            return
        
        self.input_field.clear()
        self.add_user_message(message)
        
        # Process message in thread to avoid blocking UI
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    def process_message(self, message: str):
        """Process message with JARVIS."""
        try:
            if self.jarvis:
                response = self.jarvis.respond(message, use_voice=False)
            else:
                response = "JARVIS backend not available. Please check configuration."
            QTimer.singleShot(0, lambda: self.add_jarvis_message(response))
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            QTimer.singleShot(0, lambda: self.add_jarvis_message(error_msg))
    
    def toggle_voice(self):
        """Toggle voice chat on/off."""
        if not self.is_voice_active:
            self.start_voice_chat()
        else:
            self.stop_voice_chat()
    
    def start_voice_chat(self):
        """Start voice chat."""
        try:
            self.voice_thread = VoiceThread()
            if self.voice_thread.stt:
                self.voice_thread.voice_command.connect(self.handle_voice_command)
                self.voice_thread.start_listening()
                
                self.is_voice_active = True
                self.voice_btn.setText("🔴 Stop Voice")
                self.statusBar().showMessage("Voice chat active")
                
                self.add_jarvis_message("Voice chat activated. Say 'JARVIS' followed by your command.")
            else:
                self.add_jarvis_message("Voice chat not available. Please check speech recognition setup.")
            
        except Exception as e:
            self.add_jarvis_message(f"Voice chat error: {str(e)}")
    
    def stop_voice_chat(self):
        """Stop voice chat with improved cleanup."""
        try:
            if self.voice_thread:
                print("🔇 Stopping voice thread...")
                self.voice_thread.stop_listening()
                
                # Wait for thread to finish with timeout
                if not self.voice_thread.wait(3000):  # 3 second timeout
                    print("⚠️ Voice thread didn't stop gracefully, terminating...")
                    self.voice_thread.terminate()
                    self.voice_thread.wait(1000)  # Wait 1 more second
                
                self.voice_thread = None
                print("✅ Voice thread stopped successfully")
        
        except Exception as e:
            print(f"Error stopping voice thread: {e}")
        
        self.is_voice_active = False
        self.voice_btn.setText("🎤 Voice Chat")
        self.voice_btn.setChecked(False)
        self.statusBar().showMessage("Voice chat stopped")
        
        self.add_jarvis_message("🔇 Voice chat deactivated - you can now control voice properly.")
    
    def force_stop_voice(self):
        """Force stop voice system - emergency stop."""
        print("⛔ FORCE STOPPING VOICE SYSTEM")
        
        try:
            # Force terminate voice thread
            if self.voice_thread:
                self.voice_thread.listening = False
                if self.voice_thread.stt:
                    self.voice_thread.stt.is_listening = False
                
                # Terminate thread forcefully
                self.voice_thread.terminate()
                self.voice_thread.wait(1000)
                self.voice_thread = None
                print("✅ Voice thread force terminated")
            
            # Reset all voice states
            self.is_voice_active = False
            self.voice_btn.setText("🎤 Voice Chat")
            self.voice_btn.setChecked(False)
            self.statusBar().showMessage("Voice system force stopped")
            
            self.add_jarvis_message("⛔ Voice system FORCE STOPPED! You can now use JARVIS normally.")
            
        except Exception as e:
            print(f"Force stop error: {e}")
            self.add_jarvis_message(f"⛔ Force stop attempted. Error: {e}")
    
    def handle_voice_command(self, command: str):
        """Handle voice command from speech recognition with better processing."""
        print(f"🎤 Voice command received: '{command}'")
        
        # Add command to GUI chat
        self.add_user_message(f"🎤 Voice: {command}")
        
        # Update status
        self.statusBar().showMessage(f"Processing voice command: {command}")
        
        # Process with JARVIS
        threading.Thread(target=self.process_voice_command, args=(command,), daemon=True).start()
    
    def process_voice_command(self, command: str):
        """Process voice command with JARVIS."""
        try:
            if self.jarvis:
                response = self.jarvis.respond(command, use_voice=True)
            else:
                response = "JARVIS backend not available."
            QTimer.singleShot(0, lambda: self.add_jarvis_message(response))
        except Exception as e:
            error_msg = f"Voice command error: {str(e)}"
            QTimer.singleShot(0, lambda: self.add_jarvis_message(error_msg))
    
    def clear_chat(self):
        """Clear chat history."""
        # Remove all message widgets except the stretch
        while self.chat_layout.count() > 1:
            child = self.chat_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Reset JARVIS memory
        if self.jarvis:
            self.jarvis.reset_memory()
        self.add_jarvis_message("Chat cleared. Memory reset.")
    
    def update_system_info(self):
        """Update system information display."""
        try:
            if self.jarvis and hasattr(self.jarvis, 'automation'):
                system_info = self.jarvis.automation.get_system_info()
                self.system_info.setPlainText(system_info)
            else:
                self.system_info.setPlainText("System information not available.")
        except Exception as e:
            self.system_info.setPlainText(f"Error getting system info: {str(e)}")
    
    def closeEvent(self, event):
        """Handle GUI close event with voice cleanup."""
        print("🔄 Closing JARVIS GUI...")
        
        # Force stop voice if active
        if self.is_voice_active:
            print("🔇 Force stopping voice on GUI close...")
            self.force_stop_voice()
        
        # Accept the close event
        event.accept()
        print("✅ JARVIS GUI closed successfully")

def start_gui():
    """Start the JARVIS GUI application."""
    app = QApplication(sys.argv)
    app.setApplicationName("JARVIS")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = JarvisGUI()
    window.show()
    
    # Start event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    start_gui()
