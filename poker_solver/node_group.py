import numpy as np
from poker_solver.node import Node
from poker_solver.sequence import Sequence

class NodeGroup:
    def __init__(self, sequence: Sequence, buckets:int):
        if sequence.ends_hand or sequence.ends_round:
            buckets = 1
        self.ends_hand = sequence.ends_hand
        self.ends_round = sequence.ends_round
        self.nodes = np.array([Node(sequence) for _ in range(buckets)])
    
    def __getitem__(self, key: int) -> Node:
        return self.nodes[key]