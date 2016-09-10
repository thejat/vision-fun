import cv2
import urllib 
import numpy as np


class IPCamera(object):

    def __init__(self,ip=None):

        if ip is None:
            print "No ip provided!"
            return NotImplementedError #TBD some other error
        else:
            self.stream=urllib.urlopen(ip)
            self.bytes=''

    # def __del__(self):

    def get_frame(self):

        while counter < 1e3:
            self.bytes+=self.stream.read(16384)
            a = self.bytes.find('\xff\xd8')
            b = self.bytes.find('\xff\xd9')
            # print 'a',a
            # print 'b',b
            if a!=-1 and b!=-1:
                jpg = bytes[a:b+2]
                #print 'jpg',jpg
                bytes= bytes[b+2:]
                i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
                # print "i",i

                if i is not None:
                    resized_i = cv2.resize(i, (400, 400)) 
                    ret, jpeg = cv2.imencode('.jpg', i)
                    cv2.destroyAllWindows()
                    return jpeg.tobytes()

            counter += 1
        print "Error. Could not get a frame!"
        return None