import numpy as np
import imutils
import cv2
import socket
import sys
import pickle
import struct
import picamera



cap = cv2.VideoCapture(0)

WIDTH = 100
HEIGHT = int((cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * WIDTH) / cap.get(cv2.CAP_PROP_FRAME_WIDTH))

while(True):
    ret, frame = cap.read()
    
    cv2.imshow('Original', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


