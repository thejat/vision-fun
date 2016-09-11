import cv2
import urllib 
import numpy
from emotion_detect import compute_emotion
from activity_detect import compute_activity

class VideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.emotion = 0
        self.activity = 0
        self.counter = 0
        self.firstFrame = None

        #state of the system
        self.state_two_people = False
        self.one_is_representative = False
        self.do_scene_emotion_detection = False

    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()

        if self.firstFrame is None:
            self.firstFrame = cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),(21, 21), 0)

        self.counter += 1
        if self.counter%10==0:
            self.emotion  = compute_emotion(image)
            self.activity = compute_activity(image,self.firstFrame)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def compute_emotion1(self,image):
    	return numpy.random.randint(0,6)

    def compute_activity1(self,image,firstFrame):
        return numpy.random.randint(0,6)

    def get_emotion_value(self):
        print "self.emotion is",self.emotion
        return self.emotion

