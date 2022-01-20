"""
Agent type which chooses a random available move on its turn.

Adapted from Andy Salerno (2016)
"""

import random

from agents.agent import Agent


class RandomAgent(Agent):
    """An agent that randomly chooses its move from the available legal moves."""

    def __init__(self, reversi, color, **kwargs):
        self.reversi = reversi
        self.color = color
        pass

    def get_action(self, state, legal_moves):
        if not legal_moves:
            return None
        return random.choice(legal_moves)

    def reset(self):
        pass

    def observe_win(self, winner):
        pass
