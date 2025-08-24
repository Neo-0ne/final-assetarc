FROM python:3.11-slim

WORKDIR /app

COPY Services/eng-compliance/app/requirements.txt .
RUN pip install -r requirements.txt

COPY Services/eng-compliance/app/ .
COPY Services/eng-compliance/tests/ ./tests
COPY common/ ./common

CMD ["python", "app.py"]
