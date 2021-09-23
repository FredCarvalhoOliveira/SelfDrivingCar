import RPi.GPIO as GPIO
import time
import socket

class CarController():
    def __init__(self):
        self.DIR_SERVO_PIN = 17
        self.FORWARD_PIN   = 27
        self.BACK_PIN      = 22
        
        self.MAX_PWM_LEFT  = 5
        self.MAX_PWM_RIGHT = 8
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIR_SERVO_PIN, GPIO.OUT)
        GPIO.setup(self.FORWARD_PIN, GPIO.OUT)
        GPIO.setup(self.BACK_PIN, GPIO.OUT)
        
        self.dirSignal = GPIO.PWM(self.DIR_SERVO_PIN, 50)
        
        self.forwardSignal  = GPIO.PWM(self.FORWARD_PIN, 100)
        self.backwardSignal = GPIO.PWM(self.BACK_PIN, 100)
        
        
    def openComChannel(host, port):
        s = socket.socket(socket.AF_INET, #Internet
                          socket.SOCK_DGRAM) #UDP?
        s.bind((host, port))
        
        
    
    #Speed = 0 - 100
    def setSpeed(self, speed, reverse=False):
        if reverse:
            self.forwardSignal.stop()
            self.backwardSignal.start(speed)
        else:
            self.backwardSignal.stop()
            self.forwardSignal.start(speed)
            
    #TODO       turn val = -1 Left to 1 Right 
    def setDirection(self, turnVal):
        inputRange  = 1 - (-1)
        outputRange = self.MAX_PWM_RIGHT - self.MAX_PWM_LEFT
        
        duty = (((turnVal - (-1)) * outputRange) / inputRange) + self.MAX_PWM_LEFT
        
        self.dirSignal.ChangeDutyCycle(duty)
    
    
    
car = CarController()

try:
    while True:
        speed = int(input("Duty = "))
        print(speed)
        if(speed >= 0):
            car.setSpeed(speed, False)
        else:
            car.setSpeed(abs(speed), True)
        
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
    
p.stop()
GPIO.cleanup() 
