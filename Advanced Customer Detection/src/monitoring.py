import time
import psutil
from datetime import datetime
from functools import wraps
from threading import Thread
import queue
import json
import os
from src.logger import log_performance, log_function

class PerformanceMonitor:
    """Sistem performansını izleyen sınıf."""
    
    def __init__(self):
        """Performans monitörünü başlat."""
        # Performans metrikleri için kuyruk
        self.metric_queue = queue.Queue()
        
        # İzleme thread'i
        self.monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self, interval=1):
        """Performans izlemeyi başlat.
        
        Args:
            interval (int): İzleme aralığı (saniye)
        """
        self.monitoring = True
        self.monitor_thread = Thread(target=self._monitor_loop, args=(interval,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Performans izlemeyi durdur."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
    
    def _monitor_loop(self, interval):
        """Performans metriklerini periyodik olarak topla."""
        while self.monitoring:
            metrics = self.get_system_metrics()
            self.metric_queue.put(metrics)
            log_performance(metrics)
            time.sleep(interval)
    
    def get_system_metrics(self):
        """Sistem metriklerini topla."""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'percent': cpu_percent,
                'count': psutil.cpu_count()
            },
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'percent': memory.percent
            },
            'disk': {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent
            }
        }
    
    def get_latest_metrics(self):
        """En son metrikleri al."""
        try:
            return self.metric_queue.get_nowait()
        except queue.Empty:
            return None

def monitor_performance(func):
    """Fonksiyon performansını izleyen dekoratör."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss
        
        execution_time = end_time - start_time
        memory_used = (end_memory - start_memory) / 1024 / 1024  # MB cinsinden
        
        log_function(func.__name__, execution_time, memory_used)
        
        return result
    return wrapper 