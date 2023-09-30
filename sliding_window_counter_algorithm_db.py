import json
import logging
from datetime import datetime, timedelta

import redis

redis = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Configure the logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("logger")


class SlidingWindowCounterAlgorithmDb:
    async def is_valid(self, client_ip: str) -> bool:
        data = redis.get(client_ip)
        if data is not None:
            json_data = json.loads(data)
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
            w = datetime.strptime(json_data["window"], date_format)
            prev_w = datetime.strptime(json_data["prev_window"], date_format)
            logger.info(f"window: {w}")
            logger.info(f"prev_window: {prev_w}")
            window = SlidingWindowCounter.from_values(
                client_ip=client_ip,
                cnt=json_data["cnt"],
                prev_cnt=json_data["prev_cnt"],
                window=w,
                prev_window=prev_w,
            )
            return window.is_valid()
        else:
            json_data = SlidingWindowCounter(client_ip=client_ip).to_json()
            _ = redis.set(client_ip, json_data)
            return True


class SlidingWindowCounter:
    def __init__(self, client_ip: str):
        self.client_ip = client_ip
        self.window = datetime.now()
        self.window_size = 10  # in seconds
        self.prev_window = self.window - timedelta(seconds=self.window_size)
        self.cnt = 0
        self.prev_cnt = 0
        self.rate_limit = 5  # 5 req/s

    @classmethod
    def from_values(cls, client_ip: str, cnt: int, prev_cnt: int, window: datetime, prev_window: datetime):
        instance = cls(client_ip)
        instance.cnt = cnt
        instance.prev_cnt = prev_cnt
        instance.window = window
        instance.prev_window = prev_window
        return instance

    def is_valid(self) -> bool:
        current_time = datetime.now()
        time_diff = (current_time - self.prev_window).total_seconds()

        # Reset the sliding window if necessary
        if time_diff >= self.window_size:
            self.prev_window = self.window
            self.window = current_time
            self.prev_cnt = self.cnt
            self.cnt = 0
            redis.set(self.client_ip, self.to_json())
            logger.info(f"reset window for {self.client_ip}")

        prev_window_weight = (self.window_size - (self.window.second % self.window_size)) / self.window_size
        prev_weighted_cnt = prev_window_weight * self.prev_cnt

        logger.info(f" rate: {self.cnt + prev_weighted_cnt}")

        if self.cnt + prev_weighted_cnt < self.rate_limit:
            self.cnt += 1
            redis.set(self.client_ip, self.to_json())
            return True
        else:
            return False

    def to_json(self) -> str:
        data = {
            "client_ip": self.client_ip,
            "window": self.window.isoformat(),
            "prev_window": self.prev_window.isoformat(),
            "cnt": self.cnt,
            "prev_cnt": self.prev_cnt,
        }
        return json.dumps(data)
