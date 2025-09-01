FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY Services/eng-identity/app/requirements.txt .
RUN pip install -r requirements.txt

COPY Services/eng-identity/app/ .
COPY Services/eng-identity/tests/ ./tests
COPY common/ ./common

CMD ["python", "app.py"]
