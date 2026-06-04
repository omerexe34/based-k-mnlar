import threading
import queue
import time

class AnalysisQueue:
    """
    Handles heavy async operations like full terrain simulation grids,
    spec scraping, or PDF export generation without blocking the main Flask thread.
    """
    def __init__(self):
        self.q = queue.Queue()
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

    def _worker(self):
        while True:
            task = self.q.get()
            if task is None:
                break
            try:
                func, args, kwargs = task
                func(*args, **kwargs)
            except Exception as e:
                print(f"Async Task Error: {e}")
            finally:
                self.q.task_done()

    def enqueue(self, func, *args, **kwargs):
        self.q.put((func, args, kwargs))

analysis_queue = AnalysisQueue()

# Example usage:
# analysis_queue.enqueue(terrain_simulator.simulate, state_dict)
