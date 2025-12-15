from flask import Flask, render_template, jsonify, request
from dots_and_boxes import Board, EdgeOrientation, Move

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

games = {}

def get_game_state(game_id):
    if game_id not in games:
        games[game_id] = {
            'board': Board(rows=3, cols=3),
            'current_player': 1,
            'scores': {1: 0, 2: 0},
            'box_owners': {}
        }
    return games[game_id]

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/game/<game_id>', methods=['GET'])
def get_game(game_id):
    state = get_game_state(game_id)
    board = state['board']
    return jsonify({
        'rows': board.rows,
        'cols': board.cols,
        'horizontal_edges': board.horizontal_edges,
        'vertical_edges': board.vertical_edges,
        'current_player': state['current_player'],
        'scores': state['scores'],
        'box_owners': state['box_owners'],
        'game_over': len(board.legal_moves()) == 0
    })

@app.route('/api/game/<game_id>/move', methods=['POST'])
def make_move(game_id):
    state = get_game_state(game_id)
    board = state['board']
    
    data = request.json
    orientation = EdgeOrientation.HORIZONTAL if data['orientation'] == 'H' else EdgeOrientation.VERTICAL
    move = Move(orientation, data['r'], data['c'])
    
    if not board.is_legal(move):
        return jsonify({'error': 'Illegal move'}), 400
    
    completed_boxes = board.apply_move(move)
    
    for box in completed_boxes:
        state['scores'][state['current_player']] += 1
        box_key = f"{box[0]},{box[1]}"
        state['box_owners'][box_key] = state['current_player']
    
    if not completed_boxes:
        state['current_player'] = 2 if state['current_player'] == 1 else 1
    
    return jsonify({
        'success': True,
        'completed_boxes': completed_boxes,
        'rows': board.rows,
        'cols': board.cols,
        'horizontal_edges': board.horizontal_edges,
        'vertical_edges': board.vertical_edges,
        'current_player': state['current_player'],
        'scores': state['scores'],
        'box_owners': state['box_owners'],
        'game_over': len(board.legal_moves()) == 0
    })

@app.route('/api/game/<game_id>/reset', methods=['POST'])
def reset_game(game_id):
    games[game_id] = {
        'board': Board(rows=3, cols=3),
        'current_player': 1,
        'scores': {1: 0, 2: 0},
        'box_owners': {}
    }
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
