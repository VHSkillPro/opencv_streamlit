import torch
from torch import nn

NUM_CLASSES = 10


class MNISTModel(nn.Module):
    def __init__(self):
        super(MNISTModel, self).__init__()
        self.conv = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3)
        self.sigmoid = nn.Sigmoid()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc = nn.Linear(32 * 13 * 13, NUM_CLASSES)

    def forward(self, x):
        x = self.conv(x)
        x = self.sigmoid(x)
        x = self.pool(x)
        x = torch.flatten(x, start_dim=1)
        x = self.fc(x)
        return x
