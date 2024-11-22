from flask import Flask, Response, render_template_string
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from libcamera import Transform
import cv2
from io import BytesIO
import numpy as np

import dlib

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
    <h1>Live Camera Stream</h1>
    <img src="/video_feed" width="100%" style="border: 1px solid black;" />
</body>
</html>
"""

# Initialize the camera
camera = Picamera2()
camera.configure(camera.create_video_configuration(transform=Transform(vflip=True), main={"size": (640, 480)}))
camera.set_controls({"AwbEnable": True})  # Enable auto white balance
camera.start()

# Load Dlib's face detector and landmark predictor
detector = dlib_streamer.get_frontal_face_detector()
predictor = dlib_streamer.shape_predictor("shape_predictor_68_face_landmarks.dat")


def detect_and_draw_landmarks(frame):
    """Detect faces and draw landmarks."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for rect in faces:
        # Get landmarks
        landmarks = predictor(gray, rect)
        for i in range(0, 68):  # Loop through each landmark
            x, y = landmarks.part(i).x, landmarks.part(i).y
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)  # Draw a small circle

    return frame

def generate_frames():
    stream = BytesIO()
    while True:
        # Capture a JPEG frame with all processing
        camera.capture_file(stream, format="jpeg")
        stream.seek(0)
        raw_frame = np.frombuffer(stream.read(), dtype=np.uint8)
        stream.seek(0)
        stream.truncate()

        # Decode JPEG into an OpenCV image
        frame = cv2.imdecode(raw_frame, cv2.IMREAD_COLOR)

        # Detect and annotate faces
        annotated_frame = detect_and_draw_faces(frame)

        # Encode frame back to JPEG
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
        app.run(host='0.0.0.0', port=5000, debug=False)
    finally:
        camera.stop()
