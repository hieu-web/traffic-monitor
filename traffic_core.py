import cv2
import sqlite3
import numpy as np
import os
from ultralytics import YOLO
from datetime import datetime

class TrafficCore:
    def __init__(self):
        self.model = YOLO("models/best.pt")
        self.class_names = self.model.names
        self.last_light_status = "UNKNOWN"
        self.light_buffer = [] 
        self.reset_session()

    def reset_session(self):
        self.stats = {"Total": 0, "Violation": 0, "Bus": 0, "Car": 0, "Motorcycle": 0, "Truck": 0}
        self.counted_ids = set()
        self.violated_ids = set()

    def get_light_color(self, roi_img):
        """Bộ lọc 15 frame giúp đèn ổn định tuyệt đối"""
        if roi_img is None or roi_img.size == 0: return "UNKNOWN"
        hsv = cv2.cvtColor(roi_img, cv2.COLOR_BGR2HSV)
        
        # Tăng cường độ nhạy màu đỏ
        mask_r = cv2.addWeighted(cv2.inRange(hsv, np.array([0, 150, 100]), np.array([10, 255, 255])), 1.0, 
                                 cv2.inRange(hsv, np.array([160, 150, 100]), np.array([180, 255, 255])), 1.0, 0)
        mask_g = cv2.inRange(hsv, np.array([40, 100, 100]), np.array([90, 255, 255]))
        
        r_pix, g_pix = cv2.countNonZero(mask_r), cv2.countNonZero(mask_g)
        current = "OFF"
        if r_pix > g_pix and r_pix > 60: current = "RED"
        elif g_pix > r_pix and g_pix > 60: current = "GREEN"
        
        if current != "OFF":
            self.light_buffer.append(current)
            if len(self.light_buffer) > 15: self.light_buffer.pop(0)
            
        return max(set(self.light_buffer), key=self.light_buffer.count) if self.light_buffer else "OFF"

    def process_frame(self, frame, cfg):
        raw_evidence = frame.copy() 
        H, W = frame.shape[:2]
        
        stop_line_y = int(H * float(cfg['stop_line']) / 100)
        rx, ry = int(W * float(cfg['roi_x']) / 100), int(H * float(cfg['roi_y']) / 100)
        rw, rh = int(W * float(cfg['roi_w']) / 100), int(H * float(cfg['roi_h']) / 100)

        roi_light = frame[ry:ry+rh, rx:rx+rw]
        self.last_light_status = self.get_light_color(roi_light)
        
        ui_color = (0, 0, 255) if self.last_light_status == "RED" else (0, 255, 0)
        cv2.rectangle(frame, (rx, ry), (rx + rw, ry + rh), (255, 255, 0), 2)
        cv2.line(frame, (0, stop_line_y), (W, stop_line_y), ui_color, 3)

        results = self.model.track(frame, persist=True, conf=float(cfg['conf_threshold']), verbose=False)
        new_violation = None

        if results and results[0].boxes is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            clss = results[0].boxes.cls.int().cpu().tolist()
            ids = results[0].boxes.id.int().cpu().tolist() if results[0].boxes.id is not None else [None]*len(boxes)

            for box, cls, tid in zip(boxes, clss, ids):
                x1, y1, x2, y2 = map(int, box)
                label = self.class_names[cls].capitalize()
                
                if label in self.stats:
                    if tid is not None and tid not in self.counted_ids:
                        self.counted_ids.add(tid); self.stats["Total"] += 1; self.stats[label] += 1

                    # LOGIC KHẮT KHE NHẤT: Dùng y1 (Mép trên cùng của xe)
                    # Nếu y1 > stop_line_y nghĩa là TOÀN BỘ xe đã nằm dưới vạch kẻ
                    box_color = (0, 255, 0)
                    
                    if self.last_light_status == "RED" and y1 > stop_line_y: 
                        box_color = (0, 0, 255) # Chỉ đổi màu đỏ khi xe đã qua hết vạch
                        if tid is not None and tid not in self.violated_ids:
                            self.violated_ids.add(tid); self.stats["Violation"] += 1
                            img_name = f"v_{tid}_{datetime.now().strftime('%H%M%S')}.jpg"
                            
                            # Vẽ bằng chứng toàn cảnh
                            cv2.rectangle(raw_evidence, (rx, ry), (rx+rw, ry+rh), (0, 0, 255), 4) # Đèn
                            cv2.line(raw_evidence, (0, stop_line_y), (W, stop_line_y), (0, 0, 255), 4) # Vạch
                            cv2.rectangle(raw_evidence, (x1, y1), (x2, y2), (0, 0, 255), 3) # Xe
                            cv2.putText(raw_evidence, "VIOLATION CONFIRMED", (50, 50), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                            
                            cv2.imwrite(f"static/evidence/{img_name}", raw_evidence)
                            self.save_to_db(label, img_name)
                            new_violation = {"type": label, "img": img_name}
                    
                    cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
                    # Chỉ hiện text nếu vi phạm để đỡ rối, hoặc hiện tất cả tùy bạn
                    if box_color == (0, 0, 255):
                         cv2.putText(frame, "VIOLATION", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)
                    else:
                         cv2.putText(frame, f"{label}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)

        return frame, new_violation

    def save_to_db(self, v_type, path):
        conn = sqlite3.connect('traffic.db')
        conn.execute("INSERT INTO violations (vehicle_type, plate, time, image_path) VALUES (?,?,?,?)",
                     (v_type, "CHECKING", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"static/evidence/{path}"))
        conn.commit(); conn.close()