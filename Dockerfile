# Sử dụng Python 3.9 bản Slim
FROM python:3.9-slim

# Cài đặt thư viện hệ thống cho OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy file requirements và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Tạo thư mục dữ liệu
RUN mkdir -p static/uploads static/evidence

# Mở cổng 5000
EXPOSE 5000

# Chạy app
CMD ["python", "app.py"]