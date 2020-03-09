import socket
from scripts.carController import Car

print(socket.gethostname())

host = '193.137.131.4'  # socket.gethostname()
port = 5000

s = socket.socket(socket.AF_INET, # Internet
                  socket.SOCK_DGRAM)
s.bind((host, port))

car = Car()

while True:
   controls = (s.recv(1024)).decode('utf_8')
   print("Data Received " + str(controls))

   if not controls:
      break

   controls  = controls.split(';')
   print(controls)
   speed     = float(controls[0])
   direction = float(controls[1])

   car.setDirection(direction)

print("Connection closed")
s.close()