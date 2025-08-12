from collections import deque
from random import sample

class AdvantageMemory:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def add(self, card_tensor, bet_tensor, advantage):
        self.buffer.append((card_tensor, bet_tensor, advantage))

    def sample(self, batch_size):
        return sample(self.buffer, min(len(self.buffer), batch_size))

    def __len__(self):
        return len(self.buffer)