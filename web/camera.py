import cv2
import urllib 
import numpy

class VideoCamera(object):

    def __init__(self,db):
        self.video = cv2.VideoCapture(0)
        self.emotion = 0
        self.activity = 0
        self.db = db

    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        self.emotion  = self.compute_emotion(image)
        self.activity = self.compute_activity(image)

        # self.write_to_db()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def compute_emotion(self,image):
    	return numpy.random.randint(0,6)

    def compute_activity(self,image):
        return numpy.random.randint(0,6)

    def write_to_db(self):
        cursor = self.db.cursor()
        cursor.execute('''INSERT INTO users(emotion,activity)
                  VALUES(?,?)''', (str(self.emotion),str(self.activity)))

        self.db.commit()

    def get_emotion_value(self):
        print "self.emotion is",self.emotion
        return self.emotion

