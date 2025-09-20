"""
PerformanceOptimizer.py
Performance optimization system for JARVIS with caching, background processing, and monitoring.
"""

import os
import time
import threading
import json
import pickle
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Callable
from functools import wraps
import psutil
import gc

class JarvisPerformanceOptimizer:
    """
    Performance optimization system that provides:
    - Intelligent caching for API responses and expensive operations
    - Background processing for heavy tasks
    - Performance monitoring and metrics
    - Memory management and garbage collection
    - Startup optimization
    """
    
    def __init__(self, cache_dir: str = "Data/cache"):
        self.cache_dir = cache_dir
        self.cache_file = os.path.join(cache_dir, "performance_cache.pkl")
        self.metrics_file = os.path.join(cache_dir, "performance_metrics.json")
        
        # Ensure cache directory exists
        os.makedirs(cache_dir, exist_ok=True)
        
        # Cache storage
        self.cache = {}
        self.cache_metadata = {}
        self.max_cache_size = 1000  # Maximum number of cached items
        self.cache_ttl = 3600  # Cache time-to-live in seconds (1 hour)
        
        # Background task queue
        self.background_tasks = []
        self.background_thread = None
        self.background_running = False
        
        # Performance metrics
        self.metrics = {
            'startup_time': 0,
            'api_call_times': [],
            'cache_hits': 0,
            'cache_misses': 0,
            'memory_usage': [],
            'error_count': 0,
            'total_requests': 0
        }
        
        # Load existing cache and metrics
        self._load_cache()
        self._load_metrics()
        
        # Start background processing
        self._start_background_processing()
    
    def _load_cache(self):
        """Load cache from disk."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
                    self.cache = cache_data.get('cache', {})
                    self.cache_metadata = cache_data.get('metadata', {})
                print(f"✅ Loaded {len(self.cache)} cached items")
        except Exception as e:
            print(f"⚠️ Cache load failed: {e}")
            self.cache = {}
            self.cache_metadata = {}
    
    def _save_cache(self):
        """Save cache to disk."""
        try:
            cache_data = {
                'cache': self.cache,
                'metadata': self.cache_metadata
            }
            with open(self.cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
        except Exception as e:
            print(f"⚠️ Cache save failed: {e}")
    
    def _load_metrics(self):
        """Load performance metrics from disk."""
        try:
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, 'r') as f:
                    self.metrics.update(json.load(f))
        except Exception as e:
            print(f"⚠️ Metrics load failed: {e}")
    
    def _save_metrics(self):
        """Save performance metrics to disk."""
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            print(f"⚠️ Metrics save failed: {e}")
    
    def _start_background_processing(self):
        """Start background processing thread."""
        if not self.background_running:
            self.background_running = True
            self.background_thread = threading.Thread(target=self._background_worker, daemon=True)
            self.background_thread.start()
            print("✅ Background processing started")
    
    def _background_worker(self):
        """Background worker for processing heavy tasks."""
        while self.background_running:
            try:
                # Process background tasks
                if self.background_tasks:
                    task = self.background_tasks.pop(0)
                    if callable(task):
                        task()
                
                # Clean up expired cache entries
                self._cleanup_cache()
                
                # Update performance metrics
                self._update_metrics()
                
                # Save cache and metrics periodically
                if len(self.background_tasks) == 0:
                    self._save_cache()
                    self._save_metrics()
                
                time.sleep(5)  # Run every 5 seconds
                
            except Exception as e:
                print(f"⚠️ Background worker error: {e}")
                time.sleep(10)  # Wait longer on error
    
    def _cleanup_cache(self):
        """Clean up expired cache entries."""
        current_time = time.time()
        expired_keys = []
        
        for key, metadata in self.cache_metadata.items():
            if current_time - metadata.get('timestamp', 0) > self.cache_ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            self.cache.pop(key, None)
            self.cache_metadata.pop(key, None)
        
        # Limit cache size
        if len(self.cache) > self.max_cache_size:
            # Remove oldest entries
            sorted_items = sorted(
                self.cache_metadata.items(),
                key=lambda x: x[1].get('timestamp', 0)
            )
            for key, _ in sorted_items[:len(self.cache) - self.max_cache_size]:
                self.cache.pop(key, None)
                self.cache_metadata.pop(key, None)
    
    def _update_metrics(self):
        """Update performance metrics."""
        try:
            # Memory usage
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            self.metrics['memory_usage'].append({
                'timestamp': time.time(),
                'memory_mb': memory_mb
            })
            
            # Keep only last 100 memory readings
            if len(self.metrics['memory_usage']) > 100:
                self.metrics['memory_usage'] = self.metrics['memory_usage'][-100:]
                
        except Exception as e:
            print(f"⚠️ Metrics update error: {e}")
    
    def cache_result(self, key: str, result: Any, ttl: Optional[int] = None) -> Any:
        """
        Cache a result with optional TTL.
        
        Args:
            key: Cache key
            result: Result to cache
            ttl: Time-to-live in seconds (default: use global TTL)
        
        Returns:
            Cached result
        """
        try:
            # Create hash of key for consistent storage
            cache_key = hashlib.md5(key.encode()).hexdigest()
            
            self.cache[cache_key] = result
            self.cache_metadata[cache_key] = {
                'timestamp': time.time(),
                'ttl': ttl or self.cache_ttl,
                'original_key': key
            }
            
            return result
            
        except Exception as e:
            print(f"⚠️ Cache error: {e}")
            return result
    
    def get_cached_result(self, key: str) -> Optional[Any]:
        """
        Get cached result if available and not expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached result or None if not found/expired
        """
        try:
            cache_key = hashlib.md5(key.encode()).hexdigest()
            
            if cache_key not in self.cache:
                self.metrics['cache_misses'] += 1
                return None
            
            metadata = self.cache_metadata.get(cache_key, {})
            current_time = time.time()
            
            # Check if expired
            if current_time - metadata.get('timestamp', 0) > metadata.get('ttl', self.cache_ttl):
                self.cache.pop(cache_key, None)
                self.cache_metadata.pop(cache_key, None)
                self.metrics['cache_misses'] += 1
                return None
            
            self.metrics['cache_hits'] += 1
            return self.cache[cache_key]
            
        except Exception as e:
            print(f"⚠️ Cache retrieval error: {e}")
            self.metrics['cache_misses'] += 1
            return None
    
    def add_background_task(self, task: Callable):
        """Add a task to background processing queue."""
        self.background_tasks.append(task)
    
    def cached_api_call(self, api_function: Callable, cache_key: str, *args, **kwargs) -> Any:
        """
        Make an API call with caching.
        
        Args:
            api_function: Function to call
            cache_key: Cache key for this call
            *args, **kwargs: Arguments for the function
            
        Returns:
            API result (from cache or fresh call)
        """
        # Try to get from cache first
        cached_result = self.get_cached_result(cache_key)
        if cached_result is not None:
            print(f"🚀 Cache hit for: {cache_key}")
            return cached_result
        
        # Make fresh API call
        start_time = time.time()
        try:
            result = api_function(*args, **kwargs)
            
            # Cache the result
            self.cache_result(cache_key, result)
            
            # Record timing
            call_time = time.time() - start_time
            self.metrics['api_call_times'].append({
                'timestamp': start_time,
                'duration': call_time,
                'api': api_function.__name__ if hasattr(api_function, '__name__') else str(api_function)
            })
            
            # Keep only last 100 API call times
            if len(self.metrics['api_call_times']) > 100:
                self.metrics['api_call_times'] = self.metrics['api_call_times'][-100:]
            
            print(f"🌐 API call completed in {call_time:.2f}s: {cache_key}")
            return result
            
        except Exception as e:
            self.metrics['error_count'] += 1
            print(f"❌ API call failed: {e}")
            raise
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics."""
        try:
            # Calculate cache hit rate
            total_cache_requests = self.metrics['cache_hits'] + self.metrics['cache_misses']
            cache_hit_rate = (self.metrics['cache_hits'] / total_cache_requests * 100) if total_cache_requests > 0 else 0
            
            # Calculate average API call time
            api_times = [call['duration'] for call in self.metrics['api_call_times']]
            avg_api_time = sum(api_times) / len(api_times) if api_times else 0
            
            # Current memory usage
            process = psutil.Process()
            current_memory = process.memory_info().rss / 1024 / 1024
            
            # Cache statistics
            cache_size = len(self.cache)
            cache_memory = sum(len(str(item)) for item in self.cache.values()) / 1024 / 1024  # Rough estimate
            
            return {
                'cache_hit_rate': round(cache_hit_rate, 2),
                'cache_size': cache_size,
                'cache_memory_mb': round(cache_memory, 2),
                'avg_api_time': round(avg_api_time, 3),
                'current_memory_mb': round(current_memory, 2),
                'total_requests': self.metrics['total_requests'],
                'error_count': self.metrics['error_count'],
                'background_tasks': len(self.background_tasks),
                'startup_time': self.metrics.get('startup_time', 0)
            }
            
        except Exception as e:
            print(f"⚠️ Stats calculation error: {e}")
            return {'error': str(e)}
    
    def optimize_memory(self):
        """Force garbage collection and memory optimization."""
        try:
            # Force garbage collection
            collected = gc.collect()
            
            # Clear expired cache entries
            self._cleanup_cache()
            
            print(f"🧹 Memory optimized: {collected} objects collected")
            return collected
            
        except Exception as e:
            print(f"⚠️ Memory optimization error: {e}")
            return 0
    
    def shutdown(self):
        """Shutdown the performance optimizer."""
        try:
            self.background_running = False
            if self.background_thread:
                self.background_thread.join(timeout=5)
            
            # Save final cache and metrics
            self._save_cache()
            self._save_metrics()
            
            print("✅ Performance optimizer shutdown complete")
            
        except Exception as e:
            print(f"⚠️ Shutdown error: {e}")

# Decorator for automatic caching
def cached(ttl: int = 3600):
    """Decorator for automatic caching of function results."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from global optimizer cache
            global _global_optimizer
            if '_global_optimizer' in globals():
                cached_result = _global_optimizer.get_cached_result(cache_key)
                if cached_result is not None:
                    return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            
            if '_global_optimizer' in globals():
                _global_optimizer.cache_result(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator

# Global optimizer instance
_global_optimizer = None

def get_optimizer() -> JarvisPerformanceOptimizer:
    """Get the global performance optimizer instance."""
    global _global_optimizer
    if _global_optimizer is None:
        _global_optimizer = JarvisPerformanceOptimizer()
    return _global_optimizer

def init_performance_optimizer():
    """Initialize the global performance optimizer."""
    global _global_optimizer
    if _global_optimizer is None:
        start_time = time.time()
        _global_optimizer = JarvisPerformanceOptimizer()
        _global_optimizer.metrics['startup_time'] = time.time() - start_time
        print(f"✅ Performance optimizer initialized in {_global_optimizer.metrics['startup_time']:.2f}s")
    return _global_optimizer
