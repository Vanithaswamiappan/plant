import os
import cv2
import uuid
import shutil
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from ultralytics import YOLO
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'C:/Users/Lenovo/Downloads/ROADONESIDE4.mp4'
OUTPUT_FOLDER = 'C:/Users/Lenovo/Downloads/output.mp4'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
model = YOLO("yolov8n.pt")  # Choose any YOLOv8 variant

zones = {
    "Entry": ((50, 50), (500, 400)),
    
}
output_path='C:/Users/Lenovo/Downloads/output.mp4'
def process_video(filepath, output_path):
    cap = cv2.VideoCapture(filepath)
    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = int(cap.get(5))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    tracker = {}
    counters = {
        'total': set(),
        'Entry': 0,
       
    }
    object_positions = {}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.track(frame, persist=True, tracker="bytetrack.yaml")
        if results[0].boxes.id is None:
            out.write(frame)
            continue

        ids = results[0].boxes.id.cpu().numpy().astype(int)
        boxes = results[0].boxes.xyxy.cpu().numpy()

        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box.astype(int)
            obj_id = ids[i]
            cx, cy = int((x1 + x2)/2), int((y1 + y2)/2)

            counters['total'].add(obj_id)

            for zone_name, (top_left, bottom_right) in zones.items():
                if top_left[0] < cx < bottom_right[0] and top_left[1] < cy < bottom_right[1]:
                    counters[zone_name] += 1

            if obj_id not in object_positions:
                object_positions[obj_id] = [(cx, cy)]
            else:
                object_positions[obj_id].append((cx, cy))

            speed = 0
            if len(object_positions[obj_id]) > 1:
                dx = object_positions[obj_id][-1][0] - object_positions[obj_id][-2][0]
                dy = object_positions[obj_id][-1][1] - object_positions[obj_id][-2][1]
                speed = np.sqrt(dx**2 + dy**2)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'ID: {obj_id} Spd:{speed:.1f}', (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        for zone_name, (top_left, bottom_right) in zones.items():
            cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 2)
            cv2.putText(frame, zone_name.upper(), (top_left[0], top_left[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

        out.write(frame)

    cap.release()
    out.release()
    return {
        'total': len(counters['total']),
        'Entry': counters['Entry'],
        
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video = request.files['video']
        if video.filename == '':
            return redirect(request.url)
        filename = str(uuid.uuid4()) + '.mp4'
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_path = os.path.join(OUTPUT_FOLDER, filename)
        video.save(input_path)
        stats = process_video(input_path, output_path)
        return redirect(url_for('results', filename=filename, **stats))
    return render_template('index.html')

@app.route('/results/<filename>')
def results(filename):
    stats = {
        'filename': filename,
        'total': request.args.get('total'),
        'Entry': request.args.get('Entry'),
        
    }
    return render_template('results.html', **stats)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
