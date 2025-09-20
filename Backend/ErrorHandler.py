"""
ErrorHandler.py
Advanced error handling and recovery system for JARVIS.
"""

import os
import time
import json
import traceback
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Callable, List
from functools import wraps
import threading

class JarvisErrorHandler:
    """
    Advanced error handling system that provides:
    - Automatic error recovery and retry mechanisms
    - Error logging and analysis
    - Graceful degradation when services fail
    - User-friendly error messages
    - Error pattern detection and learning
    """
    
    def __init__(self, log_dir: str = "Data/logs"):
        self.log_dir = log_dir
        self.error_log_file = os.path.join(log_dir, "error_log.json")
        self.recovery_log_file = os.path.join(log_dir, "recovery_log.json")
        
        # Ensure log directory exists
        os.makedirs(log_dir, exist_ok=True)
        
        # Error tracking
        self.error_counts = {}
        self.error_patterns = {}
        self.recovery_attempts = {}
        self.last_errors = []
        
        # Recovery strategies
        self.recovery_strategies = {
            'api_timeout': self._retry_with_backoff,
            'network_error': self._retry_with_backoff,
            'permission_error': self._handle_permission_error,
            'file_not_found': self._handle_file_not_found,
            'import_error': self._handle_import_error,
            'memory_error': self._handle_memory_error,
            'keyboard_interrupt': self._handle_user_interrupt,
            'default': self._default_recovery
        }
        
        # Fallback responses
        self.fallback_responses = {
            'api_error': "I'm experiencing some connectivity issues. Let me try a different approach.",
            'file_error': "I'm having trouble accessing that file. Could you check if it exists?",
            'permission_error': "I don't have permission to perform that action. Please check your system settings.",
            'memory_error': "I'm running low on memory. Let me optimize and try again.",
            'unknown_error': "Something unexpected happened. Let me try to recover and continue."
        }
        
        # Load existing error logs
        self._load_error_logs()
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging system."""
        try:
            log_file = os.path.join(self.log_dir, "jarvis.log")
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_file),
                    logging.StreamHandler()
                ]
            )
            self.logger = logging.getLogger('JARVIS')
        except Exception as e:
            print(f"⚠️ Logging setup failed: {e}")
            self.logger = None
    
    def _load_error_logs(self):
        """Load error logs from disk."""
        try:
            if os.path.exists(self.error_log_file):
                with open(self.error_log_file, 'r') as f:
                    data = json.load(f)
                    self.error_counts = data.get('error_counts', {})
                    self.error_patterns = data.get('error_patterns', {})
                    self.last_errors = data.get('last_errors', [])
            
            if os.path.exists(self.recovery_log_file):
                with open(self.recovery_log_file, 'r') as f:
                    self.recovery_attempts = json.load(f)
        except Exception as e:
            print(f"⚠️ Error log load failed: {e}")
            self.error_counts = {}
            self.error_patterns = {}
            self.recovery_attempts = {}
            self.last_errors = []
    
    def _save_error_logs(self):
        """Save error logs to disk."""
        try:
            error_data = {
                'error_counts': self.error_counts,
                'error_patterns': self.error_patterns,
                'last_errors': self.last_errors[-50:],  # Keep only last 50 errors
                'timestamp': datetime.now().isoformat()
            }
            
            with open(self.error_log_file, 'w') as f:
                json.dump(error_data, f, indent=2)
            
            with open(self.recovery_log_file, 'w') as f:
                json.dump(self.recovery_attempts, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Error log save failed: {e}")
    
    def _classify_error(self, error: Exception) -> str:
        """Classify error type for appropriate handling."""
        error_type = type(error).__name__.lower()
        error_message = str(error).lower()
        
        # Network/API errors
        if any(keyword in error_message for keyword in ['timeout', 'connection', 'network', 'api']):
            return 'api_timeout'
        elif 'permission' in error_message or 'access' in error_message:
            return 'permission_error'
        elif 'not found' in error_message or 'file' in error_message:
            return 'file_not_found'
        elif 'import' in error_message or 'module' in error_message:
            return 'import_error'
        elif 'memory' in error_message or 'out of memory' in error_message:
            return 'memory_error'
        elif isinstance(error, KeyboardInterrupt):
            return 'keyboard_interrupt'
        else:
            return 'default'
    
    def _retry_with_backoff(self, func: Callable, *args, max_retries: int = 3, **kwargs) -> Any:
        """Retry function with exponential backoff."""
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"⏳ Retry {attempt + 1}/{max_retries} after {wait_time}s delay")
                time.sleep(wait_time)
        
        return None
    
    def _handle_permission_error(self, error: Exception) -> str:
        """Handle permission-related errors."""
        return self.fallback_responses['permission_error']
    
    def _handle_file_not_found(self, error: Exception) -> str:
        """Handle file not found errors."""
        return self.fallback_responses['file_error']
    
    def _handle_import_error(self, error: Exception) -> str:
        """Handle import/module errors."""
        return "I'm missing some required components. Please check the installation."
    
    def _handle_memory_error(self, error: Exception) -> str:
        """Handle memory-related errors."""
        # Try to optimize memory
        try:
            import gc
            gc.collect()
            return self.fallback_responses['memory_error']
        except:
            return "I'm experiencing memory issues. Please restart JARVIS."
    
    def _handle_user_interrupt(self, error: Exception) -> str:
        """Handle user interrupt (Ctrl+C)."""
        return "Operation cancelled by user."
    
    def _default_recovery(self, error: Exception) -> str:
        """Default error recovery."""
        return self.fallback_responses['unknown_error']
    
    def handle_error(self, error: Exception, context: str = "", retry_func: Optional[Callable] = None) -> str:
        """
        Handle an error with appropriate recovery strategy.
        
        Args:
            error: The exception that occurred
            context: Context information about where the error occurred
            retry_func: Optional function to retry the operation
            
        Returns:
            User-friendly error message or recovery result
        """
        try:
            error_type = self._classify_error(error)
            error_key = f"{error_type}:{context}"
            
            # Track error
            self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
            self.last_errors.append({
                'timestamp': datetime.now().isoformat(),
                'type': error_type,
                'context': context,
                'message': str(error),
                'traceback': traceback.format_exc()
            })
            
            # Log error
            if self.logger:
                self.logger.error(f"Error in {context}: {error}", exc_info=True)
            
            # Try recovery strategy
            if error_type in self.recovery_strategies:
                recovery_strategy = self.recovery_strategies[error_type]
                
                # If retry function provided and error is retryable
                if retry_func and error_type in ['api_timeout', 'network_error']:
                    try:
                        result = self._retry_with_backoff(retry_func)
                        if result:
                            print(f"✅ Recovery successful for {error_type}")
                            return result
                    except Exception as retry_error:
                        print(f"❌ Recovery failed: {retry_error}")
                
                # Use fallback response
                fallback_response = recovery_strategy(error)
                return fallback_response
            
            # Default recovery
            return self.recovery_strategies['default'](error)
            
        except Exception as handler_error:
            print(f"❌ Error handler failed: {handler_error}")
            return "An unexpected error occurred. Please try again."
        finally:
            # Save error logs periodically
            if len(self.last_errors) % 10 == 0:
                self._save_error_logs()
    
    def safe_execute(self, func: Callable, *args, context: str = "", fallback: Optional[str] = None, **kwargs) -> Any:
        """
        Safely execute a function with error handling.
        
        Args:
            func: Function to execute
            *args: Function arguments
            context: Context for error reporting
            fallback: Fallback return value on error
            **kwargs: Function keyword arguments
            
        Returns:
            Function result or fallback value
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = self.handle_error(e, context)
            print(f"⚠️ {context}: {error_message}")
            return fallback
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics and patterns."""
        try:
            total_errors = sum(self.error_counts.values())
            unique_errors = len(self.error_counts)
            
            # Most common errors
            top_errors = sorted(
                self.error_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            # Recent error patterns
            recent_errors = self.last_errors[-10:] if self.last_errors else []
            
            return {
                'total_errors': total_errors,
                'unique_errors': unique_errors,
                'top_errors': top_errors,
                'recent_errors': recent_errors,
                'recovery_attempts': len(self.recovery_attempts)
            }
            
        except Exception as e:
            return {'error': f"Failed to get error stats: {e}"}
    
    def cleanup_old_errors(self, days: int = 30):
        """Clean up old error logs."""
        try:
            cutoff_date = datetime.now().timestamp() - (days * 24 * 3600)
            
            # Filter recent errors
            self.last_errors = [
                error for error in self.last_errors
                if datetime.fromisoformat(error['timestamp']).timestamp() > cutoff_date
            ]
            
            # Reset error counts periodically
            if len(self.last_errors) == 0:
                self.error_counts = {}
                self.error_patterns = {}
            
            self._save_error_logs()
            print(f"🧹 Cleaned up errors older than {days} days")
            
        except Exception as e:
            print(f"⚠️ Error cleanup failed: {e}")

# Decorator for automatic error handling
def error_handler(context: str = "", fallback: Optional[Any] = None, retry: bool = False):
    """Decorator for automatic error handling."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            global _global_error_handler
            if '_global_error_handler' not in globals() or _global_error_handler is None:
                return func(*args, **kwargs)
            
            try:
                return func(*args, **kwargs)
            except Exception as e:
                retry_func = func if retry else None
                error_message = _global_error_handler.handle_error(e, context or func.__name__, retry_func)
                
                if fallback is not None:
                    return fallback
                else:
                    return error_message
        return wrapper
    return decorator

# Global error handler instance
_global_error_handler = None

def get_error_handler() -> JarvisErrorHandler:
    """Get the global error handler instance."""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = JarvisErrorHandler()
    return _global_error_handler

def init_error_handler():
    """Initialize the global error handler."""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = JarvisErrorHandler()
        print("✅ Error handler initialized")
    return _global_error_handler
