import datetime


class SlidingWindowLogAlgorithm:
    def __init__(self):
        self.windows = []

    def is_valid(self, client_ip: str) -> bool:
        for window in self.windows:
            if window.client_ip == client_ip:
                return window.is_valid()

        self.windows.append(_SlidingWindowLog(client_ip))
        return True


class _SlidingWindowLog:
    def __init__(self, client_ip: str):
        self._logs = []  # timestamps
        self._threshold = 20  # 20 requests/min
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
