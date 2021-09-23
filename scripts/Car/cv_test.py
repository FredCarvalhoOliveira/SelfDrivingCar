import numpy as np
import imutils
import cv2
import socket
import sys
import pickle
import struct




#context = zmq.Context()
#foot_socket = context.socket(zmq.PUB)
#foot_socket.connect('tcp://localhost:5555') 
#foot_socket.connect('tcp://localhost:5555')


clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
clientSock.connect(('192.168.1.4', 8089))


cap = cv2.VideoCapture(0)

WIDTH = 100
HEIGHT = int((cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * WIDTH) / cap.get(cv2.CAP_PROP_FRAME_WIDTH))

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    resizedFrame = imutils.resize(gray, WIDTH, HEIGHT)
    
    data = pickle.dumps(resizedFrame)
    msg_size = struct.pack("L", len(data))
    
    clientSock.sendall(msg_size + data)
    
    #frame = cv2.resize(frame, (640, 480))
    #encoded, buffer = cv2.imencode('.jpg', frame)
    #jpg_as_text = base64.b64encode(buffer)
    #foot_socket.send(jpg_as_text)
    
    
    
    #cv2.imshow('Original', frame)
    #cv2.imshow('Resized', resizedFrame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

