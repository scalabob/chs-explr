from fen_utils import position_fen
from pgn_utils import get_game_stats
from hash_utils import hash_board
from fen_hash_map import FenHashMap

class ChessTree:
    def __init__(self, startBoard=None):
        self.gameCount = 0
        self.nodes = {}
        self.map = FenHashMap()
        self.gameRefs = {} # TODO

        if startBoard is not None:
            self._initStartPos(startBoard)

    def _initStartPos(self, board):
        self.startFen = position_fen(board.fen())
        startHash = hash_board(board)
        self.map.add(self.startFen, startHash)

    def find_node(self, fromHash):
        return self.nodes.get(fromHash, {})

    def save_move(self, fromHash, move, toHash, gameStats):
        node = self.find_node(fromHash)

        if move in node:
            node[move]['visits'] += 1

            accum = node[move]['accum']
            node[move]['accum'] = {
                'whiteElo': accum['whiteElo'] + gameStats['whiteElo'],
                'blackElo': accum['blackElo'] + gameStats['blackElo'],
                'whitePerf': accum['whitePerf'] + gameStats['whitePerf'],
                'blackPerf': accum['blackPerf'] + gameStats['blackPerf'],
                'win': accum['win'] + gameStats['win'],
                'loss': accum['loss'] + gameStats['loss']
            }

        else:
            node[move] = {
                'toHash': toHash,
                'visits': 1,
                'accum': gameStats
            }

        self.nodes[fromHash] = node

    def get_fen_hash(self, fen, board=None):
        if self.map.has_fen(fen):
            return self.map.get_hash(fen)
        elif board is not None:
            hash = hash_board(board)
            self.map.add(fen, hash)
            return hash
        return None

    def add_game(self, pgnGame, limitDepth=20):
        # print(f"[TREE] Adding game {self.gameCount + 1}")
        isStartPos = False
        board = pgnGame.board()
        prevFen = None
        prevHash = None
        depth = 0
        # gameRef = get_game_ref(pgnGame)
        gameStats = get_game_stats(pgnGame)

        for move in pgnGame.mainline_moves():
            board.push(move)
            boardFen = position_fen(board.fen())

            # Move through game until we reach the startFen position
            if isStartPos is False:
                # print(f"[SKIP] {move} {boardFen}")
                if boardFen == self.startFen:
                    isStartPos = True
                    prevFen = boardFen
                    prevHash = self.get_fen_hash(boardFen, board)                        
                    # print("[TREE] Found start pos")
                    self.gameCount += 1
                continue

            # Add this game's position to the tree
            # print(f"[MOVE] {move} {boardFen}")

            currHash = self.get_fen_hash(boardFen, board)
            node = self.save_move(prevHash, str(move), currHash, gameStats)
            # node = self.save_move(prevFen, str(move), boardFen, gameStats)

            depth += 1
            prevFen = boardFen
            prevHash = currHash

            if depth >= limitDepth:
                break

    def get_node_by_hash(self, hash):
        return self.find_node(str(hash))

    def get_node_by_fen(self, fen):
        nodeFen = position_fen(fen)
        fenHash = self.get_fen_hash(nodeFen)
        # print(f"[TREE] fenHash:", fenHash)
        return self.get_node_by_hash(str(fenHash))

    def to_dict(self):
        return {
            'startFen': self.startFen,
            'nodes': self.nodes,
            'fenHash': self.map.to_list()
        }

    def from_dict(self, dict):
        self.startFen = dict['startFen']
        self.nodes = dict['nodes']
        [
            self.map.add(row[0], row[1])
            for row in dict['fenHash']
        ]
