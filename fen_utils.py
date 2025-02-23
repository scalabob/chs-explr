def position_fen(fen):
    return " ".join(fen.split(" ")[:4])

def to_move_from_fen(fen):
    return fen.split(" ")[1]
