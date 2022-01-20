"""
HBA agent. Using the current beliefs of opponent type, this class uses MCTS to 
expand the game tree, before using UCT to give weight to the 'best' moves.
Edward Stevinson
Adapted from Andy Salerno (2016)
"""

import copy
import time
from typing import Tuple

import numpy as np

from agents.agent import Agent
from agents.mc_node import Node
from constants import BLACK, LOSS_PRIZE, OPPONENT, WIN_PRIZE
from game.workspace import Workspace
from util import *


class HBAAgent(Agent):
    def __init__(self, othello, color, **kwargs):
        self.color = color
        self.othello = othello
        self.sim_time = kwargs.get("sim_time", 5)

        self.workspace = Workspace()
        self.type_choice = 0

        # map states to nodes for quick lookup
        self.state_node = {}

    def reset(self):
        pass

    def observe_win(self, winner):
        pass

    def get_action(self, game_state, legal_moves, **kwargs):
        """
        Given a game state and a set of legal moves, pick a legal move and return it.
        This will be called by the Othello game object. Does not mutate the game state
        argument.
        """
        last_action = kwargs.pop("last_action")
        episode = kwargs.pop("time_step")

        if not legal_moves:
            return None

        game_state = copy.deepcopy(game_state)
        move = self.monte_carlo_search(game_state, last_action, episode)
        return move

    def monte_carlo_search(self, game_state: Tuple, last_action, time_step):
        """
        Given a game state, return the best action decided by using Monte Carlo Tree
        Search with an Upper Confidence Bound.
        """

        # map position to wins/plays for sorted info print
        results = {}

        # This isn't strictly necessary for Monte Carlo to work, but if we've seen this
        # state before we can get better results by reusing existing information.
        root = None
        if game_state in self.state_node:
            root = self.state_node[game_state]
        else:
            root = Node(game_state)

        # even if this is a "recycled" node we've already used,
        # remove its parent as it is now considered our root level node
        root.parent = None

        if time_step > 2:
            self.workspace.update_iteration(game_state[0], last_action)
            print(self.workspace.posterior)
            print(time_step)

        sim_count = 0
        now = time.time()
        while time.time() - now < self.sim_time:
            # if t>2: # It should be the first turn not the first run of MCTS
            #   # Update workspace
            #  self.workspace.update_iteration(game_state[0], lastAction)  ################################ MOVE

            self.type_choice = self.choose_player_type()
            picked_node = self.tree_policy(root)
            result = self.simulate(picked_node.game_state)
            self.back_prop(picked_node, result)
            sim_count += 1

        for child in root.children:
            wins, plays = child.get_wins_plays()
            position = child.move
            results[position] = (wins, plays)

        for position in sorted(results, key=lambda x: results[x][1]):
            info(
                "{}: ({}/{})".format(
                    position, results[position][0], results[position][1]
                )
            )
        info("{} simulations performed.".format(sim_count))
        return self.best_action(root)

    @staticmethod
    def best_action(node):
        """
        Returns the best action from this game state node.
        In Monte Carlo Tree Search we pick the one that was
        visited the most.  We can break ties by picking
        the state that won the most.
        """
        most_plays = -float("inf")
        best_wins = -float("inf")
        best_actions = []
        for child in node.children:
            wins, plays = child.get_wins_plays()
            if plays > most_plays:
                most_plays = plays
                best_actions = [child.move]
                best_wins = wins
            elif plays == most_plays:
                # break ties with wins
                if wins > best_wins:
                    best_wins = wins
                    best_actions = [child.move]
                elif wins == best_wins:
                    best_actions.append(child.move)

        return random.choice(best_actions)

    @staticmethod
    def back_prop(node, reward):
        """
        Given a node and a reward value, propagate that information up the tree
        to the root.
        """
        while node.parent is not None:
            node.plays += 1
            node.wins += reward
            node = node.parent

        # update root node of entire tree
        node.plays += 1
        node.wins += reward

    def tree_policy(self, root):
        """
        Given a root node, determine which child to visit using Upper Confidence Bound.
        """
        cur_node = root

        while True:
            legal_moves = self.othello.legal_moves(cur_node.game_state)
            if not legal_moves:
                if self.othello.winner(cur_node.game_state) is not False:
                    # The game is won
                    return cur_node
                else:
                    # No moves, so turn passes to other player
                    next_state = self.othello.next_state(cur_node.game_state, None)
                    pass_node = Node(next_state)
                    cur_node.add_child(pass_node)
                    self.state_node[next_state] = pass_node
                    cur_node = pass_node
                    continue
            elif len(cur_node.children) < len(legal_moves):
                # children are not fully expanded, so expand one
                unexpanded = [
                    move for move in legal_moves if move not in cur_node.moves_expanded
                ]

                assert len(unexpanded) > 0
                move = random.choice(unexpanded)
                state = self.othello.next_state(cur_node.game_state, move)
                n = Node(state, move)
                cur_node.add_child(n)
                self.state_node[state] = n
                return n
            else:
                # Every possible next state has been expanded, so pick one
                cur_node = self.best_child(cur_node)

        return cur_node

    def best_child(self, node):
        enemy_turn = node.game_state[1] != self.color
        C = 1  # 'exploration' value
        values = {}
        for child in node.children:
            wins, plays = child.get_wins_plays()
            if enemy_turn:
                # the enemy will play against us, not for us
                wins = plays - wins
            _, parent_plays = node.get_wins_plays()
            assert parent_plays > 0
            values[child] = (wins / plays) + C * math.sqrt(
                2 * math.log(parent_plays) / plays
            )

        best_choice = max(values, key=values.get)
        return best_choice

    def simulate(self, game_state):
        """
        Starting from the given game state, simulate a random game to completion, and
        return the profit value (1 for a win, 0 for a loss)
        """

        state = copy.deepcopy(game_state)

        step = 0
        while True:
            if winner := self.othello.winner(state):
                if winner == self.color:
                    return WIN_PRIZE
                elif winner == OPPONENT[self.color]:
                    return LOSS_PRIZE
                else:
                    raise ValueError

            moves = self.othello.legal_moves(state)
            if not moves:
                # If player has no moves, turn passes to opponent
                state = (state[0], OPPONENT[state[1]])
                moves = self.othello.legal_moves(state)

            # Act according to type for the rest of the simulation
            # Inherently presumes that HBA is white here. CHANGE!
            if state[1] == BLACK:
                # HBA continues to act randomly
                picked = random.choice(moves)
            else:
                # The opposition acts according to the type selected according to
                # posterior belief for 5 moves then randomly
                if step < 5:
                    agent_type_class = getattr(
                        self.workspace, f"type{str(self.type_choice+1)}"
                    )
                    picked = agent_type_class.get_action(state, moves)
                else:
                    picked = random.choice(moves)

            state = self.othello.apply_move(state, picked)
            step = step + 1

    def choose_player_type(self):
        """Choose player type according to the posterior values"""

        length = len(self.workspace.posterior)
        a = random.random()
        cumsum_posterior = np.cumsum(self.workspace.posterior)
        for i in range(0, length):
            if a < cumsum_posterior[i]:
                return i
