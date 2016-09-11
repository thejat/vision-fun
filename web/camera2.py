import cv2
import urllib 
import numpy


class IPCamera(object):

    def __init__(self,ip=None):

        if ip is None:
            print "No ip provided!"
            return NotImplementedError #TBD some other error
        else:
            self.stream=urllib.urlopen(ip)
            self.bytes=''

        self.emotion = 0
        self.activity = 0

    def compute_emotion(self,image):
        return numpy.random.randint(0,6)

    def compute_activity(self,image):
        return numpy.random.randint(0,6)

    def get_emotion_value(self):
        print "self.emotion is",self.emotion
        return self.emotion

    def get_frame(self):
        counter  = 0
        while counter < 1e3:
            self.bytes+=self.stream.read(16384)
            a = self.bytes.find('\xff\xd8')
            b = self.bytes.find('\xff\xd9')
            # print 'a',a
            # print 'b',b
            if a!=-1 and b!=-1:
                jpg = self.bytes[a:b+2]
                #print 'jpg',jpg
                self.bytes= self.bytes[b+2:]
                i = cv2.imdecode(numpy.fromstring(jpg, dtype=numpy.uint8),cv2.CV_LOAD_IMAGE_COLOR)
                # print "i",i

                if i is not None:
                    resized_i = cv2.resize(i, (400, 400))

                    self.emotion  = self.compute_emotion(resized_i)
                    self.activity = self.compute_activity(resized_i)

                    ret, jpeg = cv2.imencode('.jpg', i)
                    cv2.destroyAllWindows()
                    return jpeg.tobytes()

            counter += 1
        print "Error. Could not get a frame!"
        return None