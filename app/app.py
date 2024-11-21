from flask import Flask, Response, render_template_string
from picamera2 import Picamera2
from libcamera import Transform
import cv2
import numpy as np
import dlib
from io import BytesIO

app = Flask(__name__)

# HTML Template for the web page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raspberry Pi Camera Stream</title>
</head>
<body>
    <h1>Live Camera Stream with Face Detection</h1>
    <img src="/video_feed" width="100%" style="border: 1px solid black;" />
</body>
</html>
"""

# Initialize the camera
camera = Picamera2()
camera.configure(camera.create_video_configuration(transform=Transform(vflip=True), main={"size": (640, 480)}))
camera.start()

# Initialize dlib's face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(dlib.shape_predictor("shape_predictor_68_face_landmarks.dat"))

def detect_and_draw_faces(frame):
    """Detect faces and draw bounding boxes and landmarks."""
    # Convert to grayscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = detector(gray)
    for face in faces:
        # Draw bounding box
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Detect landmarks
        landmarks = predictor(gray, face)
        for n in range(68):  # Draw points for 68 landmarks
            x, y = landmarks.part(n).x, landmarks.part(n).y
            cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)

    return frame

def generate_frames():
    while True:
        # Capture a frame
        raw_frame = camera.capture_array()
        # Detect and annotate faces
        annotated_frame = detect_and_draw_faces(raw_frame)
        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()
        # Yield the frame as part of the MJPEG stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        camera.stop()
