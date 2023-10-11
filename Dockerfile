FROM python:3.11.6-alpine3.18

WORKDIR /app

COPY . .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "main.py"]