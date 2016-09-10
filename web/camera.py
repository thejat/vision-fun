import cv2
import urllib 
import numpy


class VideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.emotion = 0

    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        self.emotion = self.compute_emotion(image)
        ret, jpeg = cv2.imencode('.jpg', image)
        resized_jpeg = cv2.resize(jpeg, (300, 300)) 
        return resized_jpeg

    def compute_emotion(self,image):
    	return numpy.random.randint(0,6)

    def get_emotion_value(self):
    	return self.emotion