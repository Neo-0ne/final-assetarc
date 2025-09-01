FROM python:3.11-slim

WORKDIR /app

COPY Services/eng-drafting/app/requirements.txt .
RUN pip install -r requirements.txt

COPY Services/eng-drafting/app/ .
COPY Services/eng-drafting/tests/ ./tests
COPY common/ ./common

CMD ["python", "app.py"]
