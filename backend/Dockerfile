FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# App user
RUN useradd -m appuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    HOST=0.0.0.0 \
    APP_MODULE=${APP_MODULE:-agno_agent:app}

# Expose port
EXPOSE 8000

CMD ["sh", "-c", "python -m uvicorn $APP_MODULE --host $HOST --port $PORT --workers 1"]
