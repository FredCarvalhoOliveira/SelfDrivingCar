from carController import CarController

import RPi.GPIO as GPIO
import cv2
import imutils
 
        
car = CarController()
car.openComChannel('192.168.1.3', 5005) #192.168.2.62
car.setupVideoStream('192.168.1.3', 8089)

WIDTH = 100
HEIGHT = int((car.camera.get(cv2.CAP_PROP_FRAME_HEIGHT) * WIDTH) / car.camera.get(cv2.CAP_PROP_FRAME_WIDTH))

while True:

    # Read Camera
    ret, frame   = car.readCamera()
    gray         = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resizedFrame = imutils.resize(gray, WIDTH, HEIGHT)
    car.sendVideoFrame(resizedFrame)

    # Receive controls
    speed, direction = car.receiveAndParseCtrls()

    # Control car
    car.setSpeed(speed)
    car.setDirection(direction)

    if cv2.waitKey(1) & 0xFF == ord('q'):
    	break

car.shutdown()
