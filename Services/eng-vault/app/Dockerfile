FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY Services/eng-vault/app/requirements.txt .
RUN pip install -r requirements.txt

COPY Services/eng-vault/app/ .
COPY Services/eng-vault/tests/ ./tests
COPY common/ ./common

CMD ["python", "app.py"]
