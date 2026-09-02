from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty', 'medium').lower()
    
    # Map difficulty levels to number of clues
    difficulty_map = {
        'easy': 45,      # Remove 36 cells (45 clues)
        'medium': 35,    # Remove 46 cells (35 clues)
        'hard': 25       # Remove 56 cells (25 clues)
    }
    
    clues = difficulty_map.get(difficulty, 35)
    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle})

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    # Catch the missing field early
    if not data or 'board' not in data or data['board'] is None:
        return jsonify({"error": "Missing board field"}), 400
        
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})

if __name__ == '__main__':
    app.run(debug=True)