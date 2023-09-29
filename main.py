import uvicorn
from fastapi import FastAPI, HTTPException, Request

from sliding_window_counter_algorithm import SlidingWindowCounterAlgorithm

app = FastAPI()

# strategy = BucketTokenAlgorithm()
# strategy = WindowCounterAlgorithm()
# strategy = SlidingWindowLogAlgorithm()
strategy = SlidingWindowCounterAlgorithm()


@app.get("/limited", response_model=str)
def get_limited(request: Request):
    client_ip = request.client.host  # Get the client's IP address

    req_is_valid = strategy.is_valid(client_ip)
    if req_is_valid:
        return f"Limited, don't over use me!"
    else:
        raise HTTPException(status_code=429, detail="Too Many Requests")


@app.get("/unlimited", response_model=str)
def get_unlimited():
    return "Unlimited! Let's Go!"


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
