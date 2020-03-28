from carController import CarController

import RPi.GPIO as GPIO
import time
import cv2

    
car = CarController()
car.openComChannel('192.168.2.62', 5005)

while True:
    
    ret, frame = car.readCamera()
    
    speed, direction = car.receiveAndParseCtrls()
    
    car.setSpeed(speed)
    car.setDirection(direction)
    #print(str(speed) + "   " + str(direction))
    
    cv2.imshow('Car Vision', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
car.shutdown()    