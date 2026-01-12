# 🚦 AI Traffic Monitor - Hệ Thống Phát Hiện Vượt Đèn Đỏ

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![YOLOv8](https://img.shields.io/badge/YOLO-v8-yellow.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)

**AI Traffic Monitor** là hệ thống giám sát giao thông thông minh, sử dụng Computer Vision để tự động phát hiện và ghi lại bằng chứng các phương tiện vượt đèn đỏ. Dự án được tối ưu hóa để loại bỏ các trường hợp báo lỗi sai .

## 🚀 Tính Năng Nổi Bật

* **🎯 Nhận diện chính xác:** Sử dụng mô hình **YOLOv8** để phân loại: Xe máy, Ô tô, Xe buýt, Xe tải.
* **🚦 Logic Vượt Đèn Đỏ :** Hệ thống báo vi phạm khi xe đã vượt qua vạch dừng khi đèn đang đỏ. 
* **⚖️ Ổn định tín hiệu đèn:** Sử dụng thuật toán đệm (Buffer 15 frames) giúp trạng thái đèn (Xanh/Đỏ) không bị nhấp nháy do nhiễu sáng.
* **📸 Bằng chứng toàn cảnh:** Tự động chụp và lưu ảnh hiện trường bao gồm cả: Xe vi phạm + Vạch kẻ đường + Trạng thái đèn đỏ tại thời điểm đó.
* **🎛️ Dashboard điều khiển:** Giao diện web cho phép tùy chỉnh vị trí vạch dừng (Stop Line) và vùng nhận diện đèn (ROI) theo thời gian thực.
* **🐳 Hỗ trợ Docker:** Dễ dàng triển khai (Deploy) trên mọi máy tính chỉ với 1 lệnh.

## 🛠️ Công Nghệ Sử Dụng

* **Core AI:** Ultralytics YOLOv8
* **Xử lý ảnh:** OpenCV (cv2)
* **Backend:** Flask, Flask-SocketIO
* **Frontend:** HTML5, Bootstrap 5, Socket.IO
* **Database:** SQLite
* **Containerization:** Docker & Docker Compose

## ⚙️ Cài Đặt & Sử Dụng

cách 1


1.  **Tải source code:**
    ```bash
    git clone [https://github.com/USERNAME/traffic-monitor.git](https://github.com/USERNAME/traffic-monitor.git)
    cd traffic-monitor
    ```
2.  **Khởi chạy:**
    ```bash
    docker-compose up --build
    ```
3.  **Truy cập:** Mở trình duyệt vào `http://localhost:5000`

cách 2

1.  **Cài đặt thư viện:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Chạy ứng dụng:**
    ```bash
    python app.py
    ```
3.  **Truy cập:** Mở trình duyệt vào `http://localhost:5000`

## 📖 Hướng Dẫn Trên Dashboard

1.  **Upload Video:** Nhấn nút `Choose Video` để tải video giao thông lên.
2.  **Chỉnh Vạch Dừng (Stop Line):**
    * Kéo thanh trượt **Stop Line (%)**.
    * *Mẹo:* Nên kéo vạch thấp xuống một chút (khoảng 70-80%) để đảm bảo tính chính xác.
3.  **Chỉnh Vùng Đèn (Light ROI):**
    * Dùng thanh trượt **ROI X** và **ROI Width** để khoanh vùng trúng cột đèn giao thông.
    * Khung ROI càng nhỏ và sát bóng đèn thì nhận diện càng chuẩn.
4.  **Xem Kết Quả:**
    * **Khung Xanh:** Xe đi đúng luật.
    * **Khung Đỏ:** Xe vi phạm (hệ thống sẽ tự động chụp ảnh và đẩy sang cột bên phải).

## 📂 Cấu Trúc Thư Mục

```text
traffic-monitor/
├── app.py              # Server Flask chính
├── traffic_core.py     # Logic AI cốt lõi (Xử lý ảnh & YOLO)
├── Dockerfile          # Cấu hình môi trường Docker
├── docker-compose.yml  # Cấu hình chạy Docker
├── requirements.txt    # Danh sách thư viện Python
├── models/
│   └── best.pt         # File trọng số model YOLOv8
├── static/
│   ├── evidence/       # Thư mục chứa ảnh chụp vi phạm
│   └── uploads/        # Thư mục chứa video tải lên
├── templates/
│   └── index.html      # Giao diện chính
└── traffic.db          # Cơ sở dữ liệu SQLite
