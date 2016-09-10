from flask import Flask, render_template,jsonify, send_file
from camera import VideoCamera
import numpy, cv2
from io import StringIO
# from camera import IPCamera

app = Flask(__name__)

webcam_capture = VideoCamera()

# ip_capture = IPCamera('http://192.168.43.50:8080/video')

@app.route('/')
@app.route('/live')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    frame = webcam_capture.get_frame()
    img_io = StringIO()
    cv2.imwrite(img_io, cv2.imencode('.jpg', frame)[1].tostring())
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route('/emotion_value')
def emotion_value():
    return jsonify({'emotion':webcam_capture.get_emotion_value()})

@app.route('/test')
def test():
    f = {'emotion':numpy.random.randint(0,6)}
    return jsonify(**f)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



# http://www.chioka.in/python-live-video-streaming-example/