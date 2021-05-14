import pygame
import sys
import socket

class RemoteController:
   def __init__(self):
      pygame.init()
      self.sock = None
      self.remoteCtrlSocket = None
      self.controller = None
      self.axis_map = { "leftVertical":    1,  # 1, 4  PS4 1, 2
                        "rightHorizontal": 2}

      # how many joysticks connected to computer?
      controller_count = pygame.joystick.get_count()
      print("There is " + str(controller_count) + " controller/s")
      if controller_count == 0:
         print("Error, I did not find any controllers")
         pygame.quit()
      else:
         # initialise controller
         self.controller = pygame.joystick.Joystick(0)
         self.controller.init()

   def setupCommChannel(self, host, port):
      self.sock = socket.socket()
      self.sock.bind((host, port))
      print('>> RemoteControl Socket created')
      self.sock.listen(1)
      print('>> RemoteControl Socket waiting for connections...')
      self.remoteCtrlSocket, addr = self.sock.accept()
      print('>> RemoteControl connected to ' + str(addr))

   def readJoysticks(self):
      pygame.event.get()
      leftVertical    = self.controller.get_axis(self.axis_map["leftVertical"]) * -1
      rightHorizontal = self.controller.get_axis(self.axis_map["rightHorizontal"])
      return float("%.3f" % leftVertical), float("%.3f" % rightHorizontal)

   def sendCommands(self, leftVertical, rightHorizontal, messageSize=13):
      msg = self.__buildControlMsg(leftVertical, rightHorizontal)
      msg = self.__formatMsg(msg, messageSize)
      self.remoteCtrlSocket.send(msg)

   def __buildControlMsg(self, leftVertical, rightHorizontal):
      msg = ""
      msg += str(leftVertical) + ";"
      msg += str(rightHorizontal)
      return msg

   #  Adds padding \0 to keep message size constant
   def __formatMsg(self, msg, messageSize):
      byteArray = msg.encode('utf-8') + bytes(chr(0), 'ascii') * (messageSize - len(msg))
      return byteArray