from datetime import datetime
import time

class TimeAnalisis:
   def __init__(self):
      self.timeRegister = []
      self.startTime = None
      self.endTime   = None

   def startTimer(self):
      self.startTime = time.time()

   def stopTimer(self):
      self.endTime = time.time()

   def registerTime(self, timeElapsed):
      self.timeRegister.append(timeElapsed)

   def getTimeElapsed(self):
      # Returns time elapsed in miliseconds
      return (self.endTime - self.startTime)*1000

   def getMeanTimeElapsed(self):
      return sum(self.timeRegister)/len(self.timeRegister)


