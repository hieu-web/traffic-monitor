FROM python:3.9-slim

ENV DEBIAN_FRONTEND=noninteractive

# Thư viện hệ thống cho OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p static/uploads static/evidence

EXPOSE 5000

CMD ["python", "app.py"]

