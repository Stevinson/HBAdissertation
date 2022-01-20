"""
HBA agent type that does not always act according to type, in an attempt to simulate 
full ad hoc properties. The agents selects its type randomly on x% of moves.
Edward Stevinson
"""

import random
import copy
from agents.agent import Agent
from agents.max_disk_agent import MaxDiskAgent
from agents.r_agent import RAgent
from util import *
import numpy as np
from game.othello import Othello
 

class MaxDiskPurturb(Agent):
    """A perturbed agent to simulate full ad hoc properties.
    The agents does not act according to type 10% of moves."""
    

    def __init__(self): #, reversi, color, **kwargs
        self.reversi = Othello()
        #self.color = color
        self.type1 = MaxDiskAgent()
        self.type2 = RAgent()
        self.probs = [0.9, 0.1]
        pass
        
    def get_action(self, state, legal_moves):
        """Interface from class Agent.  Given a game state
        and a set of legal moves, pick a legal move and return it.
        This will be called by the Reversi game object. Does not mutate
        the game state argument."""
        if not legal_moves:
            return None
        state = copy.deepcopy(state)
        
    ###
    
        # Make choice of which agent
        self.choiceMade  = self.randomAct()
        # Turn into string to access type 
        b = self.choiceMade + 1
        name = 'type' + str(b)
        
        typeSel = getattr(self, name)
        picked = typeSel.get_action(state, legal_moves)
        print(name)
        #picked = typeSel.get_action(state, legal_moves)
        return picked 

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
    
    def randomAct(self):
        """Choose according to the probability values"""
        length = len(self.probs)
        a = random.randint(0,9999)
        b = a/10000
        x = np.cumsum(self.probs)
        for i in range(0,length):
            if b < x[i]:
                c = i
                break
        return c