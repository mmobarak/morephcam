from flask import Flask, Response, render_template_string
from picamera2 import Picamera2
# from picamera2.encoders import JpegEncoder
# from picamera2.outputs import FileOutput
from libcamera import Transform
import cv2
from io import BytesIO
import numpy as np
import mediapipe as mp


app = Flask(__name__)

# HTML Template for the web page
HTML_TEMPLATE1 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raspberry Pi Camera Stream</title>
</head>
<body>
    <img src="/video_feed" width="100%" style="border: 1px solid black;" />
    <img src="/video_feed" width="100%" style="border: 1px solid black;" />
</body>
</html>
"""

HTML_TEMPLATE2 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        .container {
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin: 2;
        }
        .container img {
            max-width: 50%; /* Adjust the size of the images */
            height: auto;
            border: 2px solid #ccc;
            border-radius: 8px;
        }
        button {
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
        }
        button:disabled {
            background-color: #aaa;
            cursor: not-allowed;
        }
    </style>
</head>
<body>

    <div class="container">
        <img src="/video_feed" />
        <img src="/video_feed" />
    </div>

</body>
</html>
"""

# Initialize the camera
camera = Picamera2()
camera.configure(camera.create_video_configuration(transform=Transform(vflip=True), main={"size": (640, 480)}))
camera.set_controls({"AwbEnable": True})  # Enable auto white balance
camera.start()


# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=10, min_detection_confidence=0.5)





def detect_faces_and_landmarks(frame):
    """Detect faces and landmarks using MediaPipe."""
    # Convert to RGB as MediaPipe expects RGB input
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces and landmarks
    results = face_mesh.process(rgb_frame)

    # Draw landmarks on the frame
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for landmark in face_landmarks.landmark:
                # Get landmark coordinates
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                # Draw a small circle for each landmark
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
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
        annotated_frame = detect_faces_and_landmarks(frame)

        # Encode frame back to JPEG
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()

        # Yield the frame as part of the MJPEG stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE2)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    finally:
        camera.stop()
