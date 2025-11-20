from flask import Flask, render_template, request, jsonify
import chess
from ai_player import AIPlayer

app = Flask(__name__)

# Initialize AI Player
# Ensure chess_model.pth exists (train.py should be run first)
ai = AIPlayer("chess_model.pth")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def get_move():
    data = request.json
    fen = data.get('fen')
    
    if not fen:
        return jsonify({'error': 'No FEN provided'}), 400
    
    board = chess.Board(fen)
    
    if board.is_game_over():
        return jsonify({'game_over': True, 'result': board.result()})
    
    try:
        # Get best move from AI
        difficulty = data.get('difficulty', 'easy')
        move_uci = ai.get_best_move(board, difficulty=difficulty)
        return jsonify({'move': move_uci})
    except Exception as e:
        print(f"Error generating move: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
