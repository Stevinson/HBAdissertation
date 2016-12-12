"""
HBA agent type that chooses the move that limits the opponent's mobility (available moves) the most.
Edward Stevinson
"""

import random
import copy
from agents.agent import Agent
from util import *
from game.reversi import Reversi 
 

class MobilityAgent(Agent):
    """An agent that always plays as to make the number of possible moves for the opponent 
        in the next turn as few as possible"""
    

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
        move = self.min_mobility(state, legal_moves)
        return move 

    def reset(self):
        pass

    def observe_win(self, winner):
        pass
    
    def min_mobility(self, state, legal_moves):
        """" Choose a specific move that the agent will make on this turn"""
        # Randomise so that it picks a random move if several return the same value
        random.shuffle(legal_moves)
        # Initialise 
        minValue = 100
        # Examine how many liberties each legal move makes for the opponent
        for move in legal_moves:
            next_state = self.reversi.next_state(state, move)
            next_legal_moves = self.reversi.legal_moves(next_state)         
            # Does the opponent have any moves in the next board state?
            if not next_legal_moves: # This the optimum
                prefMove = move
                break
            # Does the game end in the next turn?
            elif self.reversi.winner(next_state):
                prefMove = move                        
                break
            else:
                numberMoves = len(next_legal_moves)
                if numberMoves < minValue:
                    prefMove = move
                    minValue = numberMoves
        return prefMove
    
    def get_all_actions(self, state, legal_moves):
        """Return all the possible actions that this agent will make on a turn"""
        if not legal_moves:
            return None
        state = copy.deepcopy(state)
        allMoves = self.minMobilityAll(state, legal_moves)
        return allMoves
    
    def minMobilityAll(self, state, legal_moves):
        """Get those actions from get_all_actions"""
        """" Choose a specific move that the agent will make on this turn"""
        # Initialise 
        minValue = 100
        # Examine how many liberties each legal move makes for the opponent
        for move in legal_moves:
            next_state = self.reversi.next_state(state, move)
            next_legal_moves = self.reversi.legal_moves(next_state)         
            # Does the opponent have any moves in the next board state?
            if not next_legal_moves:
                prefMove = move # This the best move with this strategy
                break
            # Does the game end in the next turn?
            elif self.reversi.winner(next_state):  
                prefMove = move # If the next state has a winner then there is only one move                    
                break 
                # do I need to add here? 
            else:
                numberMoves = len(next_legal_moves)
                if numberMoves < minValue:
                    prefMove = [move]
                    minValue = numberMoves
                elif numberMoves == minValue:
                    prefMove.append(move)
            
        return prefMove