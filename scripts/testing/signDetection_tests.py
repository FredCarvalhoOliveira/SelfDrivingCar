import cv2
import time
from timeAnalisis import TimeAnalisis

cam = cv2.VideoCapture(0)
TA  = TimeAnalisis()
persistNumFrames = 5
persistCount     = 0
timestamp        = 0
waiting          = False

def waitStopTime(waitTime): # wait time in milliseconds
   global timestamp
   global waiting
   timestamp = time.time()

   waiting = False
   if (time.time() - timestamp)*1000 < waitTime:
      pass
   else:
      waiting = True


while True:
   TA.startTimer()
   ret_val, img = cam.read()
   clf  = cv2.CascadeClassifier("../../res/haarcascade_stopSigns")
   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   stop_signs = clf.detectMultiScale(gray, 1.02, 10)


   if len(stop_signs) > 0:
      persistCount += 1
      for (x, y, w, h) in stop_signs:
         cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
   else:
      persistCount = 0


   if persistCount >= persistNumFrames and not waiting:
      print("Stopped")
      waitStopTime(5000)
      pass
   else:
      print("Moving")
      pass

   cv2.imshow("img", img)

   TA.stopTimer()
   TA.registerTime(TA.getTimeElapsed())
   if cv2.waitKey(1) & 0xFF == ord('q'):
      break  # esc to quit
cv2.destroyAllWindows()
print(TA.getMeanTimeElapsed())


