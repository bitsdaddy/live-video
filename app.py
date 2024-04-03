from flask import Flask, render_template, Response, request
import cv2
import base64
import numpy as np

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    frame_data = request.get_json()
    # Decode base64 image data
    img_data = base64.b64decode(frame_data['frame'].split(',')[1])
    # Convert image data to numpy array
    nparr = np.frombuffer(img_data, np.uint8)
    # Decode image
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # Process frame here if needed
    return 'Frame received successfully', 200

if __name__ == "__main__":
    app.run(debug=True)
