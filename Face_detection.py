import numpy as np
import cv2
import matplotlib.pyplot as plt
import time

def detectFromImage(image):
    #ready function for read face
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    #Read to image
    img = cv2.imread(image)
    #Converts the image to black-white because computer read to fast while image black-white
    gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #ready function
    faces = face_cascade.detectMultiScale(gray_scale, 1.2, 3)

    #For reads all the face
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 4)

    #Resize
    img = cv2.resize(img, (500,500))

    #Last shows
    cv2.imshow("baslik", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

detectFromImage("Selfie.jfif")
detectFromImage("OgiCengo.jpeg")