from datetime import datetime, timedelta


class SlidingWindowCounterAlgorithm:
    def __init__(self, limit_rate: int):
        self.windows = []
        self.is_async = False
        self.limit_rate = limit_rate

    def is_valid(self, client_ip: str) -> bool:
        for window in self.windows:
            if window.client_ip == client_ip:
                return window.is_valid()

        self.windows.append(_SlidingWindowCounter(client_ip, self.limit_rate))
        return True


class _SlidingWindowCounter:
    def __init__(self, client_ip: str, limit_rate: int):
        self.client_ip = client_ip
        self._window = datetime.now()
        self._window_size = 10  # in seconds
        self._prev_window = self._window - timedelta(seconds=self._window_size)
        self._cnt = 0
        self._prev_cnt = 0
        self.limit_rate = limit_rate

    def is_valid(self) -> bool:
        current_time = datetime.now()
        time_diff = (current_time - self._prev_window).total_seconds()

        # Reset the sliding window if necessary
        if time_diff >= self._window_size:
            self._prev_window = self._window
            self._window = current_time
            self._prev_cnt = self._cnt
            self._cnt = 0

        prev_window_weight = (self._window_size - (self._window.second % self._window_size)) / self._window_size
        prev_weighted_cnt = prev_window_weight * self._prev_cnt

        if self._cnt + prev_weighted_cnt < self.limit_rate:
            self._cnt += 1
            return True
        else:
            return False
