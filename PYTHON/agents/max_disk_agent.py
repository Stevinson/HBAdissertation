"""
HBA agent type that selects the move that flips the most opposition disks.
Edward Stevinson
"""

import random
import copy
from agents.agent import Agent
from util import *
from game.reversi import Reversi 
 

class MaxDiskAgent(Agent):
    """An agent that always plays the move that gains the most disks"""
    

    def __init__(self): #, reversi, color, **kwargs
        self.reversi = Reversi()
        #self.color = color
        pass
        
    def get_action(self, state, legal_moves):
        """Interface from class Agent.  Given a game state
        and a set of legal moves, pick a legal move and return it.
        This will be called by the Reversi game object. Does not mutate
        the game state argument."""
        if not legal_moves:
            return None
        state = copy.deepcopy(state)
        move = self.max_disk(state, legal_moves)
        return move 

    def reset(self):
        pass

    def observe_win(self, winner):
        pass
    
    def max_disk(self, state, legal_moves):
        """" Choose the move that flips the most disks"""
        random.shuffle(legal_moves) # So picks a random move if several return the same score
        colour = state[1]
        # Go through the possible moves and remember the best move
        bestScore = -1
        for move in legal_moves:
            # copies the board, then makes the move
            state_copy = self.reversi.next_state(state, move)
            # get the score of the board
            #black_count, white_count = state[0].get_stone_counts
            black_count = state_copy[0].black_stones
            white_count = state_copy[0].white_stones
            # get the score of whoever's turn it is
            score = black_count if colour == 1 else white_count
            # if it is the current best score, save it
            if score > bestScore:
                bestMove = move
                bestScore = score
        # Return the best move
        return bestMove
    
    def get_all_actions(self, state, legal_moves):
        """Interface from class Agent.  Given a game state
        and a set of legal moves, pick a legal move and return it.
        This will be called by the Reversi game object. Does not mutate
        the game state argument."""
        if not legal_moves:
            return None
        state = copy.deepcopy(state)
        allMoves = self.maxDiskAll(state, legal_moves)
        return allMoves
    
    def maxDiskAll(self, state, legal_moves):
        """All actions that this agent would make considering the state"""
        colour = state[1]
        # Go through the possible moves and remember the best move
        bestScore = -1
        for move in legal_moves:
            # copies the board, then makes the move
            state_copy = self.reversi.next_state(state, move)
            # get the score of the board
            #black_count, white_count = state[0].get_stone_counts
            black_count = state_copy[0].black_stones
            white_count = state_copy[0].white_stones
            # get the score of whoever's turn it is
            score = black_count if colour == 1 else white_count
            # if it is the current best score, save it
            if score > bestScore:
                bestMoves = [move]
                bestScore = score
            elif score == bestScore:
                bestMoves.append(move) 
        """Then have to turn this into 8x8 matrix"""
        # Return the best move
        return bestMoves
        # Return all possible actions that this agent wop        pass        return bestMove   """      """   return bestMove