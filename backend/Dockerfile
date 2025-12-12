# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# system deps for PyPDF2 / build tools if needed
RUN apt-get update && apt-get install -y build-essential libpoppler-cpp-dev pkg-config python3-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy source
COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
