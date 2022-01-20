"""Abstract class for a agent to play Othello"""

import abc


class Agent(abc.ABC):
    """An abstract class defining the interface for a Reversi agent."""

    def __init__(self, reversi, color):
        raise NotImplementedError

    @abc.abstractmethod
    def get_action(self, game_state, legal_moves, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def observe_win(self, state, winner):
        raise NotImplementedError

    @abc.abstractmethod
    def reset(self):
        raise NotImplementedError
