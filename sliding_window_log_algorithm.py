import datetime


class SlidingWindowLogAlgorithm:
    def __init__(self, limit_rate: int):
        self.windows = []
        self.is_async = False
        self.limit_rate = limit_rate

    def is_valid(self, client_ip: str) -> bool:
        for window in self.windows:
            if window.client_ip == client_ip:
                return window.is_valid()

        self.windows.append(_SlidingWindowLog(client_ip, self.limit_rate))
        return True


class _SlidingWindowLog:
    def __init__(self, client_ip: str, limit_rate: int):
        self.limit_rate = limit_rate
        self._logs = []  # timestamps
        self._threshold = limit_rate  # requests/min
        self.client_ip = client_ip

    def is_valid(self) -> bool:
        current_time = datetime.datetime.now()
        one_minute_ago = current_time - datetime.timedelta(minutes=1)

        # delete all the logs that do not fit in the one minute window
        self._logs = [log for log in self._logs if log > one_minute_ago]

        # check if < threshold
        if len(self._logs) < self._threshold:
            self._logs.append(current_time)
            return True
        else:
            return False
