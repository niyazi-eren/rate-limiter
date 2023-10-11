# rate-limiter
Implementation of a Rate limiter in Python (https://codingchallenges.fyi/challenges/challenge-rate-limiter)

### Pre-requisite
- Docker
- Docker-compose

### Installation
Clone the repository: ```git clone https://github.com/niyazi-eren/rate-limiter```

```cd rate-limiter```

 ```docker-compose run --build --rm -p 8000:8000 python --strategy sliding_db```

 ### Usage
 ``` docker-compose run --build --rm -p port_number:port_number python --port <port_number> --rate <rate> --strategy <strategy>```
 
For a server running on port 8000 for example:
- You can try ```curl localhost:8000/limited ```
- Or ```curl localhost:8000/unlimited ```

### Example
- #### Run the app on port 8080 with a rate limit of 20 per minute using the sliding window log algorithm
```docker-compose run --build --rm -p 8080:8080 python --port 8080 --rate 20 --strategy log```

- #### Run the app with default options (port 8000, rate 10, and bucket token algorithm)
```docker-compose run --build --rm -p 8000:8000 python```

### Test
There is a bash script to run tests for the sliding window counter algorithm: you need to launch 2 servers with the correct algorithm, one in port 8000 one in 8001

A better way is to use [Postman](https://blog.postman.com/postman-api-performance-testing/)
