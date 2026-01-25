import cv2
import sqlite3
import numpy as np
import os
from ultralytics import YOLO
from datetime import datetime

class TrafficCore:
    def __init__(self):
        # Load model YOLO
        self.model = YOLO("models/best.pt")
        self.class_names = self.model.names
        
        
        self.traffic_direction = "UP"  
        self.vehicle_colors = {
            "Car": (0, 255, 0), "Motorcycle": (255, 255, 0),
            "Bus": (0, 255, 255), "Truck": (255, 0, 255)
        }
        self.last_light_status = "UNKNOWN"
        self.light_buffer = [] 
        os.makedirs("static/evidence", exist_ok=True)
        self.init_db()
        self.reset_session()

    def init_db(self):
        with sqlite3.connect('traffic.db') as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS violations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicle_type TEXT, plate TEXT, time TEXT, image_path TEXT
                )
            ''')

    def reset_session(self):
        self.stats = {"Total": 0, "Violation": 0, "Bus": 0, "Car": 0, "Motorcycle": 0, "Truck": 0}
        self.counted_ids = set()
        self.violated_ids = set()

    def map_label(self, raw_label):
        raw = raw_label.lower()
        if raw in ['car', 'taxi', 'suv', 'jeep', 'o to', 'ô tô']: return "Car"
        if raw in ['motorcycle', 'motorbike', 'moto', 'xe may', 'xe máy']: return "Motorcycle"
        if raw in ['bus', 'autobus', 'xe buyt']: return "Bus"
        if raw in ['truck', 'lorry', 'van', 'xe tai']: return "Truck"
        return None

    def get_light_color(self, roi_img):
        if roi_img is None or roi_img.size == 0: return "UNKNOWN"
        roi_blur = cv2.GaussianBlur(roi_img, (5, 5), 0)
        hsv = cv2.cvtColor(roi_blur, cv2.COLOR_BGR2HSV)
        
        
        mask_r = cv2.addWeighted(
            cv2.inRange(hsv, np.array([0, 100, 100]), np.array([10, 255, 255])), 1.0,
            cv2.inRange(hsv, np.array([170, 100, 100]), np.array([180, 255, 255])), 1.0, 0
        )
        
        mask_g = cv2.inRange(hsv, np.array([40, 120, 120]), np.array([90, 255, 255]))
        
        r_pix, g_pix = cv2.countNonZero(mask_r), cv2.countNonZero(mask_g)
        
        current = "OFF"
        threshold = 20
        
        if r_pix > threshold: current = "RED"
        elif g_pix > threshold + 10: current = "GREEN"
            
        if current != "OFF":
            self.light_buffer.append(current)
            if len(self.light_buffer) > 8: self.light_buffer.pop(0)
            
        return max(set(self.light_buffer), key=self.light_buffer.count) if self.light_buffer else "OFF"

    def process_frame(self, frame, cfg):
        raw_evidence = frame.copy() 
        H, W = frame.shape[:2]
        
        stop_line_y = int(H * float(cfg['stop_line']) / 100)
        rx, ry = int(W * float(cfg['roi_x']) / 100), int(H * float(cfg['roi_y']) / 100)
        rw, rh = int(W * float(cfg['roi_w']) / 100), int(H * float(cfg['roi_h']) / 100)

        
        rx, ry = max(0, rx), max(0, ry)
        rw, rh = min(W-rx, rw), min(H-ry, rh)
        if rw > 0 and rh > 0:
            roi_light = frame[ry:ry+rh, rx:rx+rw]
            self.last_light_status = self.get_light_color(roi_light)
            color_roi = (0, 0, 255) if self.last_light_status == "RED" else ((0, 255, 0) if self.last_light_status == "GREEN" else (0, 255, 255))
            cv2.rectangle(frame, (rx, ry), (rx+rw, ry+rh), color_roi, 2)

      
        cv2.line(frame, (0, stop_line_y), (W, stop_line_y), (0, 0, 255) if self.last_light_status == "RED" else (0, 255, 0), 3)

        #  Tracking
        results = self.model.track(frame, persist=True, conf=float(cfg['conf_threshold']), verbose=False)
        new_violation = None

        if results and results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            clss = results[0].boxes.cls.int().cpu().tolist()
            ids = results[0].boxes.id.int().cpu().tolist()

            for box, cls, tid in zip(boxes, clss, ids):
                x1, y1, x2, y2 = map(int, box)
                label = self.map_label(self.class_names[cls])
                if label is None: continue 
                veh_color = self.vehicle_colors.get(label, (200, 200, 200))
                center_y = int((y1 + y2) / 2)

                
                has_crossed = False
                is_violation = False
                
                
                buffer_zone = 20 

                if self.traffic_direction == "UP":
                    
                    if center_y < stop_line_y: has_crossed = True
                    
                    if self.last_light_status == "RED" and y2 < (stop_line_y - buffer_zone): 
                        is_violation = True
                        
                else:
                    
                    if center_y > stop_line_y: has_crossed = True
                    
                    if self.last_light_status == "RED" and y1 > (stop_line_y + buffer_zone): 
                        is_violation = True

                if has_crossed:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), veh_color, 2)
                    if tid not in self.counted_ids:
                        self.counted_ids.add(tid)
                        self.stats["Total"] += 1
                        self.stats[label] += 1
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 1)

                if is_violation:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    if tid not in self.violated_ids:
                        self.violated_ids.add(tid)
                        self.stats["Violation"] += 1
                        
                        img_name = f"v_{tid}_{datetime.now().strftime('%H%M%S')}.jpg"
                        cv2.putText(raw_evidence, f"VIOLATION: {label}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                        cv2.rectangle(raw_evidence, (x1, y1), (x2, y2), (0, 0, 255), 3)
                        cv2.imwrite(f"static/evidence/{img_name}", raw_evidence)
                        with sqlite3.connect('traffic.db') as conn:
                            conn.execute("INSERT INTO violations (vehicle_type, plate, time, image_path) VALUES (?,?,?,?)",
                                         (label, "Checking", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"static/evidence/{img_name}"))
                        new_violation = {"type": label}

                cv2.putText(frame, f"{label}", (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, veh_color, 2)

        return frame, new_violation