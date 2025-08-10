from collections import deque
from random import sample

class AdvantageMemory:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def add(self, state, action, advantage):
        self.buffer.append((state, action, advantage))

    def sample(self, batch_size):
        return sample(self.buffer, min(len(self.buffer), batch_size))

    def __len__(self):
        return len(self.buffer)