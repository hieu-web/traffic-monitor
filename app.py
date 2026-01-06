import os
import cv2
import sqlite3
import pandas as pd
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
from flask_socketio import SocketIO
from traffic_core import TrafficCore
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
socketio = SocketIO(app, cors_allowed_origins="*")
core = TrafficCore()

# Mặc định Confidence 0.7 và thông số ROI
config = {
    "stop_line": 70, "conf_threshold": 0.7,
    "roi_x": 93, "roi_y": 0, "roi_w": 4, "roi_h": 14
}
current_video = "test.mp4"

@app.route('/')
def index():
    return render_template('index.html', current_v=os.path.basename(current_video))

@app.route('/update_config', methods=['POST'])
def update_config():
    global config
    config.update(request.json)
    return jsonify({"status": "success"})

@app.route('/upload_video', methods=['POST'])
def upload_video():
    global current_video
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        current_video = path
        core.reset_session()
    return redirect(url_for('index'))

@app.route('/api/history')
def get_history():
    conn = sqlite3.connect('traffic.db')
    df = pd.read_sql_query("SELECT * FROM violations ORDER BY id DESC", conn)
    conn.close()
    return jsonify(df.to_dict(orient='records'))

@app.route('/history_page')
def history_page(): return render_template('history.html')

def video_stream():
    cap = cv2.VideoCapture(current_video)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.resize(frame, (960, 540))
        processed_frame, violation = core.process_frame(frame, config)
        socketio.emit('update_ui', {'stats': core.stats, 'violation': violation, 'light_status': core.last_light_status})
        _, buffer = cv2.imencode('.jpg', processed_frame)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    os.makedirs("static/evidence", exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    socketio.run(app, debug=True, port=5000)