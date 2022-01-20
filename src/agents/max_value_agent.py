"""
HBA agent type that assigns a value to each square on the board, and selects the move
associated with the square with the highest value.
Edward Stevinson
"""

import random
import copy
from agents.agent import Agent
from util import *
from pip._vendor.distlib._backport.shutil import move
from game.othello import Othello

class MaxValueAgent(Agent):
    """An agent that always plays the move associated with the highest value"""
    

    def __init__(self): #, reversi, color, **kwargs
        self.reversi = Othello()
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
        """" Choose the move associated with highest value"""
        # Shuffle so picks a random move if several return the same value
        random.shuffle(legal_moves) 
        # Get value of each move and save highest
        bestValue = -5
        for move in legal_moves:
            if self.isOnCorner(move):
                # corner always best move so can return here
                return move
            elif self.isEdgeSquare(move):
                bestMove = move
                bestValue = 1
            elif self.isCSquare(move):
                if bestValue<-2:
                    bestValue = -1
                    bestMove = move
            elif self.isXSquare(move):
                if bestValue<-1:
                    bestMove = move
                    bestValue = -2
            else:
                if bestValue<0:
                    bestMove = move
                    bestValue = 0
        # If no corner possible the method will return here
        return bestMove
    
    def get_all_actions(self, state, legal_moves):
        """Interface from class Agent.  Given a game state
        and a set of legal moves, pick a legal move and return it.
        This will be called by the Reversi game object. Does not mutate
        the game state argument."""
        if not legal_moves:
            return None
        state = copy.deepcopy(state)
        allMoves = self.maxValueAll(state, legal_moves)
        return allMoves
    
    def maxValueAll(self, state, legal_moves): 
        """All actions that this agent would make considering the state"""
        moves = [] # Variable that holds all the moves that this type of agent might make
        """First get what type of square is possible"""
        # Get value of each move and save highest
        bestValue = -5
        for move in legal_moves:
            if self.isOnCorner(move):
                # corner always best move so can break here
                bestValue = 2
                break
            elif self.isEdgeSquare(move):
                bestValue = 1
            elif self.isCSquare(move):
                if bestValue<-2:
                    bestValue = -1
            elif self.isXSquare(move):
                if bestValue<-1:
                    bestValue = -2
            else: # The rest of the squares are neutral squares
                if bestValue<0:
                    bestValue = 0
        """Now get ALL the squares of this type available"""
        for move in legal_moves:
            if bestValue == 2:
                if self.isOnCorner(move):
                    moves.append(move)
            elif bestValue == 1:
                if self.isEdgeSquare(move):
                    moves.append(move)
            elif bestValue == -1:
                if self.isCSquare(move):
                    moves.append(move)
            elif bestValue == -2:
                if self.isXSquare(move):
                    moves.append(move)
            else:
                moves.append(move)    
        """Then have to turn this into 8x8 matrix"""
        return moves
            
    def isOnCorner(self, move):
        return move==(0,0) or move==(0,7) or move==(7,7) or move==(7,0)        

    def isXSquare(self, move):
        return move==(1,1) or move==(1,6) or move==(6,1) or move==(6,6)
        
    def isCSquare(self, move):
        return move==(0,1) or move==(1,0) or move==(0,6) or move==(1,7) or move==(6,1) or move==(7,1) or move==(6,7) or move==(7,6)
    
    def isEdgeSquare(self, move):
        return move==(0,2) or move==(0,3) or move==(0,4) or move==(0,5) or move==(7,2) or move==(7,3) or move==(7,4) or move==(7,5) or move==(2,0) or move==(3,0) or move==(4,0) or move==(5,0) or move==(2,7) or move==(3,7) or move==(4,7) or move==(5,7)
