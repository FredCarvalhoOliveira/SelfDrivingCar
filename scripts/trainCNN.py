import torch
import torch.nn as nn
import torch.optim as optim
from DatasetBuilding.drivingDataset import DrivingDataset
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from modelCNN import CNN, CNN_MEDIUM, CNN_LARGE



def train_old(model, dataset, numEpochs, batchSize, learningRate, device):
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
        writer.add_hparams({'LearningRate': learningRate, 'BatchSize': batchSize}, {'Loss': sum(losses)/len(losses)})
        print("Epoch #" + str(epoch + 1) + " Loss: " + str(loss))

def train(model, dataset, numEpochs, batchSize, learningRate, device):
    print(f">>> Training {model.name} CNN")

    model.train()

    # Data
    dataloader = DataLoader(dataset, batch_size=batchSize, shuffle=True)

    # Loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learningRate)

    writer = SummaryWriter(f'runs/CNN/{model.name}_bs{batchSize}_lr{learningRate}')

    step = 0
    # Train
    for epoch in range(numEpochs):
        for batchIdx, (data, targets) in enumerate(dataloader):
            data    = data.to(device=device)
            targets = targets.to(device=device)

            # Feedforward and loss
            preds = model(data)
            loss = criterion(preds, targets)

            # Backpropagation
            optimizer.zero_grad()
            loss.backward()

            # Optimizer step
            optimizer.step()

            writer.add_scalar('Training Loss', loss, global_step=step)
            step += 1
        print("Epoch #" + str(epoch + 1) + " Loss: " + str(loss))
    torch.save(model.state_dict(), f'../res/models/{model.name}_epochs_{epoch+1}')


# Device
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# dataset = DrivingDataset("../res/datasets/fullCropped.txt", isTrainSet=True, minAcceleration=0.20)
# NUM_EPOCS = 1
#
# batchSizes    = [32, 64, 128, 256, 512]
# learningRates = [0.1, 0.01, 0.001, 0.0001]
#
#
# for bs in batchSizes:
#     for lr in learningRates:
#         model = CNN().to(device=device)
#         model.train()
#         train(model=model, dataset=dataset, numEpochs=NUM_EPOCS, batchSize=bs, learningRate=lr, device=device)


########################
### TRAIN ALL MODELS ###
# Device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

dataset = DrivingDataset("../res/datasets/imgCropped.txt", isTrainSet=True, minAcceleration=0.20)
NUM_EPOCS     = 20
BATCH_SIZE    = 64
LEARNING_RATE = 0.001

cnnLite   = CNN().to(device=device)
cnnMedium = CNN_MEDIUM().to(device=device)
cnnLarge  = CNN_LARGE().to(device=device)
models    = [cnnLite, cnnMedium, cnnLarge]

for model in models:
    train(model=model, dataset=dataset, numEpochs=NUM_EPOCS, batchSize=BATCH_SIZE, learningRate=LEARNING_RATE, device=device)
    print()

