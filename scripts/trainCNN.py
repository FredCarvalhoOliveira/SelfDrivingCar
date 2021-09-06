import torch
import torch.nn as nn
import torch.optim as optim
from DatasetBuilding.drivingDataset import DrivingDataset
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from modelCNN import CNN



def train(model, dataset, numEpochs, batchSize, learningRate, device):
    # Data
    dataloader = DataLoader(dataset, batch_size=batchSize, shuffle=True)

    # Loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learningRate)

    writer = SummaryWriter(f'runs/CNN/crop_bs{batchSize}_lr{learningRate}')

    step = 0
    # Train
    for epoch in range(numEpochs):
        losses = []

        for batchIdx, (data, targets) in enumerate(dataloader):
            data = data.to(device=device)
            targets = targets.to(device=device)

            # Feedforward and loss
            preds = model(data)
            loss = criterion(preds, targets)
            losses.append(loss.item())

            # Backpropagation
            optimizer.zero_grad()
            loss.backward()

            # Optimizer step
            optimizer.step()

            writer.add_scalar('Training Loss', loss, global_step=step)
            step += 1
        writer.add_hparams({'LearningRate': lr, 'BatchSize': bs}, {'Loss': sum(losses)/len(losses)})
        print("Epoch #" + str(epoch + 1) + " Loss: " + str(loss))




# Device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

dataset = DrivingDataset("../res/datasets/fullCropped.txt", isTrainSet=True, minAcceleration=0.20)
NUM_EPOCS = 1

batchSizes    = [32, 64, 128, 256, 512]
learningRates = [0.1, 0.01, 0.001, 0.0001]


for bs in batchSizes:
    for lr in learningRates:
        model = CNN().to(device=device)
        model.train()
        train(model=model, dataset=dataset, numEpochs=NUM_EPOCS, batchSize=bs, learningRate=lr, device=device)

