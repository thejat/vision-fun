import math
import pdb
# import openface
import cv2
import time
import dlib
import os
import pandas as pd
import numpy as np
import pickle

detector = dlib.get_frontal_face_detector() #Face detector
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") #Landmark identifier. 
clf_model = pickle.load(open("emotion_model.pkl","rb"))

def compute_emotion(image):
    face_features = get_landmark_features(image)
    print "face_features dimension:      ", face_features.shape
    if face_features == 'error':
        emotion = -1
    else:
    #try:
        emotion = clf_model.predict(face_features)[0]
        #pdb.set_trace()
        if(emotion == 0 or emotion == 1 or emotion == 2  or emotion == 4 ):
            emotion = 2    
    #except:
        # print "exception happened"
        #pdb.set_trace()
        # emotion = -1
    return emotion    



def get_landmark_features(img):
    img = img.astype(np.uint8)
    #predictor = dlib.shape_predictor("/Users/karan/Developement/shape_predictor_68_face_landmarks.dat") #Landmark identifier. Set the filename to whatever you named the downloaded file

    detections = detector(img, 1) #Detect the faces in the image

    # plot_dlib_facial_landmarks(img, detections)
    pts_x = []
    pts_y = []
    landmarks_vectorised = []
    #pdb.set_trace()
    for k,d in enumerate(detections): #For each detected face
        #pdb.set_trace()
        shape = predictor(img, d) #Get coordinates
        for i in range(56,68): #There are 68 landmark points on each face
            pts_x.append(shape.part(i).x)
            pts_y.append(shape.part(i).y)
            #cv2.circle(img, (shape.part(i).x, shape.part(i).y), 1, (0,0,255), thickness=1) #For each point, draw a red circle with thickness2 on the original frame
        # pts_x = np.array(pts_x)
        # pts_y = np.array(pts_y)

        xmean = np.mean(pts_x) #Get the mean of both axes to determine centre of gravity
        ymean = np.mean(pts_y)
        xcentral = [(x-xmean) for x in pts_x] #get distance between each point and the central point in both axes
        ycentral = [(y-ymean) for y in pts_y]

        for x, y, w, z in zip(xcentral, ycentral, pts_x, pts_y):
            landmarks_vectorised.append(x)
            landmarks_vectorised.append(y)
            meannp = np.asarray((ymean,xmean))
            coornp = np.asarray((z,w))
            dist = np.linalg.norm(coornp-meannp)
            anglerelative = (math.atan((z-ymean)/(w-xmean))*180/math.pi)
            landmarks_vectorised.append(dist)
            landmarks_vectorised.append(anglerelative)

        break

    if len(detections) < 1: 
        landmarks_vectorised = 'error'
    return np.nan_to_num(np.array(landmarks_vectorised))    