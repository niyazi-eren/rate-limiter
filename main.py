import uvicorn
from fastapi import FastAPI, HTTPException

from bucket_token import BucketToken

app = FastAPI()
strategy = BucketToken()

@app.get("/limited", response_model=str)
def get_limited():
    global strategy
    if strategy.valid():
        return f"Limited, don't over use me!"
    else:
        raise HTTPException(status_code=429, detail="Too Many Requests")


@app.get("/unlimited", response_model=str)
def get_unlimited():
    return "Unlimited! Let's Go!"


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
