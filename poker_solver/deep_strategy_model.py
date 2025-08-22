from poker_solver.deep_cfr_model import DeepCFRModel
import torch.nn as nn

class DeepStrategyModel(DeepCFRModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.soft = nn.Softmax(1)
        
    def forward(self, cards, bets):
        regrets = super().forward(cards, bets)
        return self.soft(regrets)