import torch
import torch.nn as nn
import torch.nn.functional as F
from tqdm import tqdm



class CNN(nn.Module):
   def __init__(self):
      super().__init__()
      # Image dims H=75 W=100
      self.INPUT_IMG_DIMS = (75, 100)

      self.conv00 = nn.Conv2d(1, 16,  3)
      # self.pool0 = nn.MaxPool2d(2, 2)

      self.conv10 = nn.Conv2d(16, 32, 3)
      # self.pool1 = nn.MaxPool2d(2, 2)

      self.conv20 = nn.Conv2d(32, 64, 3)
      # self.pool2 = nn.MaxPool2d(2, 2)

      # self.fc1 = nn.Linear(64 * self.INPUT_IMG_DIMS[0] * self.INPUT_IMG_DIMS[0], 500)
      self.fc1 = nn.Linear(4480, 1)


   def forward(self, x):
      x = F.avg_pool2d(F.relu(self.conv00(x)), (2, 2))
      # x = F.relu(self.conv01(x))
      # x = F.relu(self.conv02(x))
      # x = self.pool0(x)

      x = F.avg_pool2d(F.relu(self.conv10(x)), (2, 2))
      # x = F.relu(self.conv11(x))
      # x = F.relu(self.conv12(x))
      # x = self.pool1(x)


      x = F.avg_pool2d(F.relu(self.conv20(x)), (2, 2))
      # x = F.relu(self.conv21(x))
      # x = F.relu(self.conv22(x))
      # x = self.pool2(x)

      x = torch.flatten(x, 1) # flatten all dimensions except batch
      # x = torch.relu(self.fc1(x))
      # x = torch.relu(self.fc2(x))
      # x = self.fc3(x)
      x = self.fc1(x)
      # print(x)
      # print()
      return x


# def train(net, epochs, batchSize, trainImgs, trainLabels):
#    print("Training for " + str(epochs) + " Epochs, Batch size: " + str(batchSize))
#    for epoch in range(epochs):
#        for i in tqdm(range(0, len(trainImgs), batchSize)): # from 0, to the len of x, stepping batchSize at a time. [:50] ..for now just to dev
#            #print(f"{i}:{i+BATCH_SIZE}")
#
#            batch_imgs   = trainImgs[i:i+batchSize].view(-1, 1, trainImgs.shape[1], trainImgs.shape[2])
#            batch_labels = trainLabels[i:i+batchSize]
#
#            batch_imgs, batch_labels = batch_imgs.to(device), batch_labels.to(device)
#
#            net.zero_grad()
#
#            outputs = net(batch_imgs)
#            loss = lossFunction(outputs, batch_labels)
#            loss.backward()
#            optimizer.step()    # Does the update
#
#        print(f"Epoch: {epoch}. Loss: {loss}")
#        # torch.save(net,'models/modelEpoch_' + str(epoch) + '.pt')
#        torch.save(net.state_dict(), 'models/modelEpoch_' + str(epoch))



if __name__ == "__main__":
   TRAIN = False

   cnn = CNN()





