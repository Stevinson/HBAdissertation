"""""
Controller class for the Othello board game.

Adapted from Andy Salerno (2016)
"""

from copy import deepcopy
from typing import Tuple

from agents.random_agent import RandomAgent
from constants import COLOUR_STR, OPPONENT
from game.board import BLACK, EMPTY, WHITE, Board
from util import *


class Othello:
    """This class codifies the rules of the game of Othello."""

    def __init__(self, **kwargs):
        self.size = kwargs.get("size", 8)
        self.state = (Board(self.size), BLACK)

        self.legal_cache = CacheDict()

        self.last_action = None

        white_agent = kwargs.get("WhiteAgent", RandomAgent)
        black_agent = kwargs.get("BlackAgent", RandomAgent)
        self.white_agent = white_agent(self, WHITE, **kwargs)
        self.black_agent = black_agent(self, BLACK, **kwargs)

        self.time_step = 0

        make_silent(kwargs.get("silent", False))

        self.reset()

    @property
    def board(self):
        """Current game state board."""
        return self.state[0]

    @property
    def state(self):
        """The state is a tuple of the game class and whose turn it is."""
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

    def reset(self):
        """Reset the game to initial positions."""

        self.board.init_starting_position()
        self.state = (self.board, BLACK)
        self.legal_cache = CacheDict()

        self.white_agent.reset()
        self.black_agent.reset()

        self.time_step = 0

    def play_game(self):
        """
        Execute a game of Othello until the an state. Steps through the game episodes
        until a winning state is reached.
        """

        current_state = self.state
        self.print_board(current_state, msg="Current board")

        while self.winner(current_state) is False:
            colour = COLOUR_STR[current_state[1]]
            picked_action = self.agent_pick_move(current_state, self.last_action)
            self.last_action = picked_action
            current_state = self.next_state(current_state, picked_action)
            self.print_board(current_state, msg="Next episode board")
            self.time_step = self.time_step + 1

            if not picked_action:
                info(f"{colour} had no moves and passed their turn.")
            else:
                info(f"{colour} plays at {str(picked_action)}")
            info_newline()

        self.white_agent.observe_win(current_state)
        self.black_agent.observe_win(current_state)

        self.print_board(current_state, msg="End game state")

        # Calculate who won
        black_count, white_count = current_state[0].get_stone_counts()
        winner = BLACK if black_count > white_count else WHITE
        info(f"{COLOUR_STR[winner]} wins.")
        self.reset()
        return winner, white_count, black_count

    def agent_pick_move(self, state: Tuple, last_action):
        current_colour = state[1]
        legal_moves = self.legal_moves(state)
        picked = None

        # NB! The following assumes HBA is white White
        if current_colour == WHITE:
            picked = self.white_agent.get_action(
                state, legal_moves, last_action=last_action, time_step=self.time_step
            )
        elif current_colour == BLACK:
            self.white_agent.workspace.update_opponent_strategies(state, legal_moves)
            picked = self.black_agent.get_action(state, legal_moves)
            self.last_action = picked
        else:
            raise ValueError

        if picked is None:
            return None
        elif picked not in legal_moves:
            info(str(picked) + " is not a legal move! Game over.")
            quit()

        return picked

    def legal_moves(self, game_state, force_cache=False):
        # Note: this is a very naive and inefficient way to find
        # all available moves by brute force.  I am sure there is a
        # more clever way to do this.  If you want better performance
        # from agents, this would probably be the first area to improve.
        if force_cache:
            return self.legal_cache.get(game_state)

        board = game_state[0]
        if board.is_full():
            return []

        cached = self.legal_cache.get(game_state)
        if cached is not None:
            return cached

        board_size = board.get_size()
        moves = []  # list of x,y positions valid for color

        for y in range(board_size):
            for x in range(board_size):
                if self.is_valid_move(game_state, x, y):
                    moves.append((x, y))

        self.legal_cache.update(game_state, moves)
        return moves

    @staticmethod
    def is_valid_move(game_state, x, y):
        board, color = game_state
        piece = board.board[y][x]
        if piece != EMPTY:
            return False

        enemy = OPPONENT[color]

        # now check in all directions, including diagonal
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dy == 0 and dx == 0:
                    continue

                # there needs to be >= 1 opponent piece
                # in this given direction, followed by 1 of player's piece
                distance = 1
                yp = (distance * dy) + y
                xp = (distance * dx) + x

                while is_in_bounds(xp, yp, board.size) and board.board[yp][xp] == enemy:
                    distance += 1
                    yp = (distance * dy) + y
                    xp = (distance * dx) + x

                if (
                    distance > 1
                    and is_in_bounds(xp, yp, board.size)
                    and board.board[yp][xp] == color
                ):
                    return True
        return False

    def next_state(self, game_state: Tuple, move: Tuple):
        """
        Given a game_state and a position for a new piece, return a new game_state
        reflecting the change. Does not modify the input game_state.
        """
        return self.apply_move(deepcopy(game_state), move)

    @staticmethod
    def apply_move(game_state, move):
        """
        Given a game_state (which includes info about whose turn it is) and an x,y
        position to place a piece, transform it into the game_state that follows this
        play.
        """

        # If move is None, then the player simply passed their turn
        if not move:
            game_state = (game_state[0], OPPONENT[game_state[1]])
            return game_state

        x, y = move
        color = game_state[1]
        board = game_state[0]
        board.place_stone_at(color, x, y)

        # Flip all the stones in every direction
        enemy_color = OPPONENT[game_state[1]]

        to_flip = []
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dy == 0 and dx == 0:
                    continue

                # There needs to be >=1 opponent piece in this given direction, followed
                # by 1 of player's piece
                distance = 1
                yp = (distance * dy) + y
                xp = (distance * dx) + x

                flip_candidates = []
                while (
                    is_in_bounds(xp, yp, board.size)
                    and board.board[yp][xp] == enemy_color
                ):
                    flip_candidates.append((xp, yp))
                    distance += 1
                    yp = (distance * dy) + y
                    xp = (distance * dx) + x

                if (
                    distance > 1
                    and is_in_bounds(xp, yp, board.size)
                    and board.board[yp][xp] == color
                ):
                    to_flip.extend(flip_candidates)

        for each in to_flip:
            board.flip_stone(each[0], each[1])

        game_state = (game_state[0], OPPONENT[game_state[1]])
        return game_state

    def winner(self, game_state):
        """
        Given a game_state, return the color of the winner if there is one,
        otherwise return False to indicate the game isn't won yet.
        Note that legal_moves() is a slow operation, so this method
        tries to call it as few times as possible.
        """

        board = game_state[0]
        black_count, white_count = board.get_stone_counts()

        # a full board means no more moves can be made, game over.
        if board.is_full():
            if black_count > white_count:
                return BLACK
            else:
                # tie goes to white
                return WHITE

        # a non-full board can still be game-over if neither player can move.
        black_legal = self.legal_moves((game_state[0], BLACK))
        if black_legal:
            return False

        white_legal = self.legal_moves((game_state[0], WHITE))
        if white_legal:
            return False

        # neither black nor white has valid moves
        if black_count > white_count:
            return BLACK
        else:
            # tie goes to white
            return WHITE

    @staticmethod
    def print_board(state: Tuple, msg=None):
        board = state[0]
        print(msg)
        info(board)
        info_newline()
