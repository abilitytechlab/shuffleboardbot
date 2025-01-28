import time
import os
import threading


class ShutdownHelper:
    def __init__(self, inactive_time: int):
        self.inactive_time = inactive_time
        self.last_activity = time.time()
        self.running = True
        self._start_monitoring_thread()

    def _start_monitoring_thread(self):
        thread = threading.Thread(target=self._monitor_inactivity, daemon=True)
        thread.start()

    def _monitor_inactivity(self):
        while self.running:
            time.sleep(60)
            if time.time() - self.last_activity > self.inactive_time:
                print("Shutting down due to inactivity", flush=True)
                os.system("shutdown -h now")
                self.running = False

    def update(self):
        # Update last activity timestamp
        self.last_activity = time.time()

    def stop(self):
        # Stop the monitoring thread
        self.running = False
