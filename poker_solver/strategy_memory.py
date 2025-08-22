import torch
    
class StrategyMemory:
    def __init__(self, capacity, num_cards=7, num_bets=24, num_actions=3):

        self.capacity = capacity
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Preallocate storage
        self.cards = torch.zeros((capacity, num_cards), dtype=torch.int8, device=self.device)
        self.bets = torch.zeros((capacity, num_bets), dtype=torch.int8, device=self.device)
        self.strategies = torch.zeros((capacity, num_actions), dtype=torch.float16, device=self.device)
        self.index = 0
        self.full = False

    def add(self, cards, bets, strategy):
        """
        Add a batch of samples to memory.
        
        Args:
            states (Tensor): Shape (B, *state_shape)
            advantages (Tensor): Shape (B, num_actions)
        """
        self.cards[self.index] = cards
        self.bets[self.index] = bets
        self.strategies[self.index] = strategy
        self.index = self.index + 1
        if self.index == self.capacity:
            self.index = 0
            self.full = True

    def sample(self, batch_size):
        """
        Sample a random batch from memory.
        """
        max_index = self.capacity if self.full else self.index
        idx = torch.randint(0, max_index, (batch_size,), device=self.device)
        return self.cards[idx], self.bets[idx], self.strategies[idx]

    def __len__(self):
        return self.capacity if self.full else self.index