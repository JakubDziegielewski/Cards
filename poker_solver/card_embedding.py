import torch
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
        x = input.contiguous().view(-1)
        valid = x.ge(0).float()
        x = x.clamp(min=0)
        new_x = x.clone().detach().type(torch.int64)
        embs = self.card(new_x) + self.rank(new_x // 4) + self.suit(new_x % 4)
        embs = embs * valid.unsqueeze(1)
        
        return embs.view(B, num_cards, -1).sum(1)