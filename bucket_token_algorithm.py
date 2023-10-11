import threading
import time


class BucketTokenAlgorithm:
    def __init__(self, limit_rate: int):
        self.limit_rate = limit_rate
        self.buckets = []
        self.is_async = False

    def is_valid(self, client_ip: str) -> bool:
        for bucket in self.buckets:
            if bucket.client_ip == client_ip:
                return bucket.is_valid()
        else:
            bucket = _BucketToken(client_ip, self.limit_rate)
            self.buckets.append(bucket)
            return True


class _BucketToken:
    def __init__(self, client_ip: str, limit_rate: int):
        self.limit_rate = limit_rate
        self.bucket = limit_rate
        self.client_ip = client_ip
        thread = threading.Thread(target=self._add_token)
        thread.daemon = True
        thread.start()

    def is_valid(self):
        if self.bucket > 0:
            self.bucket -= 1
            return True
        else:
            return False

    def _add_token(self):
        while True:
            if self.bucket < self.limit_rate:
                self.bucket += 1
            time.sleep(1)
