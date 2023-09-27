import threading
import time


class BucketToken:
    def __init__(self):
        self.bucket = 10
        thread = threading.Thread(target=self.add_token)
        thread.daemon = True
        thread.start()

    def valid(self):
        if self.bucket >= 0:
            self.bucket -= 1
            return True
        else:
            return False

    def add_token(self):
        while True:
            if self.bucket < 10:
                self.bucket += 1
            time.sleep(1)
