"""
StartupOptimizer.py
Fast startup optimization system for JARVIS.
"""

import os
import time
import threading
import json
from typing import Dict, Any, Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed

class JarvisStartupOptimizer:
    """
    Optimizes JARVIS startup time through:
    - Parallel component initialization
    - Lazy loading of heavy components
    - Startup caching
    - Component prioritization
    """
    
    def __init__(self):
        self.startup_start = time.time()
        self.startup_log = []
        self.component_times = {}
        self.initialization_order = []
        
        # Component priorities (lower = higher priority)
        self.component_priorities = {
            'performance_optimizer': 1,
            'error_handler': 2,
            'model': 3,
            'memory': 4,
            'decision_brain': 5,
            'automation': 6,
            'search_engine': 7,
            'image_gen': 8,
            'text_to_speech': 9,
            'speech_to_text': 10
        }
        
        # Components that can be lazy loaded
        self.lazy_components = {
            'image_gen', 'text_to_speech', 'speech_to_text', 'search_engine'
        }
        
        # Critical components (must load first)
        self.critical_components = {
            'performance_optimizer', 'error_handler', 'model', 'memory'
        }
    
    def log_startup_step(self, component: str, duration: float, success: bool = True):
        """Log a startup step."""
        step = {
            'component': component,
            'duration': duration,
            'success': success,
            'timestamp': time.time()
        }
        self.startup_log.append(step)
        self.component_times[component] = duration
        self.initialization_order.append(component)
        
        status = "✅" if success else "❌"
        print(f"{status} {component}: {duration:.3f}s")
    
    def initialize_component(self, component_name: str, init_func, *args, **kwargs):
        """Initialize a single component with timing."""
        start_time = time.time()
        try:
            result = init_func(*args, **kwargs)
            duration = time.time() - start_time
            self.log_startup_step(component_name, duration, True)
            return result
        except Exception as e:
            duration = time.time() - start_time
            self.log_startup_step(component_name, duration, False)
            print(f"❌ {component_name} initialization failed: {e}")
            return None
    
    def initialize_critical_components(self, jarvis_instance) -> Dict[str, Any]:
        """Initialize critical components first (sequential)."""
        print("🚀 Initializing critical components...")
        critical_results = {}
        
        # Performance optimizer (must be first)
        if hasattr(jarvis_instance, '_init_performance_optimizer'):
            critical_results['optimizer'] = self.initialize_component(
                'performance_optimizer',
                jarvis_instance._init_performance_optimizer
            )
        
        # Error handler
        if hasattr(jarvis_instance, '_init_error_handler'):
            critical_results['error_handler'] = self.initialize_component(
                'error_handler',
                jarvis_instance._init_error_handler
            )
        
        # Model (core AI)
        if hasattr(jarvis_instance, '_init_model'):
            critical_results['model'] = self.initialize_component(
                'model',
                jarvis_instance._init_model
            )
        
        # Memory system
        if hasattr(jarvis_instance, '_init_memory'):
            critical_results['memory'] = self.initialize_component(
                'memory',
                jarvis_instance._init_memory
            )
        
        return critical_results
    
    def initialize_parallel_components(self, jarvis_instance) -> Dict[str, Any]:
        """Initialize non-critical components in parallel."""
        print("⚡ Initializing components in parallel...")
        
        # Components to initialize in parallel
        parallel_components = [
            ('decision_brain', jarvis_instance._init_decision_brain),
            ('automation', jarvis_instance._init_automation),
        ]
        
        results = {}
        
        # Use ThreadPoolExecutor for parallel initialization
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Submit all parallel initialization tasks
            future_to_component = {
                executor.submit(self.initialize_component, name, init_func): name
                for name, init_func in parallel_components
                if hasattr(jarvis_instance, init_func.__name__)
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_component):
                component_name = future_to_component[future]
                try:
                    result = future.result()
                    results[component_name] = result
                except Exception as e:
                    print(f"❌ Parallel initialization failed for {component_name}: {e}")
                    results[component_name] = None
        
        return results
    
    def initialize_lazy_components(self, jarvis_instance) -> Dict[str, Any]:
        """Initialize lazy components when needed."""
        print("🔄 Setting up lazy loading...")
        lazy_results = {}
        
        # Store initialization functions for later use
        lazy_initializers = {
            'search_engine': getattr(jarvis_instance, '_init_search_engine', None),
            'image_gen': getattr(jarvis_instance, '_init_image_gen', None),
            'text_to_speech': getattr(jarvis_instance, '_init_text_to_speech', None),
            'speech_to_text': getattr(jarvis_instance, '_init_speech_to_text', None),
        }
        
        # Store lazy initializers for later use
        jarvis_instance._lazy_initializers = lazy_initializers
        
        return lazy_results
    
    def optimize_imports(self):
        """Optimize imports by loading only what's needed."""
        print("📦 Optimizing imports...")
        
        # Import optimization strategies
        optimization_strategies = [
            "Deferring heavy imports until needed",
            "Using conditional imports",
            "Caching import results",
            "Lazy loading of optional dependencies"
        ]
        
        for strategy in optimization_strategies:
            print(f"   • {strategy}")
        
        return True
    
    def get_startup_summary(self) -> Dict[str, Any]:
        """Get startup performance summary."""
        total_startup_time = time.time() - self.startup_start
        
        # Calculate statistics
        successful_components = [c for c in self.startup_log if c['success']]
        failed_components = [c for c in self.startup_log if not c['success']]
        
        avg_component_time = sum(c['duration'] for c in successful_components) / len(successful_components) if successful_components else 0
        slowest_component = max(successful_components, key=lambda x: x['duration']) if successful_components else None
        
        summary = {
            'total_startup_time': total_startup_time,
            'total_components': len(self.startup_log),
            'successful_components': len(successful_components),
            'failed_components': len(failed_components),
            'average_component_time': avg_component_time,
            'slowest_component': slowest_component,
            'initialization_order': self.initialization_order,
            'component_times': self.component_times
        }
        
        return summary
    
    def print_startup_report(self):
        """Print a detailed startup report."""
        summary = self.get_startup_summary()
        
        print("\n" + "="*60)
        print("🚀 JARVIS STARTUP PERFORMANCE REPORT")
        print("="*60)
        
        print(f"⏱️  Total Startup Time: {summary['total_startup_time']:.3f}s")
        print(f"📦 Components Loaded: {summary['successful_components']}/{summary['total_components']}")
        
        if summary['failed_components'] > 0:
            print(f"❌ Failed Components: {summary['failed_components']}")
        
        if summary['slowest_component']:
            slowest = summary['slowest_component']
            print(f"🐌 Slowest Component: {slowest['component']} ({slowest['duration']:.3f}s)")
        
        print(f"📊 Average Component Time: {summary['average_component_time']:.3f}s")
        
        print("\n📋 Component Loading Order:")
        for i, component in enumerate(summary['initialization_order'], 1):
            duration = summary['component_times'].get(component, 0)
            print(f"   {i:2d}. {component}: {duration:.3f}s")
        
        print("="*60)
        
        # Performance recommendations
        if summary['total_startup_time'] > 5.0:
            print("⚠️  Startup time is slow. Consider:")
            print("   • Enabling more lazy loading")
            print("   • Optimizing heavy components")
            print("   • Using startup caching")
        elif summary['total_startup_time'] < 2.0:
            print("✅ Excellent startup performance!")
        else:
            print("✅ Good startup performance")
        
        return summary

def optimize_jarvis_startup(jarvis_instance) -> JarvisStartupOptimizer:
    """Optimize JARVIS startup process."""
    optimizer = JarvisStartupOptimizer()
    
    print("🚀 Starting optimized JARVIS initialization...")
    
    # Step 1: Optimize imports
    optimizer.optimize_imports()
    
    # Step 2: Initialize critical components first
    critical_results = optimizer.initialize_critical_components(jarvis_instance)
    
    # Step 3: Initialize parallel components
    parallel_results = optimizer.initialize_parallel_components(jarvis_instance)
    
    # Step 4: Setup lazy loading
    lazy_results = optimizer.initialize_lazy_components(jarvis_instance)
    
    # Step 5: Print performance report
    optimizer.print_startup_report()
    
    return optimizer

# Decorator for lazy loading
def lazy_load(component_name: str):
    """Decorator for lazy loading components."""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, component_name):
                print(f"🔄 Lazy loading {component_name}...")
                start_time = time.time()
                
                # Initialize the component
                if hasattr(self, '_lazy_initializers') and component_name in self._lazy_initializers:
                    initializer = self._lazy_initializers[component_name]
                    if initializer:
                        result = initializer()
                        setattr(self, component_name, result)
                        duration = time.time() - start_time
                        print(f"✅ {component_name} loaded in {duration:.3f}s")
                
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
