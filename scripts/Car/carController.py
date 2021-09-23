import RPi.GPIO as GPIO
import time
import socket
import cv2
import struct
import pickle

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
        self.dirSignal.start(20) #refactor this
        
        self.forwardSignal  = GPIO.PWM(self.FORWARD_PIN, 100)
        self.backwardSignal = GPIO.PWM(self.BACK_PIN, 100)
        
        self.sock = None
        self.camera = cv2.VideoCapture(0)
        
        self.videoSocket = None
        
        
        
    def setupVideoStream(self, serverIp, port):
        self.videoSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.videoSocket.connect((serverIp, port))
        print(self.videoSocket)
    
    def sendVideoFrame(self, frame):
        data     = pickle.dumps(frame)
        msg_size = struct.pack("L", len(data))
        self.videoSocket.sendall(msg_size + data)
    
    
    '''
    Opens UDP socket
    host - (string) car ip
    port - (int) desired port
    '''
    def openComChannel(self, host, port):
        #self.sock = socket.socket(socket.AF_INET, #Internet
        #                  socket.SOCK_DGRAM) #UDP?
        #self.sock.bind((host, port))
        self.sock = socket.socket()
        self.sock.connect((host, port))
        
        
    '''
    Reads from Camera
    returns (ret, frame)
    '''
    def readCamera(self):
        ret, frame = self.camera.read()
        return ret, frame
        
        
    '''
TODO SOLVE PROBLEM HERE
    Receives control data from socket and parses the data
    returns the tuple (speed, direction)
    speed     - float (-1, 1)
    direction - float (-1, 1)
    '''
    def receiveAndParseCtrls(self, messageSize=13):
        controls = self.sock.recv(messageSize).decode('utf_8').strip('\0')
        if not controls:
            return None
        else:
            controls  = controls.split(';')
            speed     = float(controls[0])
            direction = float(controls[1]) 
        return speed, direction
        
       
    '''
    Sets the car speed
    speed - (float) -1 to 1
     1 = Full Forward Throtle
    -1 = Full Backward Throtle
    '''
    def setSpeed(self, speed):
        speed *= 100
        
        if speed < 0:
            speed *= -1
            self.forwardSignal.stop()
            self.backwardSignal.start(speed)
        else:
            self.backwardSignal.stop()
            self.forwardSignal.start(speed)
            
            
    '''
    Sets the car direction
    turnVal - (float) -1 to 1
     1 = Full Right Turn
    -1 = Full Left Turn
    '''
    def setDirection(self, turnVal):
        inputRange  = 1 - (-1)
        outputRange = self.MAX_PWM_RIGHT - self.MAX_PWM_LEFT
        
        duty = (((turnVal - (-1)) * outputRange) / inputRange) + self.MAX_PWM_LEFT
        self.dirSignal.ChangeDutyCycle(duty)
    
    '''
    Closes all car systems
    '''
    def shutdown(self):
        self.camera.release()
        self.forwardSignal.stop()
        self.backwardSignal.stop()
        self.dirSignal.stop()
        GPIO.cleanup()
        #close socket TODO
        
        
    
#car = CarController()

#try:
 #   while True:
  #      speed = int(input("Duty = "))
    #    print(speed)
   #     if(speed >= 0):
      #      car.setSpeed(speed, False)
     #   else:
       #     car.setSpeed(abs(speed), True)
        
#except KeyboardInterrupt:
 #   p.stop()
  #  GPIO.cleanup()
    
#p.stop()
#GPIO.cleanup() 