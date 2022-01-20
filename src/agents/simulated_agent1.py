"""
A dynamic, mixed player distribution. The simulated agent is MaxDisk in early game stages,
MaxValue in mid-stages, and Mobility in end-moves.
Edward Stevinson
"""

import random
import copy
from agents.agent import Agent
from agents.max_value_agent import MaxValueAgent
from agents.max_disk_agent import MaxDiskAgent
from agents.mobility_agent import MobilityAgent
from util import *
from game.othello import Othello
 

class SimulatedAgent1(Agent):
    """Agent that has a mixed distribution (its type changes), which is also 
    dynamic (its type depends on what stage of the game it's in)."""
    

    def __init__(self, reversi, color, **kwargs): #, reversi, color, **kwargs
        self.reversi = Othello()
        self.color = color
        self.type1 = MaxDiskAgent()
        self.type2 = MaxValueAgent()
        self.type3 = MobilityAgent()
        pass
        
    def get_action(self, state, legal_moves, t): # , lastAction #
        """Interface from class Agent.  Given a game state
        and a set of legal moves, pick a legal move and return it.
        This will be called by the Reversi game object. Does not mutate
        the game state argument."""
        if not legal_moves:
            return None
        state = copy.deepcopy(state)
        if t<14:
            move = self.type1.get_action(state, legal_moves)
        elif t<28:
            move = self.type3.get_action(state, legal_moves)
        else:
            move = self.type2.get_action(state, legal_moves)
        return move 

    def reset(self):
        pass

    def observe_win(self, winner):
        pass
    
    def max_disk(self, state, legal_moves):
        pass
    
    def get_all_actions(self, state, legal_moves):
        pass
    
    def maxDiskAll(self, state, legal_moves):
        pass