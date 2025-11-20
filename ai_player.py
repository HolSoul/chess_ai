import torch
import chess
import numpy as np
from model import ChessNet
from data_loader import encode_board, decode_move, encode_move

class AIPlayer:
    def __init__(self, default_model_path="model_easy.pth"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.models = {}
        self.default_model_path = default_model_path
        
        # Pre-load default model as 'easy' for now if others don't exist
        self.load_model('easy', default_model_path)
        
        # Try to load others if they exist, otherwise map to default
        # In a real scenario, you'd have model_medium.pth etc.
        self.load_model('medium', "model_medium.pth")
        self.load_model('hard', "model_hard.pth")
        self.load_model('extreme', "model_extreme.pth")

    def load_model(self, difficulty, path):
        model = ChessNet().to(self.device)
        try:
            model.load_state_dict(torch.load(path, map_location=self.device))
            print(f"Loaded {difficulty} model from {path}")
            model.eval()
            self.models[difficulty] = model
        except FileNotFoundError:
            print(f"Warning: {path} not found. Using default/fallback for {difficulty}.")
            # Fallback to whatever we have or keep empty to handle gracefully later
            if 'easy' in self.models:
                 self.models[difficulty] = self.models['easy']
            else:
                 # If even easy/default is missing, we might be in trouble, but we'll handle it.
                 pass

    def get_best_move(self, board, difficulty='easy'):
        print(f"AI received request for difficulty: {difficulty}")
        model = self.models.get(difficulty)
        if not model:
            print(f"Model for {difficulty} not found, falling back to easy/default.")
            # Fallback if specific difficulty not loaded
            model = self.models.get('easy')
            if not model:
                # If absolutely no model, return random legal move
                print("No models loaded! Playing random move.")
                return list(board.legal_moves)[0].uci()

        # Encode board
        state = encode_board(board)
        state_tensor = torch.from_numpy(state).unsqueeze(0).to(self.device)

        with torch.no_grad():
            output = model(state_tensor)
            probs = torch.softmax(output, dim=1)
        
        probs = probs.squeeze(0).cpu().numpy()
        sorted_indices = np.argsort(probs)[::-1]

        legal_moves = set(board.legal_moves)
        
        for move_idx in sorted_indices:
            move = decode_move(move_idx)
            candidate_move = None
            for legal_move in legal_moves:
                if legal_move.from_square == move.from_square and legal_move.to_square == move.to_square:
                    candidate_move = legal_move
                    break
            
            if candidate_move:
                return candidate_move.uci()
        
        return list(legal_moves)[0].uci()

if __name__ == "__main__":
    ai = AIPlayer()
    board = chess.Board()
    move = ai.get_best_move(board)
    print(f"AI suggests: {move}")
