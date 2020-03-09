# import RPi.GPIO as GPIO
import time

class Car:
   def __init__(self):
      ### Init direction controls ###
      self.DIR_SERVO_PIN = 17
      self.MAX_TURN_DUTY = 11
      self.MIN_TURN_DUTY = 2
      # GPIO.setmode(GPIO.BCM)
      # GPIO.setup(self.DIR_SERVO_PIN, GPIO.OUT)
      # self.dirServo = GPIO.PWM(self.DIR_SERVO_PIN, 50)


   def setSpeed(self):
      pass

   def setDirection(self, direction): #Direction -> Float ranging from -1 to 1
      midDuty = (self.MAX_TURN_DUTY + self.MIN_TURN_DUTY)/2

      transformedDir = (midDuty - self.MIN_TURN_DUTY) * direction
      dutyCycle      = midDuty + transformedDir
      # self.dirServo.ChangeDutyCycle(dutyCycle)

