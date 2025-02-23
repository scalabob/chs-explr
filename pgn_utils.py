def get_pgn_game_headers(pgnGame):
    return {
        'Id': f"chesscom:{pgnGame.headers['ChesscomId']}",
        'Site': pgnGame.headers["Site"],
        'Event': pgnGame.headers["Event"],
        'Date': pgnGame.headers["Date"],
        'Round': pgnGame.headers["Round"],
        'Result': pgnGame.headers["Result"],
        'White': pgnGame.headers["White"],
        'WhiteElo': pgnGame.headers["WhiteElo"],
        'Black': pgnGame.headers["Black"],
        'BlackElo': pgnGame.headers["BlackElo"],
        'ECO': pgnGame.headers["ECO"]
    }

def get_pgn_game_moves(pgnGame):
    return pgnGame.mainline_moves()

def get_simple_game(pgnGame):
    headers = get_pgn_game_headers(pgnGame)
    moves = get_pgn_game_moves(pgnGame)
    return {
        'headers': headers,
        'moves': moves
    }

def calc_white_perf(playerElo, result, opponentElo):
    return (
        opponentElo
        if result == '1/2-1/2'
        else (
            opponentElo + 400
            if result == '1-0'
            else
            opponentElo - 400
        )
    )

def calc_black_perf(playerElo, result, opponentElo):
    return (
        opponentElo
        if result == '1/2-1/2'
        else (
            opponentElo - 400
            if result == '1-0'
            else
            opponentElo + 400
        )
    )

def get_game_stats(pgnGame):
    result = pgnGame.headers['Result']
    whiteElo = int(pgnGame.headers['WhiteElo'])
    blackElo = int(pgnGame.headers['BlackElo'])
    whitePerf = calc_white_perf(whiteElo, result, blackElo)
    blackPerf = calc_black_perf(blackElo, result, whiteElo)
    win = (1 if result == "1-0" else 0)
    loss = (1 if result == "0-1" else 0)

    return {
        'whiteElo': whiteElo,
        'blackElo': blackElo,
        'whitePerf': whitePerf,
        'blackPerf': blackPerf,
        'win': win,
        'loss': loss,
    }
