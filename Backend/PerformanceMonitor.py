"""
PerformanceMonitor.py
Real-time performance monitoring GUI component for JARVIS.
"""

import sys
import time
import threading
from typing import Dict, Any, Optional
from datetime import datetime

try:
    from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                                QProgressBar, QPushButton, QTextEdit, QTabWidget,
                                QGridLayout, QFrame)
    from PyQt5.QtCore import QTimer, pyqtSignal, QThread
    from PyQt5.QtGui import QFont, QPalette, QColor
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("⚠️ PyQt5 not available for performance monitoring")

class PerformanceMonitor(QWidget):
    """Real-time performance monitoring widget."""
    
    def __init__(self, jarvis_chatbot=None):
        super().__init__()
        self.jarvis = jarvis_chatbot
        self.update_interval = 2000  # Update every 2 seconds
        
        self.setWindowTitle("JARVIS Performance Monitor")
        self.setGeometry(100, 100, 800, 600)
        
        self.init_ui()
        self.start_monitoring()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("🔧 JARVIS Performance Monitor")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #0078d4; margin: 10px;")
        layout.addWidget(title)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Performance Stats Tab
        self.stats_tab = self.create_stats_tab()
        self.tab_widget.addTab(self.stats_tab, "📊 Performance")
        
        # Cache Info Tab
        self.cache_tab = self.create_cache_tab()
        self.tab_widget.addTab(self.cache_tab, "🚀 Cache")
        
        # Error Log Tab
        self.error_tab = self.create_error_tab()
        self.tab_widget.addTab(self.error_tab, "❌ Errors")
        
        layout.addWidget(self.tab_widget)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.optimize_btn = QPushButton("🧹 Optimize System")
        self.optimize_btn.clicked.connect(self.optimize_system)
        self.optimize_btn.setStyleSheet("QPushButton { background-color: #28a745; color: white; padding: 8px; }")
        
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.refresh_data)
        self.refresh_btn.setStyleSheet("QPushButton { background-color: #0078d4; color: white; padding: 8px; }")
        
        self.close_btn = QPushButton("❌ Close")
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setStyleSheet("QPushButton { background-color: #dc3545; color: white; padding: 8px; }")
        
        button_layout.addWidget(self.optimize_btn)
        button_layout.addWidget(self.refresh_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def create_stats_tab(self):
        """Create performance statistics tab."""
        widget = QWidget()
        layout = QGridLayout()
        
        # Performance metrics
        self.cache_hit_rate_label = QLabel("Cache Hit Rate: 0%")
        self.cache_size_label = QLabel("Cache Size: 0 items")
        self.memory_usage_label = QLabel("Memory Usage: 0 MB")
        self.response_time_label = QLabel("Avg Response Time: 0s")
        self.total_requests_label = QLabel("Total Requests: 0")
        self.error_count_label = QLabel("Error Count: 0")
        
        # Progress bars
        self.cache_hit_bar = QProgressBar()
        self.cache_hit_bar.setRange(0, 100)
        self.cache_hit_bar.setValue(0)
        
        self.memory_bar = QProgressBar()
        self.memory_bar.setRange(0, 1000)  # Up to 1GB
        self.memory_bar.setValue(0)
        
        # Layout
        layout.addWidget(QLabel("🚀 Cache Performance"), 0, 0, 1, 2)
        layout.addWidget(self.cache_hit_rate_label, 1, 0)
        layout.addWidget(self.cache_hit_bar, 1, 1)
        layout.addWidget(self.cache_size_label, 2, 0, 1, 2)
        
        layout.addWidget(QLabel("💾 Memory Usage"), 3, 0, 1, 2)
        layout.addWidget(self.memory_usage_label, 4, 0)
        layout.addWidget(self.memory_bar, 4, 1)
        
        layout.addWidget(QLabel("⚡ Response Times"), 5, 0, 1, 2)
        layout.addWidget(self.response_time_label, 6, 0, 1, 2)
        layout.addWidget(self.total_requests_label, 7, 0, 1, 2)
        
        layout.addWidget(QLabel("🔧 System Health"), 8, 0, 1, 2)
        layout.addWidget(self.error_count_label, 9, 0, 1, 2)
        
        widget.setLayout(layout)
        return widget
    
    def create_cache_tab(self):
        """Create cache information tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.cache_info = QTextEdit()
        self.cache_info.setReadOnly(True)
        self.cache_info.setFont(QFont("Consolas", 9))
        
        layout.addWidget(QLabel("🚀 Cache Information"))
        layout.addWidget(self.cache_info)
        
        widget.setLayout(layout)
        return widget
    
    def create_error_tab(self):
        """Create error log tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.error_log = QTextEdit()
        self.error_log.setReadOnly(True)
        self.error_log.setFont(QFont("Consolas", 9))
        
        layout.addWidget(QLabel("❌ Error Log"))
        layout.addWidget(self.error_log)
        
        widget.setLayout(layout)
        return widget
    
    def start_monitoring(self):
        """Start the monitoring timer."""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(self.update_interval)
        
        # Initial update
        self.update_stats()
    
    def update_stats(self):
        """Update performance statistics."""
        if not self.jarvis or not self.jarvis.optimizer:
            return
        
        try:
            stats = self.jarvis.optimizer.get_performance_stats()
            
            # Update performance stats
            cache_hit_rate = stats.get('cache_hit_rate', 0)
            self.cache_hit_rate_label.setText(f"Cache Hit Rate: {cache_hit_rate}%")
            self.cache_hit_bar.setValue(int(cache_hit_rate))
            
            self.cache_size_label.setText(f"Cache Size: {stats.get('cache_size', 0)} items")
            
            memory_mb = stats.get('current_memory_mb', 0)
            self.memory_usage_label.setText(f"Memory Usage: {memory_mb:.1f} MB")
            self.memory_bar.setValue(min(int(memory_mb), 1000))
            
            self.response_time_label.setText(f"Avg Response Time: {stats.get('avg_api_time', 0):.3f}s")
            self.total_requests_label.setText(f"Total Requests: {stats.get('total_requests', 0)}")
            self.error_count_label.setText(f"Error Count: {stats.get('error_count', 0)}")
            
            # Update cache info
            cache_info = f"""Cache Statistics:
• Hit Rate: {cache_hit_rate}%
• Cache Size: {stats.get('cache_size', 0)} items
• Cache Memory: {stats.get('cache_memory_mb', 0):.2f} MB
• Background Tasks: {stats.get('background_tasks', 0)}

Last Updated: {datetime.now().strftime('%H:%M:%S')}
"""
            self.cache_info.setText(cache_info)
            
            # Update error log
            if self.jarvis.error_handler:
                error_stats = self.jarvis.error_handler.get_error_stats()
                error_log = f"""Error Statistics:
• Total Errors: {error_stats.get('total_errors', 0)}
• Unique Errors: {error_stats.get('unique_errors', 0)}
• Recovery Attempts: {error_stats.get('recovery_attempts', 0)}

Top Errors:
"""
                for error, count in error_stats.get('top_errors', [])[:5]:
                    error_log += f"• {error}: {count} times\n"
                
                error_log += f"\nLast Updated: {datetime.now().strftime('%H:%M:%S')}"
                self.error_log.setText(error_log)
            
        except Exception as e:
            print(f"⚠️ Performance monitor update error: {e}")
    
    def refresh_data(self):
        """Manually refresh all data."""
        self.update_stats()
    
    def optimize_system(self):
        """Optimize system performance."""
        if self.jarvis:
            result = self.jarvis.optimize_system()
            print(result)
            self.refresh_data()
    
    def closeEvent(self, event):
        """Handle close event."""
        if hasattr(self, 'timer'):
            self.timer.stop()
        event.accept()

def show_performance_monitor(jarvis_chatbot):
    """Show the performance monitor window."""
    if not GUI_AVAILABLE:
        print("❌ Performance monitor requires PyQt5")
        return None
    
    try:
        monitor = PerformanceMonitor(jarvis_chatbot)
        monitor.show()
        return monitor
    except Exception as e:
        print(f"❌ Failed to create performance monitor: {e}")
        return None

if __name__ == "__main__":
    if GUI_AVAILABLE:
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        monitor = PerformanceMonitor()
        monitor.show()
        sys.exit(app.exec_())
    else:
        print("❌ PyQt5 not available")
