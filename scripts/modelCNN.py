import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from tqdm import tqdm
from DatasetBuilding.drivingDataset import DrivingDataset
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter


class CNN(nn.Module):
   def __init__(self):
      super().__init__()
      self.name = "Lite"
      # Image dims H=75 W=100
      self.INPUT_IMG_DIMS = (75, 100)
      self.conv00 = nn.Conv2d(1,  16,  3)
      self.conv10 = nn.Conv2d(16, 32,  3)
      self.conv20 = nn.Conv2d(32, 64,  3)
      self.fc1 = nn.Linear(1280, 2)

   def forward(self, x):
      x = F.relu(self.conv00(x))
      x = F.avg_pool2d(x, (2, 2))

      x = F.relu(self.conv10(x))
      x = F.avg_pool2d(x, (2, 2))

      x = F.relu(self.conv20(x))
      x = F.avg_pool2d(x, (2, 2))

      x = torch.flatten(x, 1) # flatten all dimensions except batch
      x = self.fc1(x)
      return x

class CNN_MEDIUM(nn.Module):
   def __init__(self):
      super().__init__()
      self.name = "Medium"

      self.INPUT_IMG_DIMS = (75, 100)
      self.conv00 = nn.Conv2d(1,  16,   3)
      self.conv01 = nn.Conv2d(16,  16,  3)

      self.conv10 = nn.Conv2d(16, 32,  3)
      self.conv11 = nn.Conv2d(32, 32,  3)

      self.conv20 = nn.Conv2d(32, 64,  3)
      self.fc1 = nn.Linear(640, 2)

   def forward(self, x):
      x = F.relu(self.conv00(x))
      x = F.relu(self.conv01(x))
      x = F.avg_pool2d(x, (2, 2))

      x = F.relu(self.conv10(x))
      x = F.relu(self.conv11(x))
      x = F.avg_pool2d(x, (2, 2))

      x = F.relu(self.conv20(x))
      x = F.avg_pool2d(x, (2, 2))

      x = torch.flatten(x, 1) # flatten all dimensions except batch
      x = self.fc1(x)
      return x

class CNN_LARGE(nn.Module):
   def __init__(self):
      super().__init__()
      self.name = "Large"

      self.INPUT_IMG_DIMS = (75, 100)
      self.conv00 = nn.Conv2d(1,  16,   3)
      self.conv01 = nn.Conv2d(16,  16,  3)

      self.conv10 = nn.Conv2d(16, 32,  3)
      self.conv11 = nn.Conv2d(32, 32,  3)
      self.conv12 = nn.Conv2d(32, 64,  3)

      self.conv20 = nn.Conv2d(64, 64,  3)
      self.conv20 = nn.Conv2d(64, 64,  3)
      self.fc1 = nn.Linear(576, 100)
      self.fc2 = nn.Linear(100, 2)

   def forward(self, x):
      x = F.relu(self.conv00(x))
      x = F.relu(self.conv01(x))
      x = F.avg_pool2d(x, (2, 2))

      x = F.relu(self.conv10(x))
      x = F.relu(self.conv11(x))
      x = F.relu(self.conv12(x))
      x = F.avg_pool2d(x, (2, 2))

      x = F.relu(self.conv20(x))
      x = F.avg_pool2d(x, (2, 2))

      x = torch.flatten(x, 1) # flatten all dimensions except batch
      x = F.relu(self.fc1(x))
      x = self.fc2(x)
      return x



if __name__ == "__main__":
   # Device
   device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

   # Train params
   numEpochs = 1#500
   batchSize = 100
   learningRate = 0.001

   # Data
   dataset    = DrivingDataset("../res/datasets/imgCropped.txt", isTrainSet=True, minAcceleration=0.20)
   dataloader = DataLoader(dataset, batch_size=batchSize, shuffle=True)

   # Init model
   model = CNN().to(device=device)
   model = CNN().to(device=device)

   # Loss function and optimizer
   criterion = nn.MSELoss()
   optimizer = optim.Adam(model.parameters(), lr=learningRate)


   # batchSizes    = [8, 16, 32, 64, 128, 256, 512]
   # learningRates = [0.1, 0.01, 0.001, 0.0001]




   # writer = SummaryWriter(f'runs/CNN/crop_lr{learningRate}_bs{batchSize}')

   step = 0
   # Train
   for epoch in range(numEpochs):
      for batchIdx, (data, targets) in enumerate(dataloader):
         data = data.to(device=device)
         targets = targets.to(device=device)

         # Feedforward and loss
         preds = model(data)
         loss = criterion(preds, targets)

         # Backpropagation
         optimizer.zero_grad()
         loss.backward()

         # Optimizer step
         optimizer.step()

         # writer.add_scalar('Training Loss', loss, global_step=step)
         step += 1

   #    print("Epoch #" + str(epoch + 1) + " Loss: " + str(loss))
   # torch.save(model.state_dict(), '../res/models/FINAL_CNN_epochs_' + str(epoch + 1))
