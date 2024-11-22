from flask import Flask, Response, render_template_string
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from libcamera import Transform
import cv2
from io import BytesIO
import numpy as np

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

# Provide the correct path to the Haar cascade file
face_cascade = cv2.CascadeClassifier('app/ml_data/haarcascade_frontalface_default.xml')

# Check if the cascade file loaded correctly
if face_cascade.empty():
    raise IOError("Failed to load Haar cascade file. Check the file path!")

def detect_and_draw_faces(frame):
    """Detect faces and draw bounding boxes."""
    # Convert to grayscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        # Draw bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Add placeholder for landmarks (optional feature points for demonstration)
        for i in range(5):  # Example points
            cv2.circle(frame, (x + int(w * (i + 1) / 6), y + h // 2), 5, (255, 0, 0), -1)

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
