import cv2
import urllib 
import numpy
import imutils
from emotion_detect import compute_emotion
import copy

class VideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.emotion = -1
        self.activity = 0
        self.firstFrame = None
        self.emotion_counter = 0
        self.people_duration_counter = 0

        #state of the system
        self.state_two_people = False
        self.state_one_is_representative = False

        self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()

        if self.firstFrame is None:
            image = imutils.resize(image, width=300)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            self.firstFrame = copy.deepcopy(gray)

        if self.state_two_people is False:
            if self.check_two_people(image) is True:
                self.state_two_people = True

        if self.state_two_people is True and self.state_one_is_representative is False:
            if self.detect_representative_color(image) is True:
                self.state_one_is_representative = True

        if self.state_one_is_representative is True:
            self.emotion_counter += 1
            if self.emotion_counter%20==0:
                self.emotion  = compute_emotion(image)

        image_marked = self.get_faces(image)

        ret, jpeg = cv2.imencode('.jpg', image_marked)
        return jpeg.tobytes()

    def get_faces(self,image):

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return image

    def get_emotion_value(self):
        # print "self.emotion is",self.emotion
        return self.emotion

    def get_state_two_people(self):
        return self.state_two_people

    def get_state_one_is_representative(self):
        return self.state_one_is_representative

    def check_two_people(self,image):

        min_area = 1200

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(image, width=300)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # compute the absolute difference between the current frame and
        # first frame
        # print "firstframe",self.firstFrame.shape
        # print "gray",gray.shape
        frameDelta = cv2.absdiff(self.firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        valid = 0
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < min_area:
                continue

            (x, y, w, h) = cv2.boundingRect(c)
            if w > 30 and h > 30:
                valid += 1

        if valid >= 2:

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )
            
            if len(faces) > 1:       
                self.people_duration_counter += 1

        print "\n\n\n {0} \n\n\n".format(self.people_duration_counter)

        if self.people_duration_counter > 15:
            print "##############  Two people detected ##############"
            
            self.save_body_proposals(faces,image)

            return True
        else:
            return False

    def save_body_proposals(self,faces,image):
        top2 = []
        for i,e in enumerate(faces):
            (x, y, w, h) = e
            cv2.imwrite("body_test_image"+str(i)+".png",frame[y:y+h, x:x+w])


    def detect_representative_color(self,image):
        print "Representative detected"
        return True
