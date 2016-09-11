import datetime
import imutils
import time
import cv2
 

def get_activity(image,firstFrame):
  min_area = 1000
  firstFrame = None

  activity_label = "Unoccupied"
 
 
  # resize the frame, convert it to grayscale, and blur it
  frame = imutils.resize(image, width=300)
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(gray, (21, 21), 0)

  # compute the absolute difference between the current frame and
  # first frame
  frameDelta = cv2.absdiff(firstFrame, gray)
  thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
  # dilate the thresholded image to fill in holes, then find contours
  # on thresholded image
  thresh = cv2.dilate(thresh, None, iterations=2)
  (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
 
  # loop over the contours
  for c in cnts:
    # if the contour is too small, ignore it
    if cv2.contourArea(c) < min_area:
      continue
 
    # compute the bounding box for the contour, draw it on the frame,
    # and update the text
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    activity_label = "Agitated"


  # draw the text and timestamp on the frame
  cv2.putText(frame, "Customer Status: {}".format(activity_label), (10, 20),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
  cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
return (activity_label, frame)