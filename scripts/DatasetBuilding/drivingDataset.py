from torch.utils.data import Dataset
from datasetParser import DatasetParser

class DrivingDataset(Dataset):
   def __init__(self, filename, minAcceleration=0.20):
      self.inputs = None
      self.desiredOutputs = None
      self.__parseDataset(filename, minAcceleration)

   def __len__(self):
      return len(self.inputs)

   def __getitem__(self, idx):
      return self.inputs[idx], self.desiredOutputs[idx]

   def __parseDataset(self, filename, minAcceleration):
      print(">>> Parsing datafile " + filename)
      print(">>> Loading dataset...")
      parser = DatasetParser(filename)
      inputs, desiredOutputs = parser.loadDataset(minAcceleration)
      self.inputs = inputs
      self.desiredOutputs = desiredOutputs
      print(">>> Dataset loaded successfully with " + str(len(self)) + " entries")


if __name__ == '__main__':
    dataset = DrivingDataset("05-14-2021__15-05-20_carTest.txt", minAcceleration=0.20)
    print(">>> Example sample (first):")
    print(dataset[0])