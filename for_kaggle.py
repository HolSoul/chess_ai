import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import chess
import chess.pgn
import os

# --- 1. Data Processing ---
def encode_board(board):
    board_state = np.zeros((12, 8, 8), dtype=np.float32)
    piece_map = {chess.PAWN: 0, chess.KNIGHT: 1, chess.BISHOP: 2, chess.ROOK: 3, chess.QUEEN: 4, chess.KING: 5}
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            channel = piece_map[piece.piece_type]
            if piece.color == chess.BLACK: channel += 6
            rank, file = chess.square_rank(square), chess.square_file(square)
            board_state[channel, rank, file] = 1.0
    return board_state

def encode_move(move):
    return move.from_square * 64 + move.to_square

def parse_pgn(pgn_file_path, max_games=None):
    with open(pgn_file_path) as pgn:
        games_processed = 0
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None: break
            board = game.board()
            for move in game.mainline_moves():
                yield encode_board(board), encode_move(move)
                board.push(move)
            games_processed += 1
            if max_games and games_processed >= max_games: break

class ChessDataset(Dataset):
    def __init__(self, pgn_file, max_games=1000):
        self.data = []
        print(f"Loading up to {max_games} games from {pgn_file}...")
        try:
            for state, move in parse_pgn(pgn_file, max_games=max_games):
                self.data.append((state, move))
        except FileNotFoundError:
            print("PGN file not found. Generating dummy data.")
            for _ in range(100):
                self.data.append((np.zeros((12,8,8), dtype=np.float32), 0))
        print(f"Loaded {len(self.data)} positions.")

    def __len__(self): return len(self.data)
    def __getitem__(self, idx):
        state, move = self.data[idx]
        return torch.from_numpy(state), torch.tensor(move, dtype=torch.long)

# --- 2. Model ---
class ChessNet(nn.Module):
    def __init__(self):
        super(ChessNet, self).__init__()
        self.conv1 = nn.Conv2d(12, 64, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(64)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(128)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(256)
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(16384, 1024)
        self.dropout = nn.Dropout(0.3)
        self.fc2 = nn.Linear(1024, 4096)

    def forward(self, x):
        x = torch.relu(self.bn1(self.conv1(x)))
        x = torch.relu(self.bn2(self.conv2(x)))
        x = torch.relu(self.bn3(self.conv3(x)))
        x = self.flatten(x)
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        return self.fc2(x)

# --- 3. Training Routine ---
def train_model(pgn_file, output_name, epochs, max_games, lr=0.001):
    print(f"--- Training {output_name} ---")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    
    dataset = ChessDataset(pgn_file, max_games=max_games)
    if len(dataset) == 0: return
    dataloader = DataLoader(dataset, batch_size=64, shuffle=True)
    
    model = ChessNet().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for data, target in dataloader:
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(dataloader):.4f}")
        
    torch.save(model.state_dict(), output_name)
    print(f"Saved {output_name}")

if __name__ == "__main__":
    # Configuration
    PGN_FILE = "games.pgn" # Upload your PGN to Kaggle and update this path
    
    # Train 3 levels of difficulty
    # Easy: Small dataset, few epochs (undertrained)
    train_model(PGN_FILE, "model_easy.pth", epochs=1, max_games=100)
    
    # Medium: Moderate dataset
    train_model(PGN_FILE, "model_medium.pth", epochs=5, max_games=1000)
    
    # Hard: Larger dataset
    train_model(PGN_FILE, "model_hard.pth", epochs=10, max_games=5000)
    
    # Extreme: Largest dataset
    train_model(PGN_FILE, "model_extreme.pth", epochs=20, max_games=20000)
