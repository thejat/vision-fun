# import cv2
# import openface
# import dlib
# import matplotlib


# def plot_dlib_facial_landmarks(img, landmarks):
#     for point in landmarks:
#         cv2.circle(img, point, 2, (0,0,255), 2)

# class FaceAnalyzer:
#     def __init__(self):
#         self.img_dim = 96
#         self.align = openface.AlignDlib("/Users/karan/Developement/shape_predictor_68_face_landmarks.dat")
#         # self.net = openface.TorchNeuralNet("/Users/karan/Developement/openface/models/openface/nn4.def.lua", img_dim)

#     def openface_analyze_face(self, image, bounding_box):
#         dlib_bb = dlib.rectangle(bounding_box[0], bounding_box[1], bounding_box[2], bounding_box[3])
#         alignedFace = self.align.align(self.img_dim, image, dlib_bb, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
#         return alignedFace

#     def openface_landmark_detect(self, image, bounding_box):
#         dlib_bb = dlib.rectangle(bounding_box[0], bounding_box[1], bounding_box[2], bounding_box[3])
#         landmarks = self.align.findLandmarks(image, dlib_bb)
#         return landmarks


if __name__ == "__main__":

    import numpy as np
    import cv2

    import urllib

    # stream = urllib.urlopen('http://localhost:8080/frame.mjpg')
    stream = urllib.urlopen('http://192.168.137.170:8080/video/frame.mjpg')
    bytes = ''

    bytes += stream.read(16384)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
        cv2.imwrite('temp.png', i)
        cv2.startWindowThread()
        cv2.namedWindow("Preview")
        cv2.imshow('Preview', i)
        # cv2.show('i', i)
        cv2.waitKey()
        if cv2.waitKey(10) == 27:
            exit(0)    

    # while True:
    #     bytes += stream.read(16384)
    #     a = bytes.find('\xff\xd8')
    #     b = bytes.find('\xff\xd9')
    #     if a != -1 and b != -1:
    #         jpg = bytes[a:b+2]
    #         bytes = bytes[b+2:]
    #         i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
    #         cv2.imshow('i',i)
    #         if cv2.waitKey(1) == 27:
    #             exit(0)    



    # SKIP_FRAMES = 4
    # cap = cv2.VideoCapture(0)
    # face_detector = dlib.get_frontal_face_detector()
    # detect_face = False
    # frame_counter = 0
    # bb = ()
    # bb_draw = []
    # fa = FaceAnalyzer()
    # while(True):
    #     # Capture frame-by-frame
    #     ret, frame = cap.read()
    #     ratio_scale = .5

    #     if ret:
    #         # Our operations on the frame come here
    #         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #         gray_resize = cv2.resize(gray, dsize=(int(gray.shape[1]*ratio_scale),int(gray.shape[0]*ratio_scale)))
    #         if(detect_face):
    #             dets = face_detector(gray_resize, 1)
    #             detect_face = False
    #             for i, d in enumerate(dets):
    #                 bb = (d.left(), d.top(), d.right(), d.bottom())

    #         if(len(bb) == 4):
    #             ratio = 1./ratio_scale
    #             bb_draw = [int(x*ratio) for x in bb]

    #             aligned_face = fa.openface_analyze_face(frame, bb_draw)
    #             landmarks = fa.openface_landmark_detect(frame, bb_draw)
    #             plot_dlib_facial_landmarks(frame, landmarks)
    #             cv2.rectangle(gray, (bb_draw[0],bb_draw[1]), (bb_draw[2], bb_draw[3]), (255,0,0), 4)
    #             # Display the resulting frame
    #         cv2.imshow('frame',frame)

    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break

    #         # if cv2.waitKey(1) & 0xFF == ord('c'):
    #         try:
    #             if(aligned_face.shape[0] > 0 & aligned_face.shape[1] > 0):
    #                 cv2.imshow('face', aligned_face)
    #         except:
    #             print "Name error"

    #         frame_counter = frame_counter + 1
    #         if(frame_counter % SKIP_FRAMES == 0):
    #             detect_face = True
    #             frame_counter = 0
    #             # When everything done, release the capture
    # cap.release()
    # cv2.destroyAllWindows()
