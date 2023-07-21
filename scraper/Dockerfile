FROM python:3.9-slim-buster
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
ENV SANIC_WORKERS=1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
