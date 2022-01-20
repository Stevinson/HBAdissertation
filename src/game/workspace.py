"""HBA controller class, i.e. calculate move histories and posterior beliefs."""
import numpy as np

from agents.max_disk_agent import MaxDiskAgent
from agents.max_value_agent import MaxValueAgent
from agents.mobility_agent import MobilityAgent


class Workspace:
    def __init__(self):
        self.type1 = MaxDiskAgent()
        self.type2 = MaxValueAgent()
        self.type3 = MobilityAgent()

        self.prob_history = [[] for i in range(3)]
        self.opponent_strategies = [[] for i in range(3)]
        self.prior = [1 / 3, 1 / 3, 1 / 3]
        self.posterior = [1 / 3, 1 / 3, 1 / 3]

    def update_iteration(self, state, last_action):
        """
        Add the opponent's move to the accumulative history and use this this to
        update the posterior belief of the opponent types.
        """
        self.extend_prob_history(last_action)
        self.update_posteriors()

    def update_posteriors(self):
        """On each turn update posterior beliefs"""
        likelihood = self.likelihood_gtw()

        # Calculate unnormalised posterior by multiplying the prior and likelihood
        likelihoods = []
        likelihoods.append(likelihood[0] * self.prior[0])
        likelihoods.append(likelihood[1] * self.prior[1])
        likelihoods.append(likelihood[2] * self.prior[2])

        # Calculate normalising constant
        summ = likelihoods[0] + likelihoods[1] + likelihoods[2]

        # Create posterior
        self.posterior[0] = likelihoods[0] / summ
        self.posterior[1] = likelihoods[1] / summ
        self.posterior[2] = likelihoods[2] / summ

    def likelihood_gtw(self):
        """Method that specifies how evidence accounted for (acts upon prob_history)."""

        index_latest_move = len(self.prob_history[0]) - 1
        prob_array = np.asarray(self.prob_history)

        time_steps = []
        for i in range(index_latest_move, -1, -1):
            time_steps.append(i)

        if not time_steps:
            time_steps.append(0)

        time_step_array = np.asarray(time_steps)

        # Create the weights that determine the drop off rate
        c = np.power(time_step_array, 5) * 0.01
        weights = np.subtract(10, c)
        mask = np.greater(weights, 0)
        weights = mask * weights

        # Matrix multiply H and transpose(w)
        l_mat = np.dot(prob_array, np.transpose(weights))
        return l_mat.tolist()

    def update_opponent_strategies(self, state, legal_moves):
        """
        `opponent_strategies` are the moves that each pure type of agent would play
        given the current game state. This method updates the strategies for the current
        game state.
        """
        # Fill the list with the possible moves
        self.opponent_strategies[0] = self.type1.get_all_actions(state, legal_moves)
        self.opponent_strategies[1] = self.type2.get_all_actions(state, legal_moves)
        self.opponent_strategies[2] = self.type3.get_all_actions(state, legal_moves)

    def extend_prob_history(self, last_action):
        """Update prob_history"""

        for i in range(3):  # One for each agent
            # Case when opposition had no moves in the past stage
            if not last_action:
                self.prob_history[0].append(1)
                self.prob_history[1].append(1)
                self.prob_history[2].append(1)
                break

            # Case when this type had no possible actions in the past stage
            if not self.opponent_strategies[i]:
                self.prob_history[i].append(0)

            # If action matches that which the type would have made make it 1, else 0
            if last_action in self.opponent_strategies[i]:
                self.prob_history[i].append(1)
            else:
                self.prob_history[i].append(0)
