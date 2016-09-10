import cv2
import urllib 
import numpy as np

stream=urllib.urlopen('http://192.168.43.50:8080/video')
bytes=''
counter = 0
while counter < 1e3:
    bytes+=stream.read(16384)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    # print 'a',a
    # print 'b',b
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        #print 'jpg',jpg
        bytes= bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
        # print "i",i

        #cv2.imwrite("../output/test_image_rajat.png",i)

        if i is not None:
            print "have data at counter ",counter
            # gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
            resized_i = cv2.resize(i, (400, 400)) 
            cv2.imshow('Video', resized_i)
            cv2.waitKey(1)
            cv2.destroyAllWindows()


    counter += 1


# When everything is done, release the capture
cv2.destroyAllWindows()