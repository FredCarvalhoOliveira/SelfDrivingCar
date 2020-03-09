import pygame, sys
import socket
from time import sleep

# setup the pygame window
pygame.init()
window = pygame.display.set_mode((200, 200), 0, 32)

# how many joysticks connected to computer?
joystick_count = pygame.joystick.get_count()
print("There is " + str(joystick_count) + " joystick/s")

if joystick_count == 0:
   # if no joysticks, quit program safely
   print("Error, I did not find any joysticks")
   pygame.quit()
   sys.exit()
else:
   # initialise joystick
   joystick = pygame.joystick.Joystick(0)
   joystick.init()

axis_map = {
   "leftVertical":    1,  # 1, 4
   "rightHorizontal": 4
}

def buildControlMsg(axis_map):
   msg  = ""
   msg += str(joystick.get_axis(axis_map["leftVertical"]) * -1)   + ";    "
   msg += str(joystick.get_axis(axis_map["rightHorizontal"]))
   return msg


# Setup UDP socket
host = '192.168.2.62'  # car local Ip
port = 5005
s = socket.socket(socket.AF_INET,  # Internet
                  socket.SOCK_DGRAM)
print("connecting")
s.connect((host, port))
print("connected")

while True:
   for event in pygame.event.get():
      # loop through events, if window shut down, quit program
      if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()

   # Build and send control message
   msg = buildControlMsg(axis_map)
   # print(msg)
   s.sendall(msg.encode('utf-8'))
