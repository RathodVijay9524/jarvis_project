"""
SystemMonitorService.py
System monitoring and alerts service for JARVIS.
"""

import os
import json
import time
import threading
import psutil
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import subprocess
import platform

class JarvisSystemMonitorService:
    """
    System monitoring service with:
    - CPU, memory, and disk monitoring
    - System alerts and notifications
    - Performance tracking
    - System information
    - Process monitoring
    - Network monitoring
    """
    
    def __init__(self, data_dir: str = "Data/system"):
        self.data_dir = data_dir
        self.alerts_file = os.path.join(data_dir, "alerts.json")
        self.metrics_file = os.path.join(data_dir, "metrics.json")
        self.settings_file = os.path.join(data_dir, "settings.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Load existing data
        self.alerts = self._load_alerts()
        self.metrics_history = self._load_metrics()
        self.settings = self._load_settings()
        
        # Monitoring state
        self.monitoring = False
        self.monitor_thread = None
        
        # Alert thresholds (default values)
        self.thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'disk_percent': 90.0,
            'temperature': 80.0,  # Celsius
            'network_latency': 1000.0,  # milliseconds
        }
        
        # Update thresholds from settings
        if 'thresholds' in self.settings:
            self.thresholds.update(self.settings['thresholds'])
    
    def _load_alerts(self) -> List[Dict[str, Any]]:
        """Load alerts from file."""
        try:
            if os.path.exists(self.alerts_file):
                with open(self.alerts_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"⚠️ Error loading alerts: {e}")
            return []
    
    def _save_alerts(self):
        """Save alerts to file."""
        try:
            with open(self.alerts_file, 'w') as f:
                json.dump(self.alerts, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving alerts: {e}")
    
    def _load_metrics(self) -> List[Dict[str, Any]]:
        """Load metrics history from file."""
        try:
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"⚠️ Error loading metrics: {e}")
            return []
    
    def _save_metrics(self):
        """Save metrics history to file."""
        try:
            # Keep only last 1000 entries
            if len(self.metrics_history) > 1000:
                self.metrics_history = self.metrics_history[-1000:]
            
            with open(self.metrics_file, 'w') as f:
                json.dump(self.metrics_history, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving metrics: {e}")
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"⚠️ Error loading settings: {e}")
            return {}
    
    def _save_settings(self):
        """Save settings to file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving settings: {e}")
    
    def get_system_info(self) -> str:
        """Get comprehensive system information."""
        try:
            response = "💻 **System Information**\n\n"
            
            # Basic system info
            response += "🖥️ **Operating System:**\n"
            response += f"   • System: {platform.system()} {platform.release()}\n"
            response += f"   • Version: {platform.version()}\n"
            response += f"   • Architecture: {platform.machine()}\n"
            response += f"   • Processor: {platform.processor()}\n\n"
            
            # CPU information
            cpu_count = psutil.cpu_count()
            cpu_percent = psutil.cpu_percent(interval=1)
            response += f"⚡ **CPU:**\n"
            response += f"   • Cores: {cpu_count} (Physical: {psutil.cpu_count(logical=False)})\n"
            response += f"   • Usage: {cpu_percent:.1f}%\n"
            response += f"   • Frequency: {psutil.cpu_freq().current:.0f} MHz\n\n"
            
            # Memory information
            memory = psutil.virtual_memory()
            response += f"🧠 **Memory:**\n"
            response += f"   • Total: {memory.total / (1024**3):.1f} GB\n"
            response += f"   • Available: {memory.available / (1024**3):.1f} GB\n"
            response += f"   • Used: {memory.used / (1024**3):.1f} GB ({memory.percent:.1f}%)\n"
            response += f"   • Free: {memory.free / (1024**3):.1f} GB\n\n"
            
            # Disk information
            response += f"💾 **Disk Usage:**\n"
            for partition in psutil.disk_partitions():
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    total_gb = partition_usage.total / (1024**3)
                    used_gb = partition_usage.used / (1024**3)
                    free_gb = partition_usage.free / (1024**3)
                    percent = (used_gb / total_gb) * 100
                    
                    response += f"   • {partition.device} ({partition.mountpoint}):\n"
                    response += f"     Used: {used_gb:.1f} GB / {total_gb:.1f} GB ({percent:.1f}%)\n"
                    response += f"     Free: {free_gb:.1f} GB\n"
                except PermissionError:
                    continue
            response += "\n"
            
            # Network information
            response += f"🌐 **Network:**\n"
            network_io = psutil.net_io_counters()
            response += f"   • Bytes Sent: {network_io.bytes_sent / (1024**2):.1f} MB\n"
            response += f"   • Bytes Received: {network_io.bytes_recv / (1024**2):.1f} MB\n"
            response += f"   • Packets Sent: {network_io.packets_sent:,}\n"
            response += f"   • Packets Received: {network_io.packets_recv:,}\n\n"
            
            # Boot time
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            response += f"⏰ **System Uptime:**\n"
            response += f"   • Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            response += f"   • Uptime: {uptime.days} days, {uptime.seconds // 3600} hours\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting system info: {str(e)}"
    
    def get_current_metrics(self) -> str:
        """Get current system metrics."""
        try:
            # Get current metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            response = "📊 **Current System Metrics**\n\n"
            response += f"⚡ **CPU Usage:** {cpu_percent:.1f}%\n"
            response += f"🧠 **Memory Usage:** {memory.percent:.1f}% ({memory.used / (1024**3):.1f} GB)\n"
            
            # Disk usage for main partition
            disk_usage = psutil.disk_usage('/')
            disk_percent = (disk_usage.used / disk_usage.total) * 100
            response += f"💾 **Disk Usage:** {disk_percent:.1f}% ({disk_usage.used / (1024**3):.1f} GB)\n"
            
            # Check for alerts
            alerts = []
            if cpu_percent > self.thresholds['cpu_percent']:
                alerts.append(f"⚠️ High CPU usage: {cpu_percent:.1f}%")
            
            if memory.percent > self.thresholds['memory_percent']:
                alerts.append(f"⚠️ High memory usage: {memory.percent:.1f}%")
            
            if disk_percent > self.thresholds['disk_percent']:
                alerts.append(f"⚠️ High disk usage: {disk_percent:.1f}%")
            
            if alerts:
                response += "\n🚨 **Alerts:**\n"
                for alert in alerts:
                    response += f"   {alert}\n"
            else:
                response += "\n✅ **System Status:** All metrics within normal ranges\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting current metrics: {str(e)}"
    
    def get_top_processes(self, limit: int = 10, sort_by: str = 'cpu') -> str:
        """
        Get top processes by CPU or memory usage.
        
        Args:
            limit: Number of processes to show
            sort_by: 'cpu' or 'memory'
        """
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by specified metric
            if sort_by == 'cpu':
                processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
                metric_name = "CPU"
                metric_unit = "%"
            else:  # memory
                processes.sort(key=lambda x: x['memory_percent'] or 0, reverse=True)
                metric_name = "Memory"
                metric_unit = "%"
            
            # Get top processes
            top_processes = processes[:limit]
            
            response = f"📈 **Top {limit} Processes by {metric_name} Usage**\n\n"
            
            for i, proc in enumerate(top_processes, 1):
                name = proc['name'] or 'Unknown'
                pid = proc['pid']
                
                if sort_by == 'cpu':
                    metric_value = proc['cpu_percent'] or 0
                else:
                    metric_value = proc['memory_percent'] or 0
                
                memory_mb = (proc['memory_info'].rss / (1024**2)) if proc['memory_info'] else 0
                
                response += f"**{i}. {name}** (PID: {pid})\n"
                response += f"   {metric_name}: {metric_value:.1f}{metric_unit}\n"
                response += f"   Memory: {memory_mb:.1f} MB\n\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting top processes: {str(e)}"
    
    def start_monitoring(self, interval: int = 60) -> str:
        """
        Start continuous system monitoring.
        
        Args:
            interval: Monitoring interval in seconds
        """
        try:
            if self.monitoring:
                return "⚠️ System monitoring is already running"
            
            self.monitoring = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_system, 
                args=(interval,), 
                daemon=True
            )
            self.monitor_thread.start()
            
            return f"✅ System monitoring started (interval: {interval}s)"
            
        except Exception as e:
            return f"❌ Error starting monitoring: {str(e)}"
    
    def stop_monitoring(self) -> str:
        """Stop system monitoring."""
        try:
            self.monitoring = False
            return "✅ System monitoring stopped"
        except Exception as e:
            return f"❌ Error stopping monitoring: {str(e)}"
    
    def _monitor_system(self, interval: int):
        """Background thread for system monitoring."""
        while self.monitoring:
            try:
                # Collect metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk_usage = psutil.disk_usage('/')
                disk_percent = (disk_usage.used / disk_usage.total) * 100
                
                # Create metrics entry
                metrics_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'memory_used_gb': memory.used / (1024**3),
                    'disk_percent': disk_percent,
                    'disk_used_gb': disk_usage.used / (1024**3)
                }
                
                # Add to history
                self.metrics_history.append(metrics_entry)
                self._save_metrics()
                
                # Check for alerts
                self._check_alerts(cpu_percent, memory.percent, disk_percent)
                
                time.sleep(interval)
                
            except Exception as e:
                print(f"⚠️ Monitoring error: {e}")
                time.sleep(interval)
    
    def _check_alerts(self, cpu_percent: float, memory_percent: float, disk_percent: float):
        """Check for system alerts."""
        try:
            current_time = datetime.now()
            
            # CPU alert
            if cpu_percent > self.thresholds['cpu_percent']:
                self._create_alert('cpu', f"High CPU usage: {cpu_percent:.1f}%", current_time)
            
            # Memory alert
            if memory_percent > self.thresholds['memory_percent']:
                self._create_alert('memory', f"High memory usage: {memory_percent:.1f}%", current_time)
            
            # Disk alert
            if disk_percent > self.thresholds['disk_percent']:
                self._create_alert('disk', f"High disk usage: {disk_percent:.1f}%", current_time)
                
        except Exception as e:
            print(f"⚠️ Alert checking error: {e}")
    
    def _create_alert(self, alert_type: str, message: str, timestamp: datetime):
        """Create a new alert."""
        alert = {
            'id': len(self.alerts) + 1,
            'type': alert_type,
            'message': message,
            'timestamp': timestamp.isoformat(),
            'status': 'active'
        }
        
        self.alerts.append(alert)
        self._save_alerts()
        
        # Print alert to console
        print(f"🚨 ALERT: {message}")
    
    def get_alerts(self, status: str = 'active', limit: int = 10) -> str:
        """Get system alerts."""
        try:
            filtered_alerts = [
                alert for alert in self.alerts
                if alert['status'] == status
            ]
            
            if not filtered_alerts:
                return f"📋 No {status} alerts found"
            
            # Get recent alerts
            recent_alerts = filtered_alerts[-limit:]
            recent_alerts.reverse()  # Show newest first
            
            response = f"🚨 **{status.title()} Alerts** ({len(recent_alerts)} entries)\n\n"
            
            for alert in recent_alerts:
                timestamp = datetime.fromisoformat(alert['timestamp'])
                alert_type_emoji = {
                    'cpu': '⚡',
                    'memory': '🧠',
                    'disk': '💾',
                    'network': '🌐',
                    'temperature': '🌡️'
                }.get(alert['type'], '⚠️')
                
                response += f"{alert_type_emoji} **{alert['message']}**\n"
                response += f"   🕒 {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
                response += f"   🆔 ID: {alert['id']}\n\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting alerts: {str(e)}"
    
    def clear_alerts(self, alert_type: str = None) -> str:
        """Clear alerts."""
        try:
            if alert_type:
                # Clear alerts of specific type
                self.alerts = [alert for alert in self.alerts if alert['type'] != alert_type]
                message = f"✅ Cleared {alert_type} alerts"
            else:
                # Clear all alerts
                self.alerts = []
                message = "✅ Cleared all alerts"
            
            self._save_alerts()
            return message
            
        except Exception as e:
            return f"❌ Error clearing alerts: {str(e)}"
    
    def set_threshold(self, metric: str, value: float) -> str:
        """Set alert threshold for a metric."""
        try:
            if metric not in self.thresholds:
                available_metrics = ', '.join(self.thresholds.keys())
                return f"❌ Unknown metric '{metric}'. Available metrics: {available_metrics}"
            
            self.thresholds[metric] = value
            self.settings['thresholds'] = self.thresholds
            self._save_settings()
            
            return f"✅ Set {metric} threshold to {value}"
            
        except Exception as e:
            return f"❌ Error setting threshold: {str(e)}"
    
    def get_thresholds(self) -> str:
        """Get current alert thresholds."""
        try:
            response = "⚙️ **Alert Thresholds**\n\n"
            
            for metric, threshold in self.thresholds.items():
                metric_emoji = {
                    'cpu_percent': '⚡',
                    'memory_percent': '🧠',
                    'disk_percent': '💾',
                    'temperature': '🌡️',
                    'network_latency': '🌐'
                }.get(metric, '📊')
                
                response += f"{metric_emoji} **{metric.replace('_', ' ').title()}:** {threshold}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting thresholds: {str(e)}"
    
    def get_performance_summary(self, hours: int = 24) -> str:
        """Get performance summary for specified hours."""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Filter metrics for the specified time period
            recent_metrics = [
                metric for metric in self.metrics_history
                if datetime.fromisoformat(metric['timestamp']) >= cutoff_time
            ]
            
            if not recent_metrics:
                return f"📊 No metrics available for the last {hours} hours"
            
            # Calculate averages
            cpu_avg = sum(m['cpu_percent'] for m in recent_metrics) / len(recent_metrics)
            memory_avg = sum(m['memory_percent'] for m in recent_metrics) / len(recent_metrics)
            disk_avg = sum(m['disk_percent'] for m in recent_metrics) / len(recent_metrics)
            
            # Calculate peaks
            cpu_peak = max(m['cpu_percent'] for m in recent_metrics)
            memory_peak = max(m['memory_percent'] for m in recent_metrics)
            disk_peak = max(m['disk_percent'] for m in recent_metrics)
            
            response = f"📊 **Performance Summary (Last {hours} Hours)**\n\n"
            response += f"📈 **Averages:**\n"
            response += f"   • CPU: {cpu_avg:.1f}%\n"
            response += f"   • Memory: {memory_avg:.1f}%\n"
            response += f"   • Disk: {disk_avg:.1f}%\n\n"
            
            response += f"📊 **Peaks:**\n"
            response += f"   • CPU: {cpu_peak:.1f}%\n"
            response += f"   • Memory: {memory_peak:.1f}%\n"
            response += f"   • Disk: {disk_peak:.1f}%\n\n"
            
            response += f"📊 **Data Points:** {len(recent_metrics)} measurements\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting performance summary: {str(e)}"
    
    def get_system_monitor_help(self) -> str:
        """Get help information for system monitoring features."""
        return """💻 **System Monitoring Help**

🔧 **System Information:**
   • 'system info' - Get comprehensive system information
   • 'system metrics' - Get current system metrics
   • 'top processes' - Show top CPU-consuming processes
   • 'top processes memory' - Show top memory-consuming processes

📊 **Monitoring:**
   • 'start monitoring' - Start continuous system monitoring
   • 'stop monitoring' - Stop system monitoring
   • 'performance summary' - Get performance summary
   • 'performance summary 12' - Get 12-hour performance summary

🚨 **Alerts:**
   • 'system alerts' - Show active alerts
   • 'clear alerts' - Clear all alerts
   • 'clear alerts cpu' - Clear CPU alerts only
   • 'set threshold cpu_percent 75' - Set CPU alert threshold

⚙️ **Configuration:**
   • 'get thresholds' - Show current alert thresholds
   • 'set threshold memory_percent 80' - Set memory threshold
   • 'set threshold disk_percent 85' - Set disk threshold

📈 **Available Metrics:**
   • cpu_percent - CPU usage percentage
   • memory_percent - Memory usage percentage
   • disk_percent - Disk usage percentage
   • temperature - CPU temperature (if available)
   • network_latency - Network latency

💡 **Examples:**
   • 'system info' - Get full system information
   • 'top processes 5' - Show top 5 processes
   • 'start monitoring 30' - Monitor every 30 seconds
   • 'set threshold cpu_percent 70' - Alert if CPU > 70%
   • 'performance summary 6' - 6-hour performance summary

📊 **Features:**
   • Real-time system monitoring
   • Customizable alert thresholds
   • Performance history tracking
   • Process monitoring
   • Network statistics
   • Automatic alert generation
"""
