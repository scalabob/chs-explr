from tree_utils import format_wdl_stats, format_perf_stats
from fen_utils import position_fen, to_move_from_fen

class MainLineTreeTraversal:
    def __init__(self, tree, min_visits=100, depth=None):
        self.tree = tree
        self.min_visits = min_visits

    def _to_move_from_hash(self, hash):
        return self.tree.map.get_fen(hash)
        

    def _recurse(self, node_hash, min_visits, depth=0, max_depth=None):
        node = self.tree.get_node_by_hash(node_hash)
        node_items = sorted(node.items(), key=lambda tup: -tup[1]['visits'])
        # print("[NODE]", node_hash, node)
        # is_white_to_move = to_move_from_fen(node_fen) == "w"
        is_white_to_move = self._to_move_from_hash(node_hash) == "w"
        indent = "" + ("    " * (depth - 1))
        
        for move, move_data in node_items:
            visits = move_data['visits']
            if visits < min_visits:
                break

            accum = move_data['accum']
            moveStr = f"{indent}* {move}"
            wdlStr = format_wdl_stats(accum, visits)
            perfStr = format_perf_stats(accum, visits, is_white_to_move)
            print(f"{moveStr.ljust(32)} {str(visits).rjust(5)} {wdlStr.rjust(14)} {perfStr}")

            if max_depth is None or depth < max_depth:
                self._recurse(move_data['toHash'], min_visits, depth + 1, max_depth)

    def traverse(self, fen=None, min_visits=None, max_depth=None):
        # Depth-first traversal, show nodes with at least minVisit visits
        node_fen = position_fen(fen or self.tree.startFen)
        fenHash = self.tree.get_fen_hash(node_fen)
        print(f"From: {node_fen}")
        self._recurse(fenHash, min_visits or self.min_visits, 1, max_depth)
