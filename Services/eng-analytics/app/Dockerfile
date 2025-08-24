FROM python:3.11-slim

WORKDIR /app

COPY Services/eng-analytics/app/requirements.txt .
RUN pip install -r requirements.txt

COPY Services/eng-analytics/app/ .
COPY Services/eng-analytics/tests/ ./tests
COPY common/ ./common

CMD ["python", "app.py"]
