import cv2 #opencv
import numpy as np

#ready function for read faces and eyes
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

#to turn on the webcam #for first camera we will write (0)
cap = cv2.VideoCapture(0)

while True:
    #First parameter is unimportant -> _,
    _, img = cap.read()
    #img convert to black-gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)

    for (x,y,w,h) in faces:
        #When processing, we process in black and white, and when printing results, we also print in color.
        cv2.rectangle(img, (x,y) , (x+w, y+h), (0,0,255), 6) #4 is thickness
        roi_gray = gray[y:y+h, x:x+w] #region on interest
        roi_color = img[y:y+h, x:x+w]

    cv2.imshow("detected.", img)
    # When the push esc , webcam will be close
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()