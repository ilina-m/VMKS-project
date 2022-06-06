from tkinter import Frame, font
from unicodedata import name
import numpy as np
import face_recognition as fr
import cv2
from numpy.matrixlib.defmatrix import mat
from cv2 import rotate
from pyfirmata import Arduino, SERVO, util
from time import sleep


video_capture = cv2.VideoCapture(0)

ilina_image = fr.load_image_file("ilina.jpg")
ilina_face_encoding =  fr.face_encodings(ilina_image)[0]

known_face_encodings = [ilina_face_encoding]
known_face_names = ["Ilina"]

file = open("name.txt", "w")

while True:
    ret, frame = video_capture.read()

    rgb_frame = frame [:, :, ::-1]

    face_locations = fr.face_locations(rgb_frame)
    face_encodings = fr.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations,face_encodings):

        matches = fr.compare_faces(known_face_encodings, face_encoding)

        name = "unknown"

        face_distances = fr.face_distance(known_face_encodings, face_encoding)

        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            file.write(name + "\n")
            file.close
            
        elif name == "unknown":
            file.write(name + "\n")
            file.close
            
        file.close
        cv2.rectangle(frame, (left,top), (right, bottom), (0,0,255), 2)

        cv2.rectangle(frame, (left, bottom -35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.putText(frame, name, (left +6, bottom -6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow("Webcam_facerecognition", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

port = 'COM3'
pin=10
board=Arduino(port)

board.digital[pin].mode=SERVO


def rotateservo(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.015)

file = open("name.txt", "r")
name1 = file.readline()
file.close

if "unknown" in name1:
    print("You're %s! You shall not pass!" % name1)
        
else:
    print("Welcome %s!" % name1)   
    for i in range(0,90):
        rotateservo(pin, i)

f = open('name.txt', 'r+')
f.truncate(0) # need '0' when using r+



