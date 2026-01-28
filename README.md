# 🚦 AI Traffic Violation Monitor System

![YOLOv8](https://img.shields.io/badge/YOLO-v8-yellow.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20App-lightgrey.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)

AI Traffic Violation Monitor System is a real-time computer vision application for detecting **red light violations** from traffic videos. The system provides an interactive dashboard that allows users to tune detection parameters and observe results instantly.

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
* **Right panel:** Real-time traffic statistics

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

### 🧠 Traffic Light State Stabilization

* Uses a frame buffer to stabilize red/green state
* Reduces false detection caused by lighting noise

### 📸 Violation Evidence Capture

* Automatically saves frames when violations occur
* Evidence includes vehicle position, stop line, and traffic light state

### 📊 Real-Time Statistics

* Total violations
* Vehicle violated count by type

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
* **AI Confidence:** Minimum confidence score required for a detection to be considered valid.

### Video Upload

* Upload `.mp4` traffic videos
* Statistics reset automatically for each new video

---

## 🛠️ Technology Stack

| Component        | Technology             |
| ---------------- | ---------------------- |
| Object Detection | YOLOv8 (Ultralytics)   |
| Video Processing | OpenCV                 |
| Backend          | Flask, Flask-SocketIO  |
| Frontend         | HTML, CSS, Bootstrap   |
| Database         | SQLite                 |
| Deployment       | Docker, Docker Compose |



---

## ⚙️ Installation & Usage

### Method 1: Docker (Recommended)

```bash
git clone https://github.com/hieu-web/traffic-monitor.git
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

---


## 🏗️ System Architecture

### High-Level Architecture
The system follows a modular architecture separating the web interface, backend server, and the AI processing core.

```mermaid
graph TD
    subgraph "Frontend (User Browser)"
        UI["💻 Web Dashboard"]
        JS["🔌 Socket.IO Client"]
    end

    subgraph "Backend (Flask Server)"
        Flask["🌐 Flask Web App"]
        SocketServer["📡 Socket.IO Server"]
        
        subgraph "AI Processing Core"
            Core["🧠 TrafficCore Controller"]
            YOLO["📦 YOLOv8 Detection"]
            CV["🖼️ OpenCV Processing"]
            Logic["⚡ Business Logic"]
        end
    end

    subgraph "Storage"
        SQLite[("💾 SQLite DB")]
        FS["📂 File System"]
    end

    UI -->|Upload/Config| Flask
    Flask -->|Video Frame| Core
    Core -->|Detect| YOLO
    Core -->|Process| CV
    Core -->|Analyze| Logic
    Logic -->|Save Violation| SQLite
    Logic -->|Save Image| FS
    Core -->|Stream Frame| UI
    SocketServer -->|Live Stats| JS

---



## 🔄 Video Processing Data Flow
The logic separates "Counting" (all vehicles) from "Violation Detection" (vehicles in the enforcement zone).

```mermaid
sequenceDiagram
    participant App as 🌐 Flask App
    participant Core as 🧠 TrafficCore
    participant Logic as ⚡ Logic Filters
    participant DB as 💾 Database

    loop 🎞️ Every Frame
        App->>Core: Process Frame
        Core->>Core: 1. 🚦 Detect Traffic Light
        Core->>Core: 2. 📦 YOLOv8 Tracking
        
        loop 🚗 Each Vehicle
            Core->>Logic: 📏 Filter Horizon/Size
            
            par 🔢 Counting Logic
                Logic->>Logic: Check Stop Line Crossing
                Logic-->>Core: Count All Vehicles
            and 🚨 Violation Logic
                Logic->>Logic: Check Enforcement Zone
                Logic->>Logic: Check Red Light
                alt 📸 Violation Detected
                    Logic->>DB: Save Record & Image
                    Logic-->>Core: Mark Red Box
                end
            end
        end
        Core-->>App: Return Processed Frame
    end