"""
Top level script to play game of Reversi.

Adapted from Andy Salerno (2016)
"""

import time
from sys import argv

from agents import hba_agent, human_agent
from constants import BLACK, COLOUR_STR, WHITE
from game.othello import Othello
from util import *

agent_mapping = {
    # 'q_learning': q_learning_agent.QLearningAgent,
    # 'monte_carlo': monte_carlo_agent.MonteCarloAgent,
    "human": human_agent.HumanAgent,
    "hba": hba_agent.HBAAgent,
    # 'simulated_agent1': agent1.Agent1,
    # 'agent4_pert':agent4_pert.Agent4P,
}


def main(**kwargs):

    input_args = prop_parse(argv)
    input_args.update(kwargs)

    if len(argv) <= 1 and len(kwargs) <= 1:
        print(
            "required inputs:\n\tBlackAgent=, WhiteAgent=\n\tchoices: q_learning, "
            "monte_carlo, random, human\n"
            "optional inputs: \n\tsize=(board size), num_games=(#games), "
            "silent=(True/False), sim_time=(seconds for monte carlo sim)"
        )
        quit()

    for k, v in input_args.items():
        # convert 'human' to human_agent.HumanAgent, etc
        if v in agent_mapping:
            input_args[k] = agent_mapping[v]
        elif v == "q_learning":
            from agents import q_learning_agent

            input_args[k] = q_learning_agent.QLearningAgent

    num_games = input_args.get("num_games", 1)
    make_silent(input_args.get("silent", False))

    print(
        f"About to run {num_games} games, black as {input_args['BlackAgent'].__name__}"
        f", white as {input_args['WhiteAgent'].__name__}."
    )

    summary = []
    white_wins = 0
    black_wins = 0
    othello = Othello(**input_args)
    start = time.time()
    for game_idx in range(1, num_games + 1):
        info(f"Starting game {game_idx} of {num_games}")

        winner, white_score, black_score = othello.play_game()

        if winner == WHITE:
            white_wins += 1
        elif winner == BLACK:
            black_wins += 1
        info("game {} complete.".format(game_idx))
        message = "{} wins! {}-{}".format(COLOUR_STR[winner], white_score, black_score)
        info(message)
        summary.append(message)

    seconds_spent = time.time() - start
    ms_per_game = (seconds_spent / num_games) * 1000
    print(
        "time: {0:.2f} minutes ({0:.2f}ms per game)".format(
            seconds_spent / 60, ms_per_game
        )
    )
    print("summary: {} games played".format(len(summary)))
    for each in summary:
        info(each)
    wins = {
        "Black": black_wins / (black_wins + white_wins) * 100,
        "White": white_wins / (black_wins + white_wins) * 100,
    }
    print("Black won {}%".format(wins["Black"]))
    print("White won {}%".format(wins["White"]))

    return wins


if __name__ == "__main__":
    # NB. White agent has to be an HBA agent.
    main(BlackAgent="human", WhiteAgent="hba", sim_time=10)
