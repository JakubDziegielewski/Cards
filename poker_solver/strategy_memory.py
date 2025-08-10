from collections import deque
from random import sample


class StrategyMemory:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def add(self, state, strategy):
        self.buffer.append((state, strategy))

    def sample(self, batch_size):
        return sample(self.buffer, min(len(self.buffer), batch_size))

    def __len__(self):
        return len(self.buffer)