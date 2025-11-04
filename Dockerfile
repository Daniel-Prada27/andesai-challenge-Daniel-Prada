FROM python:3.12.3-slim

WORKDIR /api

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app /api/app
COPY data /api/data
COPY .env.example /api/.env

ENV PYTHONPATH=/api

RUN useradd -m appuser

RUN chown -R appuser:appuser /api/data

USER appuser


EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
