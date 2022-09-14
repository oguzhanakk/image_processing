import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

cap = cv2.VideoCapture(0)

while True:
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 4)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

                              #we use roi_gray here
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3)
        i = 0
        for(x2, y2, w2, h2) in eyes:
            i += 1
            cv2.rectangle(roi_color, (x2, y2), (x2+w2, y2+h2), (0,0,255),2)
            if(i==2):
                break

    cv2.imshow("Capture", img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()