from flask import Flask, render_template, Response
from streamlit import to_streamlit
import cv2

app = Flask(__name__)

def generate_frames():
    camera = cv2.VideoCapture(0)
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

@app.route('/streamlit_camera')
def streamlit_camera():
    streamlit_app = """
    import streamlit as st
    from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

    class VideoTransformer(VideoTransformerBase):
        def transform(self, frame):
            # Do any processing of the frame here
            return frame

    def main():
        st.title('Streamlit Webcam')

        webrtc_ctx = webrtc_streamer(key='example', video_transformer_factory=VideoTransformer)

    if __name__ == '__main__':
        main()
    """
    # Render the Streamlit app within a Flask route
    return to_streamlit(streamlit_app)

if __name__ == "__main__":
    app.run(debug=True)
