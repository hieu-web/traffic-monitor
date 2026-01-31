# 🚦 AI Traffic Violation Monitor System

![YOLOv8](https://img.shields.io/badge/YOLO-v8-yellow.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20App-lightgrey.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)
![ALPR](https://img.shields.io/badge/ALPR-License%20Plate-red.svg)

AI Traffic Violation Monitor System is a real-time computer vision application for detecting **red light violations** from traffic videos. The system now features **Automatic License Plate Recognition (ALPR)**, providing an interactive dashboard that allows users to tune detection parameters, observe results, and view zoomed-in license plate evidence instantly.

---

## 🖥️ System Interface

<div align="center">
  <img src="demo/demo1.PNG" width="48%" alt="Dashboard Screenshot 1">
  <img src="demo/demo2.PNG" width="48%" alt="Dashboard Screenshot 2">
  <br><br>
  <img src="demo/gif.gif" width="100%" alt="System Demo GIF">
</div>
The dashboard includes:

* **Left panel:** Detection and configuration controls
* **Center:** Processed video stream
* **Right panel:** Real-time traffic statistics & **Live Plate Zoom**

---

## 🚀 Main Features

### 🎯 Vehicle Detection
* YOLOv8-based detection
* Supported vehicle classes:
    * Car
    * Motorbike
    * Bus
    * Truck

### 🚦 Red Light Violation Detection
A violation is recorded when:
* The traffic light state is **RED**
* A detected vehicle crosses the **Stop Line**

### 🔍 License Plate Recognition & Zoom (New)
* **2-Stage Detection Strategy**:
    1.  **Stage 1:** Detects the violating vehicle using the main traffic model.
    2.  **Stage 2:** Crops the vehicle image and passes it to a specialized secondary YOLOv8 model to locate the license plate.
* **Smart Zoom:** Automatically crops and enlarges the license plate for clear readability.
* **Real-time Display:** The zoomed plate is flashed on the dashboard immediately when a violation occurs.

### 🧠 Traffic Light State Stabilization
* Uses a frame buffer to stabilize red/green state
* Reduces false detection caused by lighting noise

### 📸 Violation Evidence Capture
* Automatically saves frames when violations occur
* Evidence includes:
    * Full scene image with bounding boxes
    * **Cropped and zoomed license plate image**
    * Vehicle type, timestamp, and traffic light state

### 📊 Real-Time Statistics
* Total violations
* Vehicle classified and counted by type

---

## 🎛️ Dashboard Controls

### Stop Line (%)
* Adjusts the vertical position of the stop line
* Typical range: **70–80%**

### AI Confidence
* Minimum confidence threshold for YOLO detections

### Traffic Light ROI (%)
Defines the region for traffic light detection:
* ROI X
* ROI Y
* ROI Width
* ROI Height

### 🛣️ Road Limits Configuration
Limits the valid road area to reduce false detections outside lanes.
* **Horizon Limit (Top):** Upper boundary of the road area. Vehicles above this line are ignored.
* **Lane Left (%):** Left boundary of the valid road region.
* **Lane Right (%):** Right boundary of the valid road region.

### Video Upload
* Upload `.mp4` traffic videos
* Statistics reset automatically for each new video

---

## 🛠️ Technology Stack

| Component        | Technology             |
| ---------------- | ---------------------- |
| Object Detection | **Dual YOLOv8 Models** (Traffic + License Plate) |
| Video Processing | OpenCV                 |
| Backend          | Flask, Flask-SocketIO  |
| Frontend         | HTML, CSS, Bootstrap   |
| Database         | SQLite                 |
| Deployment       | Docker, Docker Compose |

---

## ⚙️ Installation & Usage

### Method 1: Docker (Recommended)

```bash
git clone [https://github.com/hieu-web/traffic-monitor.git](https://github.com/hieu-web/traffic-monitor.git)
cd traffic-monitor
docker-compose up --build
```

Open in browser:

```
http://localhost:5000
```

---

### Method 2: Local Installation

```bash
pip install -r requirements.txt
python app.py
```

Open in browser:

```
http://localhost:5000
```

---

## 📂 Project Structure

```text
traffic-monitor/
├── models/              # YOLOv8 weights
├── static/
│   ├── uploads/         # Uploaded videos
│   ├── evidence/        # Violation images
│   └── style.css
├── templates/
│   ├── index.html       # Main dashboard
│   └── history.html    # Violation history
├── app.py               # Flask backend
├── traffic_core.py      # Detection logic
├── traffic.db           # SQLite database
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

