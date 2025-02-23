from chess.polyglot import zobrist_hash

def hash_board(board):
    return hex(zobrist_hash(board))
