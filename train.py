import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from data_loader import parse_pgn
from model import ChessNet
import os

class ChessDataset(Dataset):
    def __init__(self, pgn_file, max_games=100):
        self.data = []
        print(f"Loading games from {pgn_file}...")
        # Load all data into memory (fine for small datasets/demos)
        for state, move in parse_pgn(pgn_file, max_games=max_games):
            self.data.append((state, move))
        print(f"Loaded {len(self.data)} positions.")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        state, move = self.data[idx]
        return torch.from_numpy(state), torch.tensor(move, dtype=torch.long)

def train(pgn_file, epochs=5, batch_size=32, lr=0.001):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    dataset = ChessDataset(pgn_file, max_games=200) # Limit games for demo speed
    if len(dataset) == 0:
        print("No data found! Check PGN file.")
        return
        
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = ChessNet().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for batch_idx, (data, target) in enumerate(dataloader):
            data, target = data.to(device), target.to(device)

            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
        
        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")

    torch.save(model.state_dict(), "chess_model.pth")
    print("Model saved to chess_model.pth")

if __name__ == "__main__":
    # Use dummy.pgn if it exists, otherwise warn
    if os.path.exists("dummy.pgn"):
        train("dummy.pgn", epochs=10)
    else:
        print("dummy.pgn not found. Please provide a PGN file.")
