from poker_solver.deep_cfr_model import DeepCFRModel
from torch.nn.functional import softmax

class DeepStrategyModel(DeepCFRModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def forward(self, cards, bets):
        regrets = super().forward(cards, bets)
        return softmax(regrets, dim=-1)