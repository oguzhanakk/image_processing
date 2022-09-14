import cv2 #opencv
import numpy as np

def detectFaces_EyesFromImage(image):
    # ready function for read face and eyes
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

    #Read to image
    img = cv2.imread(image)

    #Converts the image to black-white because computer read to fast while image black-white
    gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #ready function
    faces = face_cascade.detectMultiScale(gray_scale, 1.2, 4)

    #For reads all the face
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 4)
        roi_gray = gray_scale[y:y+h, x:x+w] #Region on interest
        roi_color = img[y:y+h, x:x+w]
        # For each face , shows all eyes
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for(x2,y2,w2,h2) in eyes:                               #color RGB code
            cv2.rectangle(roi_color, (x2,y2), (x2+w2 , y2+h2), (0,255,0),2)

    #Resize img
    img = cv2.resize(img, (500, 500))

    cv2.imshow("Faces and eyes detected", img)
    cv2.waitKey()
    cv2.destroyAllWindows()

detectFaces_EyesFromImage("Selfie.jfif")


