import socket
import struct
import pickle


class VideoStreamReceiver:
   def __init__(self):
      self.receiverSocket = None
      self.streamSocket = None
      self.data = b''
      self.payload_size = struct.calcsize("L")


   def setupVideoStreamReceiver(self, host, port):
      self.receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.receiverSocket.bind((host, port))
      print('>> VideoStream Socket created')
      self.receiverSocket.listen(1)
      print('>> VideoStream Socket waiting for connections...')
      conn, addr = self.receiverSocket.accept()
      self.streamSocket = conn
      print('>> VideoStream connected to ' + str(addr))


   def recvVideoFrame(self):
      # Retrieve message size
      while len(self.data) < self.payload_size:
         self.data += self.streamSocket.recv(4096)

      packed_msg_size = self.data[:self.payload_size]
      self.data = self.data[self.payload_size:]
      msg_size = struct.unpack("L", packed_msg_size)[0]  ### CHANGED

      # Retrieve all data based on message size
      while len(self.data) < msg_size:
         self.data += self.streamSocket.recv(4096)

      frame_data = self.data[:msg_size]
      self.data = self.data[msg_size:]

      # Extract frame
      frame = pickle.loads(frame_data)
      return frame

   def endConnection(self):
      self.streamSocket.close()