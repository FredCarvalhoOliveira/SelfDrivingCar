import RPi.GPIO as GPIO
import time

print("Hello Raspberry!")

DIR_SERVO_PIN = 17
FORWARD_PIN   = 27
BACK_PIN      = 22

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_SERVO_PIN, GPIO.OUT)
GPIO.setup(FORWARD_PIN, GPIO.OUT)

#p = GPIO.PWM(DIR_SERVO_PIN, 50)
p = GPIO.PWM(DIR_SERVO_PIN, 50)


p.start(20)

try:
    while True:
        speed = int(input("Duty = "))
        p.ChangeDutyCycle(speed)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
    
p.stop()
GPIO.cleanup()    