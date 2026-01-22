# 🚦 AI Traffic Monitor – Red Light Violation Detection System

![YOLOv8](https://img.shields.io/badge/YOLO-v8-yellow.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)

**AI Traffic Monitor** is an intelligent traffic surveillance system that uses Computer Vision to automatically detect and record evidence of vehicles running red lights.  
The system is optimized to reduce false positives and ensure stable, reliable detection.

---

## 🚀 Key Features

* **🎯 Accurate Detection:** Uses the **YOLOv8** model to classify vehicles such as motorcycles, cars, buses, and trucks.
* **🚦 Red Light Violation Logic:** The system reports a violation when a vehicle crosses the stop line while the traffic light is red.
* **⚖️ Stable Traffic Light State:** A buffering algorithm (15 frames) is used to prevent traffic light state flickering (green/red) caused by lighting noise.
* **📸 Full-Scene Evidence:** Automatically captures and stores violation images including the violating vehicle, stop line, and red light state at that moment.
* **🎛️ Control Dashboard:** A web-based interface allows real-time adjustment of the stop line position and traffic light detection region (ROI).
* **🐳 Docker Support:** Easy deployment on any machine using a single command.

---

## 🛠️ Technologies Used

* **Core AI:** Ultralytics YOLOv8
* **Image Processing:** OpenCV (cv2)
* **Backend:** Flask, Flask-SocketIO
* **Frontend:** HTML5, Bootstrap 5, Socket.IO
* **Database:** SQLite
* **Containerization:** Docker & Docker Compose

---

## ⚙️ Installation & Usage

### Method 1: Docker (Recommended)

1.  **Download the source code:**
    ```bash
    git clone [https://github.com/USERNAME/traffic-monitor.git](https://github.com/USERNAME/traffic-monitor.git)
    cd traffic-monitor
    ```
2.  **Run the application:**
    ```bash
    docker-compose up --build
    ```
3.  **Access the system:**
    Open your browser and go to `http://localhost:5000`

### Method 2: Local Installation

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the application:**
    ```bash
    python app.py
    ```
3.  **Access the system:**
    Open your browser and go to `http://localhost:5000`

---

## 📖 Dashboard User Guide

### 1. Upload Video
Click **Choose Video** to upload a traffic video for analysis.

### 2. Adjust Stop Line
Use the **Stop Line (%)** slider to position the detection boundary.
* **Recommended value:** 70–80%

### 3. Adjust Traffic Light ROI
Use **ROI X** and **ROI Width** sliders to define the traffic light area.
* **Tip:** Keep the ROI tight around the traffic light bulb for best accuracy.



### 4. View Results
* **Green Box:** Vehicle is compliant.
* **Red Box:** Red light violation (evidence image is automatically saved to the system).

| Visual Indicator | Meaning | System Action |
| :--- | :--- | :--- |
| **Green Box** | Compliant | No violation detected. |
| **Red Box** | **Violation** | Red light violation detected; evidence image saved. |