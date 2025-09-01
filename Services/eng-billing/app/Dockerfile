FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY Services/eng-billing/app/requirements.txt .
RUN pip install -r requirements.txt

COPY Services/eng-billing/app/ .
COPY Services/eng-billing/tests/ ./tests
COPY common/ ./common

CMD ["python", "app.py"]
