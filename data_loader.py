import chess
import chess.pgn
import numpy as np
import torch

def encode_board(board):
    """
    Encodes a chess board into a 12x8x8 float32 tensor.
    Channels 0-5: White pieces (P, N, B, R, Q, K)
    Channels 6-11: Black pieces (P, N, B, R, Q, K)
    """
    # 12 channels: P, N, B, R, Q, K for White, then Black
    board_state = np.zeros((12, 8, 8), dtype=np.float32)
    
    piece_map = {
        chess.PAWN: 0,
        chess.KNIGHT: 1,
        chess.BISHOP: 2,
        chess.ROOK: 3,
        chess.QUEEN: 4,
        chess.KING: 5
    }
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            # Calculate channel index
            channel = piece_map[piece.piece_type]
            if piece.color == chess.BLACK:
                channel += 6
            
            # Map square (0-63) to (row, col)
            # python-chess square 0 is a1, 63 is h8.
            # We'll map rank (0-7) to row, file (0-7) to col.
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            
            board_state[channel, rank, file] = 1.0
            
    return board_state

def encode_move(move):
    """
    Encodes a move into an integer index (0-4095).
    Formula: from_square * 64 + to_square
    """
    return move.from_square * 64 + move.to_square

def decode_move(move_index):
    """
    Decodes a move index back to a chess.Move object.
    Note: This doesn't handle promotion logic perfectly (defaults to None or Queen if needed later).
    """
    from_square = move_index // 64
    to_square = move_index % 64
    
    # Basic move, promotion is not handled in this simple encoding
    # For a real engine, we'd need 4096 * promotion_types or similar.
    # For now, we'll assume auto-queen promotion if applicable in the game loop logic,
    # but the move object itself is just from-to.
    return chess.Move(from_square, to_square)

def parse_pgn(pgn_file_path, max_games=None):
    """
    Generator that reads a PGN file and yields (board_tensor, move_index) tuples.
    """
    with open(pgn_file_path) as pgn:
        games_processed = 0
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break
            
            board = game.board()
            for move in game.mainline_moves():
                # Encode current state
                state = encode_board(board)
                action = encode_move(move)
                
                yield state, action
                
                board.push(move)
            
            games_processed += 1
            if max_games and games_processed >= max_games:
                break

if __name__ == "__main__":
    # Simple test
    board = chess.Board()
    encoded = encode_board(board)
    print(f"Encoded board shape: {encoded.shape}")
    print(f"White pawns at start: {np.sum(encoded[0])}") # Should be 8
