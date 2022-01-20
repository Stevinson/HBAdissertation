"""Node in the game tree used for Monte Carlo methods"""


class Node:

    def __init__(self, game_state, move=None):
        self.game_state = game_state
        self.plays = 0
        self.wins = 0
        self.children = []
        self.parent = None
        self.moves_expanded = set()

        # the move that led to this child state
        self.move = move

    def __hash__(self):
        return hash(self.game_state)

    def __repr__(self):
        return f"move: {self.move} wins: {self.wins} plays: {self.plays}"

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.game_state == other.game_state

    def add_child(self, node):
        self.children.append(node)
        self.moves_expanded.add(node.move)
        node.parent = self

    def has_children(self):
        return len(self.children) > 0

    def get_wins_plays(self):
        return self.wins, self.plays
