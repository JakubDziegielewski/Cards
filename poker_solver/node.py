from poker_solver.sequence import Sequence
import numpy as np

class Node:
    def __init__(self, sequence: Sequence):
        if not sequence.ends_round and not sequence.ends_hand:
            self.num_actions = 3 if sequence.betting_sequence[-1].count("B") < 4 else 2
            self.regret_sum = np.zeros(self.num_actions)
            self.strategy_sum = np.zeros(self.num_actions)
        self.visited = 0
    
    def get_strategy(self) -> np.ndarray:
        positive_regrets = np.maximum(self.regret_sum, 0)
        normalizing_sum = positive_regrets.sum()
        if normalizing_sum > 0:
            return positive_regrets / normalizing_sum
        else:
            return np.ones(self.num_actions) / self.num_actions

    def get_average_strategy(self) -> np.ndarray:
        normalizing_sum = self.strategy_sum.sum()
        if normalizing_sum > 0:
            return self.strategy_sum / normalizing_sum
        else:
            return np.ones(self.num_actions) / self.num_actions