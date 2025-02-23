import json
import os.path
from chess_tree import ChessTree
from fen_utils import position_fen
from tree_utils import format_wdl_stats

def save_tree(projectSlug, tree):
    treeFile = f"./{projectSlug}/tree.json"
    with open(treeFile, 'w') as fp:
        json.dump(tree.to_dict(), fp)

def load_tree(projectSlug):
    treeFile = f"./{projectSlug}/tree.json"

    if os.path.isfile(treeFile) is False:
        print("No existing tree")
        return None

    with open(treeFile, 'r') as fp:
        treeData = json.load(fp)

        tree = ChessTree()
        tree.from_dict(treeData)
        # tree = ChessTree(treeData['startFen'])
        # tree.nodes = treeData['nodes']
        return tree

def dump_node(fen, node):
    nodeFen = position_fen(fen)
    print(f"[FEN]  {nodeFen}")
    items = sorted(node.items(), key=lambda tup: -tup[1]['visits'])
    for key, values in items:
        visits = values['visits']
        accum = values['accum']
        whiteElo = accum['whiteElo'] // visits
        blackElo = accum['blackElo'] // visits
        whitePerf = accum['whitePerf'] // visits
        blackPerf = accum['blackPerf'] // visits

        wdlStr = format_wdl_stats(values['accum'], visits)
        print(f"[MOVE] {key} ({str(visits).rjust(5)}) {wdlStr} => {values['toHash']}")
    print()

def print_node(tree, fen):
    nodeFen = position_fen(fen)
    node = tree.get_node_by_fen(nodeFen)
    dump_node(nodeFen, node)
