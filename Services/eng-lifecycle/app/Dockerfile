FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY Services/eng-lifecycle/app/requirements.txt .
RUN pip install -r requirements.txt

COPY Services/eng-lifecycle/app/ .
COPY Services/eng-lifecycle/tests/ ./tests
COPY common/ ./common

CMD ["python", "app.py"]
