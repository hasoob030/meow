from flask import Flask, Response
import mss
import threading

app = Flask(__name__)
sct = mss.mss()

def generate_frames():
    monitor = sct.monitors[1]
    while True:
        img = sct.grab(monitor)
        img_bytes = img.rgb
        frame = (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n')
        yield frame

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return """
    <html>
        <head>
            <title>Screen Stream</title>
        </head>
        <body>
            <h1>Live Screen Stream</h1>
            <img src="/video_feed" style="width:100%; max-width: 800px;"/>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
