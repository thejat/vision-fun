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
        self.emotion = self.get_emotion(image)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_emotion(self,image):
    	return numpy.random.randint(0,6)