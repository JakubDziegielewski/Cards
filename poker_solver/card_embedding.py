import torch.nn as nn
import torch.nn.functional as F

class CardEmbedding(nn.Module):
    def __init__(self, dim):
        super(CardEmbedding, self).__init__()
        self.rank = nn.Embedding(13, dim)
        self.suit = nn.Embedding(4, dim)
        self.card = nn.Embedding(52, dim)
        
    def forward(self, input):
        B, num_cards = input.shape
        x = input.view(-1)
        valid = x.ge(0).float()
        x = x.clamp(min=0)
        embs = self.card(x) + self.rank(x // 4) + self.suit(x % 4)
        embs = embs * valid.unsqueeze(1)
        
        return embs.view(B, num_cards, -1).sum(1)