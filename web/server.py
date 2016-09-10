from flask import Flask, render_template, Response, jsonify
import sqlite3
from camera import VideoCamera
# from camera import IPCamera

app = Flask(__name__)



db = sqlite3.connect('mydb')
cursor = db.cursor()
cursor.execute('''DROP TABLE users''')
db.commit()
cursor.execute('''
    CREATE TABLE users(id INTEGER PRIMARY KEY, emotion TEXT, activity TEXT)
''')
db.commit()

webcam_capture = VideoCamera(db)


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


@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/emotion_value')
def emotion_value():
    print "emotion value GET query happened"
    return jsonify({'emotion':webcam_capture.get_emotion_value()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True,threaded=True)



# http://www.chioka.in/python-live-video-streaming-example/