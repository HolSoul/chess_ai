import torch
import torch.nn as nn
import torch.nn.functional as F

class ChessNet(nn.Module):
    def __init__(self):
        super(ChessNet, self).__init__()
        # Input: 12 channels (6 white pieces, 6 black pieces), 8x8 board
        self.conv1 = nn.Conv2d(12, 64, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(64)
        
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(128)
        
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(256)
        
        self.flatten = nn.Flatten()
        
        # 8x8 * 256 = 16384
        self.fc1 = nn.Linear(16384, 1024)
        self.dropout = nn.Dropout(0.3)
        
        # Output: 4096 possible moves (64 from * 64 to)
        # This is a simplification. A full engine handles promotions (4096 * 4 approx).
        self.fc2 = nn.Linear(1024, 4096)

    def forward(self, x):
        # x shape: (batch, 12, 8, 8)
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        
        x = self.flatten(x)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        
        x = self.fc2(x)
        return x # Return raw logits (CrossEntropyLoss will handle softmax)

if __name__ == "__main__":
    # Test model shape
    model = ChessNet()
    dummy_input = torch.randn(1, 12, 8, 8)
    output = model(dummy_input)
    print(f"Model output shape: {output.shape}")
