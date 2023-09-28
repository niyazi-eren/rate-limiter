import threading
import time


class BucketTokenAlgorithm:
    def __init__(self):
        self.buckets = []

    def is_valid(self, client_ip: str) -> bool:
        for bucket in self.buckets:
            if bucket.client_ip == client_ip:
                return bucket.is_valid()
        else:
            bucket = _BucketToken(client_ip)
            self.buckets.append(bucket)
            return True


class _BucketToken:
    def __init__(self, client_ip):
        self._bucket = 10
        self.client_ip = client_ip
        thread = threading.Thread(target=self._add_token)
        thread.daemon = True
        thread.start()

    def is_valid(self):
        if self._bucket > 0:
            self._bucket -= 1
            return True
        else:
            return False

    def _add_token(self):
        while True:
            if self._bucket < 10:
                self._bucket += 1
            time.sleep(1)
