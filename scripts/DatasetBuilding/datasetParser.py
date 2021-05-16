import numpy as np
import os
from torch.utils.data import DataLoader

class DatasetParser:
   def __init__(self, fileName):
      self.filepath = fileName#"../../res/datasets/" + fileName
      self.inShape    = None
      self.outShape   = None
      self.inVarType  = None
      self.outVarType = None

   def __parseMetadata(self, metadataStr):
      metadata = metadataStr.split('|')

      inShape = metadata[0].split(';')
      for i in range(len(inShape)):
         inShape[i] = int(inShape[i])
      self.inShape = tuple(inShape) if len(inShape) > 1 else inShape[0]

      outShape = metadata[1].split(';')
      for i in range(len(outShape)):
         outShape[i] = int(outShape[i])
      self.outShape = tuple(outShape) if len(outShape) > 1 else outShape[0]
      self.inVarType  = metadata[2]
      self.outVarType = metadata[3]

   def __parseDataLine(self, line):
      inputs, outputs = line.split("|")
      inputs  = inputs.split(";")
      outputs = outputs.split(";")

      inputs  = np.array(inputs).astype(self.inVarType).reshape(self.inShape)
      outputs = np.array(outputs).astype(self.outVarType).reshape(self.outShape)

      return inputs, outputs

   def __parseDataset(self):
      dataFile = open(self.filepath, 'r')
      lines    = dataFile.readlines()

      inputs  = [None for l in range(len(lines) - 1)] # -1 because first line is metadata
      outputs = [None for l in range(len(lines) - 1)] # -1 because first line is metadata

      for lineIdx in range(len(lines)):
         line = lines[lineIdx].rstrip()

         if lineIdx == 0:
            self.__parseMetadata(line)
         else:
            parsedIn, parsedOut = self.__parseDataLine(line)

            inputs[lineIdx-1]  = parsedIn
            outputs[lineIdx-1] = parsedOut

      return inputs, outputs

   def __cleanDataset(self, inputs, outputs, minAcceleration=0.20):
      inputs  = np.array(inputs)
      outputs = np.array(outputs)
      mask    = outputs[:, 0] > minAcceleration
      inputs  = inputs[mask]
      outputs = outputs[mask]
      return inputs, outputs

   def loadDataset(self, minAcceleration=0.20):
      inputs, desiredOutputs = self.__parseDataset()
      inputs, desiredOutputs = self.__cleanDataset(inputs, desiredOutputs, minAcceleration)
      # dataset = DrivingDataset(inputs, desiredOutputs)
      return inputs, desiredOutputs

if __name__ == '__main__':
   import imutils
   import cv2

   scale = 0.1
   parser = DatasetParser("../../res/datasets/05-14-2021__15-05-20_carTest.txt")
   inputs, desiredOutputs = parser.loadDataset()


   imgIdx = 0
   while True:
      frame = inputs[imgIdx]
      frame = imutils.resize(frame, int(frame.shape[1] / scale), int(frame.shape[0] / scale))
      print(">>> #" + str(imgIdx) + " Current input <<<")
      print(inputs[imgIdx])
      print(">>> #" + str(imgIdx) + " Current output <<<")
      print(desiredOutputs[imgIdx])
      print()

      cv2.imshow("img", frame)
      if cv2.waitKey(0) & 0xFF == ord('n'):
         if imgIdx < len(inputs) - 1:
            imgIdx += 1
      if cv2.waitKey(0) & 0xFF == ord('b'):
         if imgIdx > 0:
            imgIdx -= 1
      if cv2.waitKey(0) & 0xFF == ord('q'):
         break  # esc to quit
