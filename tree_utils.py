def format_wdl_stats(accum, visits):
    win = accum['win']
    loss = accum['loss']
    draw = visits - win - loss
    winP = (100 * win) // visits
    lossP = (100 * loss) // visits
    drawP = (100 * draw) // visits
    return f"({winP}%:{drawP}%:{lossP}%)"

def format_perf_stats(accum, visits, is_white_to_move):
    whiteElo = accum['whiteElo'] // visits
    blackElo = accum['blackElo'] // visits
    whitePerf = accum['whitePerf'] // visits
    blackPerf = accum['blackPerf'] // visits


    if is_white_to_move:
        diff = whitePerf - whiteElo
        posDiff = "+" if whitePerf > whiteElo else ""
        return f"{whiteElo} {whitePerf}({posDiff}{whitePerf - whiteElo})"
        
    diff = blackPerf - blackElo
    posDiff = "+" if blackPerf > blackElo else ""
    return f"{blackElo} {blackPerf}({posDiff}{blackPerf - blackElo})"
