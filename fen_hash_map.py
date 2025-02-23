class FenHashMap():
    def __init__(self):
        self.fenIdx = {}
        self.hashIdx = {}

    def has_fen(self, fen):
        return fen in self.fenIdx

    def has_hash(self, hash):
        return hash in self.hashIdx

    def add(self, fen, hash):
        self.fenIdx[fen] = hash
        self.hashIdx[hash] = fen

    def get_hash(self, fen):
        return self.fenIdx.get(fen, None)

    def get_fen(self, hash):
        return self.hashIdx.get(hash, None)

    def to_list(self):
        return [[fen, hash] for fen, hash in self.fenIdx.items()]
