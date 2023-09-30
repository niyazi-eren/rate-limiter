import argparse
import sys

import uvicorn
from fastapi import FastAPI, HTTPException, Request

from sliding_window_counter_algorithm_db import SlidingWindowCounterAlgorithmDb

app = FastAPI()

# strategy = BucketTokenAlgorithm()
# strategy = WindowCounterAlgorithm()
# strategy = SlidingWindowLogAlgorithm()
# strategy = SlidingWindowCounterAlgorithm()
strategy = SlidingWindowCounterAlgorithmDb()


@app.get("/limited", response_model=str)
async def get_limited(request: Request):
    client_ip = request.client.host  # Get the client's IP address

    req_is_valid = await strategy.is_valid(client_ip)
    if req_is_valid:
        return "Limited, don't over use me!"
    else:
        raise HTTPException(status_code=429, detail="Too Many Requests")


@app.get("/unlimited", response_model=str)
def get_unlimited():
    return "Unlimited! Let's Go!"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the app with specified port.')
    parser.add_argument('--port', type=int, default=8000, help='Port number (default: 8000)')
    args = parser.parse_args()
    uvicorn.run(app, host="localhost", port=args.port)
