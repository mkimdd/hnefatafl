import math

class Node:
    """Represents Node for Monte Carlo Tree Search."""
    def __init__(self, parent=None, m=None, g=None):
        """Initializes Node for Monte Carlo Tree Search."""
        self.g = g
        # n - number of visits to this Node
        self.n = 0
        # t - total score
        self.t = 0
        # m - represented move
        self.m = m
        self.parent = parent
        self.children = []
    def add_child(self, child):
        self.children.append(child)
    def get_n(self):
        return self.n
    def get_move(self):
        return self.m
    def get_game(self):
        return self.g
    def confidence(self):
        print(f"{self.t} + math.sqrt( math.log( {self.parent.get_n()}/{self.n} ) )")
        try:
            confidence = self.t + 2 * math.sqrt(math.log(self.parent.get_n())/self.n)
        except ValueError:
            return 100000
        return confidence
    def update(self, result):
        self.n += 1
        self.t += result