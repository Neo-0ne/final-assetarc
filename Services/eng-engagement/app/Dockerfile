FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY Services/eng-engagement/app/requirements.txt .
RUN pip install -r requirements.txt

COPY Services/eng-engagement/app/ .
COPY Services/eng-engagement/tests/ ./tests
COPY common/ ./common

CMD ["python", "app.py"]
