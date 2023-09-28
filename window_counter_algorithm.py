import threading
import time


class WindowCounterAlgorithm:
    def __init__(self):
        self.windows = []

    def is_valid(self, client_ip: str) -> bool:
        for window in self.windows:
            if window.client_ip == client_ip:
                return window.is_valid()
        else:
            self.windows.append(_WindowCounter(client_ip))
            return True


class _WindowCounter:
    def __init__(self, client_ip: str):
        self.window_size = 10
        self.client_ip = client_ip

        thread = threading.Thread(target=self._reset_window)
        thread.daemon = True
        thread.start()

    def is_valid(self) -> bool:
        if self.window_size > 0:
            self.window_size -= 1
            return True
        else:
            return False

    # reset window size every minute
    def _reset_window(self):
        while True:
            current_time = time.localtime()

            if current_time.tm_sec == 0:
                self.window_size = 10
                time.sleep(1)
