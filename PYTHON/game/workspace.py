"""
Contains the information to implement HBA such as move history and posterior beliefs.
Edward Stevinson
"""
from agents.max_disk_agent import MaxDiskAgent
from agents.max_value_agent import MaxValueAgent
from agents.mobility_agent import MobilityAgent
import numpy as np

class Workspace:
    # Everything currently set for HBA with two types
    
        def __init__(self):
            # Create each of the possible types
            self.type1 = MaxDiskAgent()
            self.type2 = MaxValueAgent()
            self.type3 = MobilityAgent()
            # Create a 2D prob_history
            self.prob_history = [] 
            self.prob_history.append([])
            self.prob_history.append([])
            self.prob_history.append([]) 
            # Create W.Str 
            self.create_opp_strategies()
            self.prior = [1/3, 1/3, 1/3] # Create Prior
            self.posterior = [1/3, 1/3, 1/3] #self.prior # Create Posterior beliefs 
            
        def update_iteration(self, state, lastAction):
            # Extend probability history
            self.extend_prob_history(lastAction)
            # Update posterior beliefs
            self.update_posteriors()
            # Get opp_strategies # This not done here as state already updated for the move in interest
            # self.opp_strategies = self.update_opp_strategies(state)
            
                
        def update_posteriors(self):
            """On each turn update posterior beliefs"""
            l = self.likelihood_gtw()
        # Calculate posterior
            # Multiply the prior and likelihood
            like = []
            like.append(l[0]*self.prior[0])
            like.append(l[1]*self.prior[1])
            like.append(l[2]*self.prior[2]) 
            # Create normalising constant
            summ = like[0] + like[1] + like[2]
            # Create posterior 
            a = like[0]/summ 
            b = like[1]/summ  
            c = like[2]/summ
            self.posterior[0] = a  
            self.posterior[1] = b 
            self.posterior[2] = c
            
        def likelihood_gtw(self):
            """Method that specifies how evidence accounted for (acts upon prob_history)
            Returns...   """
            # index of last entry
            t = len(self.prob_history[0]) - 1
            prob_array = np.asarray(self.prob_history)
            #
            a = []
            for i in range (t, -1, -1):
                a.append(i)
            if not a: # For the first iteration
                a.append(0)
            b = np.asarray(a)
            c = np.power(b, 5) # These variables affect the drop off rate
            d = c * 0.01
            w = np.subtract(10, d) 
            #
            e = np.greater(w,0)
            w = e * w
            # Turn prob_history into matrix
            
        # Matrix multiply H and transpose(w)
            f = np.transpose(w)
            l_mat = np.dot(prob_array, f)
            l = l_mat.tolist()
            
            ###
            #a = self.prob_history[0][t]
            #b = self.prob_history[1][t]
            #c = self.prob_history[2][t]
            #l = [a,b,c]
            return l
        
        def create_opp_strategies(self):
            """Initialise W.Str"""
            # Create 2D list
            self.opp_strategies = []
            self.opp_strategies.append([]) 
            self.opp_strategies.append([])
            self.opp_strategies.append([])
            
        def update_opp_strategies(self, state, legal_moves):
            """Return what moves the opponent would make (Equivalent to W.Str)
            Note that often there will be multiple moves per turn"""
            # Fill the list with the possible moves
            self.opp_strategies[0] = self.type1.get_all_actions(state, legal_moves)
            self.opp_strategies[1] =  self.type2.get_all_actions(state, legal_moves)
            self.opp_strategies[2] = self.type3.get_all_actions(state, legal_moves)
        
        def extend_prob_history(self, lastAction):
            """Update prob_history"""
            # lastAction is opposition's action from the last turn
            # Iterate for each type
            for i in (0,1,2):
                
                if not lastAction: # For the case when opposition had no moves in the past stage
                    self.prob_history[0].append(1)
                    self.prob_history[1].append(1)
                    self.prob_history[2].append(1)
                    break
                    
                if not self.opp_strategies[i]: # For the case when this type had no possible actions in the past stage
                    self.prob_history[i].append(0)
                    
                # If action matches that which the type would have made make it 1, else 0
                if lastAction in self.opp_strategies[i]: 
                    self.prob_history[i].append(1)
                else:
                    self.prob_history[i].append(0)

            
            