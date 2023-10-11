import argparse
import logging

import uvicorn
from fastapi import FastAPI, HTTPException, Request

from bucket_token_algorithm import BucketTokenAlgorithm
from sliding_window_counter_algorithm import SlidingWindowCounterAlgorithm
from sliding_window_counter_algorithm_db import SlidingWindowCounterAlgorithmDb
from sliding_window_log_algorithm import SlidingWindowLogAlgorithm
from window_counter_algorithm import WindowCounterAlgorithm

app = FastAPI()

strategy = None
server = None

# Configure the logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("logger")


@app.get("/limited", response_model=str)
async def get_limited(request: Request):
    global strategy
    global server

    client_ip = request.client.host  # Get the client's IP address

    if strategy.is_async:
        try:
            req_is_valid = await strategy.is_valid(client_ip)
        except HTTPException as exc:
            raise HTTPException(status_code=exc.status_code, detail=exc.detail)
    else:
        req_is_valid = strategy.is_valid(client_ip)

    if req_is_valid:
        return "Limited, don't over use me!"
    else:
        raise HTTPException(status_code=429, detail="Too Many Requests")


@app.get("/unlimited", response_model=str)
def get_unlimited():
    return "Unlimited! Let's Go!"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the app with specified port.')
    parser.add_argument('--port', type=str, default=8000, help='Port number (default: 8000)')
    parser.add_argument('--rate', type=int, default=10, help='Rate')
    parser.add_argument('--strategy', default="bucket", choices=['bucket', 'window', 'log', 'sliding', 'sliding_db'],
                        help='Choose a strategy: bucket, window, log, sliding, or sliding_db')
    args = parser.parse_args()
    rate = args.rate - 1

    # Set the rate limiting strategy
    if args.strategy == 'bucket':
        strategy = BucketTokenAlgorithm(rate)
    elif args.strategy == 'window':
        strategy = WindowCounterAlgorithm(rate)
    elif args.strategy == 'log':
        strategy = SlidingWindowLogAlgorithm(rate)
    elif args.strategy == 'sliding':
        strategy = SlidingWindowCounterAlgorithm(rate)
    elif args.strategy == 'sliding_db':
        strategy = SlidingWindowCounterAlgorithmDb(rate)
    else:
        parser.print_usage()
        exit(1)

    logger.info(f"using {type(strategy).__name__} with rate: {args.rate}")
    uvicorn.run(app, host="0.0.0.0", port=args.port)
