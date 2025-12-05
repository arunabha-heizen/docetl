import psutil
import time
import threading
from typing import Dict, Any

class ResourceMonitor:
    def __init__(self, sample_interval: float = 0.1):
        self.sample_interval = sample_interval
        self.stop_event = threading.Event()
        self.metrics = {
            "peak_memory_mb": 0.0,
            "cpu_samples": [],
            "peak_cpu_percent": 0.0
        }
        self.thread = None
        self.process = psutil.Process()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        self.thread = threading.Thread(target=self._monitor_loop)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join()

    def _monitor_loop(self):
        # Initial call to cpu_percent returns 0.0 usually, so we ignore it or just start loop
        self.process.cpu_percent() 
        
        while not self.stop_event.is_set():
            # Memory
            mem_info = self.process.memory_info()
            rss_mb = mem_info.rss / (1024 * 1024)
            if rss_mb > self.metrics["peak_memory_mb"]:
                self.metrics["peak_memory_mb"] = rss_mb

            # CPU
            # We use interval=None because we are sleeping manually
            try:
                cpu = self.process.cpu_percent(interval=None)
                self.metrics["cpu_samples"].append(cpu)
                if cpu > self.metrics["peak_cpu_percent"]:
                    self.metrics["peak_cpu_percent"] = cpu
            except:
                pass

            time.sleep(self.sample_interval)

    def get_metrics(self) -> Dict[str, Any]:
        samples = self.metrics["cpu_samples"]
        avg_cpu = sum(samples) / len(samples) if samples else 0.0
        
        return {
            "peak_memory_mb": round(self.metrics["peak_memory_mb"], 2),
            "peak_cpu_usage_percent": round(self.metrics["peak_cpu_percent"], 2),
            "avg_cpu_usage_percent": round(avg_cpu, 2),
            "active_core_count": psutil.cpu_count()
        }
