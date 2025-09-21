"""
ModernGUI.py
Modern, sleek GUI interface inspired by Neural Chat AI design.
Features: Sidebar navigation, modern chat bubbles, gradients, and professional styling.
"""

import sys
import os
import json
import time
import threading
from datetime import datetime
from typing import Optional, List, Dict, Any

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QTextEdit, QLineEdit, QPushButton, QFrame, QScrollArea,
    QSplitter, QStackedWidget, QSizePolicy, QSpacerItem, QProgressBar,
    QMenu, QAction, QMessageBox, QFileDialog, QInputDialog
)
from PyQt5.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation, 
    QEasingCurve, QRect, QSize, pyqtProperty
)
from PyQt5.QtGui import (
    QFont, QPixmap, QPainter, QColor, QLinearGradient, 
    QBrush, QPen, QIcon, QPalette, QCursor
)

# Import JARVIS components
try:
    from Backend.Chatbot import JarvisChatbot
    from Backend.TextToSpeech import speak
    from Backend.SpeechToText import JarvisSpeechToText
    JARVIS_AVAILABLE = True
except ImportError:
    JARVIS_AVAILABLE = False
    print("⚠️ JARVIS components not available")

class MessageBubble(QFrame):
    """Modern message bubble with gradient styling."""
    
    def __init__(self, message: str, is_user: bool = False, timestamp: str = ""):
        super().__init__()
        self.message = message
        self.is_user = is_user
        self.timestamp = timestamp
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the message bubble UI."""
        self.setFrameStyle(QFrame.NoFrame)
        self.setContentsMargins(10, 10, 10, 10)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Header with avatar and name
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)
        
        # Avatar
        avatar = QLabel()
        avatar.setFixedSize(32, 32)
        avatar.setStyleSheet("""
            QLabel {
                border-radius: 16px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border: 2px solid white;
            }
        """)
        
        if self.is_user:
            avatar.setStyleSheet("""
                QLabel {
                    border-radius: 16px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #f093fb, stop:1 #f5576c);
                    border: 2px solid white;
                }
            """)
        
        # Online indicator
        online_indicator = QLabel()
        online_indicator.setFixedSize(8, 8)
        online_indicator.setStyleSheet("""
            QLabel {
                border-radius: 4px;
                background-color: #4ade80;
                border: 1px solid white;
            }
        """)
        
        # Name and timestamp
        name_layout = QVBoxLayout()
        name_label = QLabel("You" if self.is_user else "JARVIS")
        name_label.setStyleSheet("""
            QLabel {
                color: #374151;
                font-weight: 600;
                font-size: 14px;
            }
        """)
        
        time_label = QLabel(self.timestamp)
        time_label.setStyleSheet("""
            QLabel {
                color: #9ca3af;
                font-size: 12px;
            }
        """)
        
        name_layout.addWidget(name_label)
        name_layout.addWidget(time_label)
        
        header_layout.addWidget(avatar)
        header_layout.addWidget(online_indicator)
        header_layout.addLayout(name_layout)
        header_layout.addStretch()
        
        # Message content
        message_label = QLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        if self.is_user:
            # User message styling
            message_label.setStyleSheet("""
                QLabel {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #667eea, stop:1 #764ba2);
                    color: white;
                    padding: 12px 16px;
                    border-radius: 18px;
                    font-size: 14px;
                    font-weight: 500;
                }
            """)
        else:
            # AI message styling
            message_label.setStyleSheet("""
                QLabel {
                    background-color: white;
                    color: #374151;
                    padding: 12px 16px;
                    border-radius: 18px;
                    font-size: 14px;
                    border: 1px solid #e5e7eb;
                }
            """)
        
        # Action buttons for AI messages
        if not self.is_user:
            actions_layout = QHBoxLayout()
            actions_layout.setSpacing(8)
            
            # Action buttons
            buttons = [
                ("👍", "thumbs_up"),
                ("👎", "thumbs_down"), 
                ("📋", "copy"),
                ("🔄", "regenerate")
            ]
            
            for icon, action in buttons:
                btn = QPushButton(icon)
                btn.setFixedSize(28, 28)
                btn.setStyleSheet("""
                    QPushButton {
                        border: none;
                        border-radius: 14px;
                        background-color: #f3f4f6;
                        color: #6b7280;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #e5e7eb;
                        color: #374151;
                    }
                """)
                btn.clicked.connect(lambda checked, a=action: self.on_action_clicked(a))
                actions_layout.addWidget(btn)
            
            actions_layout.addStretch()
            layout.addLayout(actions_layout)
        
        layout.addLayout(header_layout)
        layout.addWidget(message_label)
        
        self.setLayout(layout)
    
    def on_action_clicked(self, action: str):
        """Handle action button clicks."""
        if action == "copy":
            QApplication.clipboard().setText(self.message)
        elif action == "regenerate":
            # Emit signal for message regeneration
            pass
        # Add other action handlers as needed

class ConversationSidebar(QWidget):
    """Left sidebar with conversations and user profile."""
    
    def __init__(self):
        super().__init__()
        self.conversations = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the sidebar UI."""
        self.setFixedWidth(280)
        self.setStyleSheet("""
            QWidget {
                background-color: #f9fafb;
                border-right: 1px solid #e5e7eb;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        # Logo
        logo_label = QLabel("🤖")
        logo_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 12px;
                padding: 8px;
                color: white;
            }
        """)
        
        title_label = QLabel("Neural JARVIS")
        title_label.setStyleSheet("""
            QLabel {
                color: #374151;
                font-size: 18px;
                font-weight: 700;
            }
        """)
        
        subtitle_label = QLabel("Powered by Groq")
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #6b7280;
                font-size: 12px;
            }
        """)
        
        header_layout.addWidget(logo_label)
        header_layout.addStretch()
        
        # Status indicators
        status_layout = QVBoxLayout()
        
        # Online status
        online_layout = QHBoxLayout()
        online_dot = QLabel("●")
        online_dot.setStyleSheet("color: #4ade80; font-size: 12px;")
        online_text = QLabel("Online")
        online_text.setStyleSheet("color: #6b7280; font-size: 12px;")
        online_layout.addWidget(online_dot)
        online_layout.addWidget(online_text)
        
        # Message count
        msg_layout = QHBoxLayout()
        msg_icon = QLabel("💬")
        msg_text = QLabel("4 msgs")
        msg_text.setStyleSheet("color: #6b7280; font-size: 12px;")
        msg_layout.addWidget(msg_icon)
        msg_layout.addWidget(msg_text)
        
        status_layout.addLayout(online_layout)
        status_layout.addLayout(msg_layout)
        
        header_layout.addLayout(status_layout)
        
        # Conversations section
        conversations_label = QLabel("Conversations")
        conversations_label.setStyleSheet("""
            QLabel {
                color: #374151;
                font-size: 16px;
                font-weight: 600;
                margin-top: 10px;
            }
        """)
        
        # New chat button
        new_chat_btn = QPushButton("+ New Chat")
        new_chat_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 16px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a67d8, stop:1 #6b46c1);
            }
        """)
        new_chat_btn.clicked.connect(self.new_chat)
        
        # Current chat
        current_chat = QFrame()
        current_chat.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        current_chat_layout = QHBoxLayout()
        current_chat_layout.setContentsMargins(8, 8, 8, 8)
        
        current_icon = QLabel("🎯")
        current_text = QLabel("Active conversation\nwith 4 messages")
        current_text.setStyleSheet("color: #374151; font-size: 14px;")
        current_text.setWordWrap(True)
        
        current_chat_layout.addWidget(current_icon)
        current_chat_layout.addWidget(current_text)
        current_chat.setLayout(current_chat_layout)
        
        # Previous chats
        prev_chat = QFrame()
        prev_chat.setStyleSheet("""
            QFrame {
                background-color: #f3f4f6;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        prev_chat_layout = QHBoxLayout()
        prev_chat_layout.setContentsMargins(8, 8, 8, 8)
        
        prev_icon = QLabel("📄")
        prev_text = QLabel("Code review\ndiscussion...")
        prev_text.setStyleSheet("color: #6b7280; font-size: 14px;")
        prev_text.setWordWrap(True)
        
        prev_chat_layout.addWidget(prev_icon)
        prev_chat_layout.addWidget(prev_text)
        prev_chat.setLayout(prev_chat_layout)
        
        # User profile section
        profile_frame = QFrame()
        profile_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                padding: 16px;
            }
        """)
        profile_layout = QVBoxLayout()
        profile_layout.setContentsMargins(0, 0, 0, 0)
        profile_layout.setSpacing(12)
        
        # User avatar and info
        user_layout = QHBoxLayout()
        user_layout.setSpacing(12)
        
        user_avatar = QLabel()
        user_avatar.setFixedSize(40, 40)
        user_avatar.setStyleSheet("""
            QLabel {
                border-radius: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f093fb, stop:1 #f5576c);
                border: 2px solid white;
            }
        """)
        
        user_info = QVBoxLayout()
        user_name = QLabel("John Doe")
        user_name.setStyleSheet("color: #374151; font-weight: 600; font-size: 14px;")
        user_email = QLabel("john.doe@example.com")
        user_email.setStyleSheet("color: #6b7280; font-size: 12px;")
        
        user_info.addWidget(user_name)
        user_info.addWidget(user_email)
        
        user_layout.addWidget(user_avatar)
        user_layout.addLayout(user_info)
        user_layout.addStretch()
        
        # Online indicator
        user_online = QLabel("●")
        user_online.setStyleSheet("color: #4ade80; font-size: 12px;")
        user_layout.addWidget(user_online)
        
        # Usage today
        usage_label = QLabel("Usage Today")
        usage_label.setStyleSheet("color: #6b7280; font-size: 12px;")
        
        usage_bar = QProgressBar()
        usage_bar.setRange(0, 100)
        usage_bar.setValue(4)
        usage_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #e5e7eb;
                height: 8px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #1d4ed8);
                border-radius: 4px;
            }
        """)
        
        usage_text = QLabel("4/100")
        usage_text.setStyleSheet("color: #6b7280; font-size: 12px;")
        
        usage_layout = QHBoxLayout()
        usage_layout.addWidget(usage_bar)
        usage_layout.addWidget(usage_text)
        
        profile_layout.addLayout(user_layout)
        profile_layout.addWidget(usage_label)
        profile_layout.addLayout(usage_layout)
        
        profile_frame.setLayout(profile_layout)
        
        # Add all components to main layout
        layout.addLayout(header_layout)
        layout.addWidget(conversations_label)
        layout.addWidget(new_chat_btn)
        layout.addWidget(current_chat)
        layout.addWidget(prev_chat)
        layout.addStretch()
        layout.addWidget(profile_frame)
        
        self.setLayout(layout)
    
    def new_chat(self):
        """Start a new chat conversation."""
        print("Starting new chat...")

class ChatArea(QWidget):
    """Main chat area with modern message display."""
    
    def __init__(self):
        super().__init__()
        self.messages = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the chat area UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(0)
        
        # Header bar
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 20)
        
        # Settings and model info
        settings_layout = QHBoxLayout()
        
        # Model selector
        model_btn = QPushButton("🧠 Gemini Pro ▼")
        model_btn.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 8px 12px;
                color: #374151;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e5e7eb;
            }
        """)
        
        # Premium star
        star_btn = QPushButton("⭐")
        star_btn.setStyleSheet("""
            QPushButton {
                background: none;
                border: none;
                font-size: 16px;
                color: #f59e0b;
            }
        """)
        
        # Settings gear
        settings_btn = QPushButton("⚙️")
        settings_btn.setStyleSheet("""
            QPushButton {
                background: none;
                border: none;
                font-size: 16px;
                color: #6b7280;
            }
            QPushButton:hover {
                color: #374151;
            }
        """)
        
        settings_layout.addWidget(model_btn)
        settings_layout.addWidget(star_btn)
        settings_layout.addWidget(settings_btn)
        settings_layout.addStretch()
        
        header_layout.addLayout(settings_layout)
        
        # Scrollable messages area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #f3f4f6;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #d1d5db;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #9ca3af;
            }
        """)
        
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout()
        self.messages_layout.setContentsMargins(0, 0, 0, 0)
        self.messages_layout.setSpacing(16)
        self.messages_widget.setLayout(self.messages_layout)
        
        self.scroll_area.setWidget(self.messages_widget)
        
        # Add sample messages
        self.add_sample_messages()
        
        layout.addLayout(header_layout)
        layout.addWidget(self.scroll_area)
        
        self.setLayout(layout)
    
    def add_sample_messages(self):
        """Add sample messages to demonstrate the interface."""
        current_time = datetime.now().strftime("%H:%M")
        
        # AI message
        ai_message = MessageBubble(
            "Nice to meet you, vijay! Is there anything I can help you with today?",
            is_user=False,
            timestamp=current_time
        )
        self.messages_layout.addWidget(ai_message)
        
        # User message
        user_message = MessageBubble(
            "What is my name?",
            is_user=True,
            timestamp=current_time
        )
        self.messages_layout.addWidget(user_message)
        
        # AI response
        ai_response = MessageBubble(
            "Your name is vijay.",
            is_user=False,
            timestamp=current_time
        )
        self.messages_layout.addWidget(ai_response)
        
        # Add spacer to push messages to top
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.messages_layout.addItem(spacer)
    
    def add_message(self, message: str, is_user: bool = False):
        """Add a new message to the chat."""
        current_time = datetime.now().strftime("%H:%M")
        
        message_bubble = MessageBubble(
            message,
            is_user=is_user,
            timestamp=current_time
        )
        
        # Remove spacer if it exists
        if self.messages_layout.count() > 0:
            item = self.messages_layout.itemAt(self.messages_layout.count() - 1)
            if isinstance(item, QSpacerItem):
                self.messages_layout.removeItem(item)
        
        self.messages_layout.addWidget(message_bubble)
        
        # Add spacer back
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.messages_layout.addItem(spacer)
        
        # Scroll to bottom
        QTimer.singleShot(100, self.scroll_to_bottom)
    
    def scroll_to_bottom(self):
        """Scroll to the bottom of the chat."""
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

class InputArea(QWidget):
    """Modern input area with quick actions and voice controls."""
    
    message_sent = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the input area UI."""
        self.setFixedHeight(120)
        self.setStyleSheet("""
            QWidget {
                background-color: #f9fafb;
                border-top: 1px solid #e5e7eb;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        
        # Main input area
        input_layout = QHBoxLayout()
        input_layout.setSpacing(12)
        
        # Text input
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Type your message...")
        self.text_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                padding: 12px 16px;
                font-size: 14px;
                color: #374151;
            }
            QLineEdit:focus {
                border-color: #667eea;
                outline: none;
            }
        """)
        self.text_input.returnPressed.connect(self.send_message)
        
        # Sparkle icon
        sparkle_label = QLabel("✨")
        sparkle_label.setStyleSheet("font-size: 16px; color: #f59e0b;")
        
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(sparkle_label)
        
        # Quick actions
        actions_label = QLabel("Quick actions:")
        actions_label.setStyleSheet("color: #6b7280; font-size: 12px;")
        
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)
        
        quick_actions = [
            ("💡", "Explain"),
            ("🔍", "Analyze"), 
            ("✨", "Help")
        ]
        
        for icon, text in quick_actions:
            btn = QPushButton(f"{icon} {text}")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 1px solid #e5e7eb;
                    border-radius: 8px;
                    padding: 8px 12px;
                    color: #374151;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #f3f4f6;
                    border-color: #d1d5db;
                }
            """)
            btn.clicked.connect(lambda checked, t=text: self.on_quick_action(t))
            actions_layout.addWidget(btn)
        
        actions_layout.addStretch()
        
        # Character count and controls
        controls_layout = QHBoxLayout()
        
        char_count = QLabel("0/2000")
        char_count.setStyleSheet("color: #6b7280; font-size: 12px;")
        
        # Voice button
        voice_btn = QPushButton("🎤")
        voice_btn.setFixedSize(40, 40)
        voice_btn.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                border: 1px solid #e5e7eb;
                border-radius: 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #e5e7eb;
            }
        """)
        voice_btn.clicked.connect(self.toggle_voice)
        
        # Send button
        send_btn = QPushButton("🚀")
        send_btn.setFixedSize(40, 40)
        send_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border: none;
                border-radius: 20px;
                font-size: 16px;
                color: white;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a67d8, stop:1 #6b46c1);
            }
        """)
        send_btn.clicked.connect(self.send_message)
        
        controls_layout.addWidget(char_count)
        controls_layout.addStretch()
        controls_layout.addWidget(voice_btn)
        controls_layout.addWidget(send_btn)
        
        layout.addLayout(input_layout)
        layout.addWidget(actions_label)
        layout.addLayout(actions_layout)
        layout.addLayout(controls_layout)
        
        self.setLayout(layout)
    
    def send_message(self):
        """Send the current message."""
        message = self.text_input.text().strip()
        if message:
            self.message_sent.emit(message)
            self.text_input.clear()
    
    def on_quick_action(self, action: str):
        """Handle quick action button clicks."""
        quick_messages = {
            "Explain": "Can you explain this in simple terms?",
            "Analyze": "Please analyze this and provide insights.",
            "Help": "I need help with this."
        }
        
        if action in quick_messages:
            self.text_input.setText(quick_messages[action])
            self.text_input.setFocus()
    
    def toggle_voice(self):
        """Toggle voice input."""
        print("Voice input toggled...")

class ModernJarvisGUI(QMainWindow):
    """Modern JARVIS GUI with sleek design inspired by Neural Chat AI."""
    
    def __init__(self):
        super().__init__()
        self.chatbot = None
        self.setup_ui()
        self.initialize_jarvis()
    
    def setup_ui(self):
        """Setup the main UI."""
        self.setWindowTitle("Neural JARVIS - AI Assistant")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 800)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create components
        self.sidebar = ConversationSidebar()
        self.chat_area = ChatArea()
        self.input_area = InputArea()
        
        # Chat and input layout
        chat_layout = QVBoxLayout()
        chat_layout.setContentsMargins(0, 0, 0, 0)
        chat_layout.setSpacing(0)
        
        chat_layout.addWidget(self.chat_area)
        chat_layout.addWidget(self.input_area)
        
        # Add to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addLayout(chat_layout)
        
        central_widget.setLayout(main_layout)
        
        # Connect signals
        self.input_area.message_sent.connect(self.handle_user_message)
        
        # Apply modern styling
        self.apply_modern_styling()
    
    def apply_modern_styling(self):
        """Apply modern styling and effects."""
        # Set window properties for modern look
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        
        # Add subtle shadow effect (simulated with border)
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
                border: 1px solid #e5e7eb;
            }
        """)
    
    def initialize_jarvis(self):
        """Initialize JARVIS chatbot."""
        if JARVIS_AVAILABLE:
            try:
                self.chatbot = JarvisChatbot()
                print("✅ JARVIS initialized successfully")
            except Exception as e:
                print(f"❌ Failed to initialize JARVIS: {e}")
                self.show_error("JARVIS Initialization Error", 
                               f"Failed to initialize JARVIS: {str(e)}")
        else:
            self.show_error("Missing Dependencies", 
                           "JARVIS backend components are not available.")
    
    def handle_user_message(self, message: str):
        """Handle user message and get JARVIS response."""
        if not self.chatbot:
            self.chat_area.add_message("JARVIS is not available. Please check the backend.", is_user=False)
            return
        
        # Add user message to chat
        self.chat_area.add_message(message, is_user=True)
        
        # Get JARVIS response
        try:
            response = self.chatbot.respond(message)
            self.chat_area.add_message(response, is_user=False)
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.chat_area.add_message(error_msg, is_user=False)
    
    def show_error(self, title: str, message: str):
        """Show error dialog."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

def main():
    """Main function to run the modern GUI."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Neural JARVIS")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("JARVIS AI")
    
    # Create and show main window
    window = ModernJarvisGUI()
    window.show()
    
    # Run application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
