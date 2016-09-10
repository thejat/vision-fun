from flask import Flask, render_template, Response, request, stream_with_context, jsonify
from camera import VideoCamera
import numpy
# from camera import IPCamera

import json
from functools import wraps
from flask import redirect, request, current_app

def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f().data) + ')'
            return current_app.response_class(content, mimetype='application/json')
        else:
            return f(*args, **kwargs)
    return decorated_function



app = Flask(__name__)

webcam_capture = VideoCamera()

# ip_capture = IPCamera('http://192.168.43.50:8080/video')

@app.route('/')
@app.route('/live')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        output = webcam_capture.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + output + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    resp = gen(webcam_capture)
    return Response(resp, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/emotion_value')
def emotion_value():
    return Response(webcam_capture.emotion)

@app.route('/test')
@support_jsonp
def test():
    f = {'emotion':numpy.random.randint(0,6)}
    return jsonify(**f)

@app.route('/stream')
def streamed_response():
    def generate():
        yield 'Hello '
        yield 'request.args'
        yield '!'
    return Response(stream_with_context(generate()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



# http://www.chioka.in/python-live-video-streaming-example/