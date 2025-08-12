import torch
import torch.nn as nn
import torch.nn.functional as F
from poker_solver.card_embedding import CardEmbedding

class DeepCFRModel(nn.Module):
    def __init__(self, ncardtypes, nbets, nactions, card_embeddings, dim=64):
        super(DeepCFRModel, self).__init__()
        self.card_embeddings = card_embeddings
        self.card1 = nn.Linear(dim * ncardtypes, dim * ncardtypes)
        self.card2 = nn.Linear(dim * ncardtypes, dim * ncardtypes)
        self.card3 = nn.Linear(dim * ncardtypes, dim)
        
        self.bet1 = nn.Linear(nbets * 2, dim)
        self.bet2 = nn.Linear(dim, dim)
        
        self.comb1 = nn.Linear(2 * dim, dim)
        self.comb2 = nn.Linear(dim, dim)
        self.comb3 = nn.Linear(dim, dim)
        
        self.action_head = nn.Linear(dim, nactions)
        nn.init.zeros_(self.action_head.weight)
        nn.init.zeros_(self.action_head.bias)
        
    def forward(self, cards, bets):
        card_groups = [
            cards[:, 0:2],
            cards[:, 2:5],
            cards[:, 5:7]
        ]
        card_embs = []
        for embedding, card_group in zip(self.card_embeddings, card_groups):
            card_embs.append(embedding(card_group))
        card_embs = torch.cat(card_embs, dim=1)
        
        x = F.relu(self.card1(card_embs))
        x = F.relu(self.card2(x))
        x = F.relu(self.card3(x))
        
        bet_size = bets.clamp(0, 1e6)
        bet_occured = bets.ge(0)
        bet_feats = torch.cat([bet_size, bet_occured.float()], dim=1)
        y = F.relu(self.bet1(bet_feats))
        y = F.relu(self.bet2(y) + y)
        
        z = torch.cat([x, y], dim=1)
        z = F.relu(self.comb1(z))            
        z = F.relu(self.comb2(z) + z)            
        z = F.relu(self.comb3(z) + z) 
        
        z = (z - torch.mean(z)) / torch.std(z)
        return self.action_head(z)
        
    def reset_weights(self):
        """
        Reinitialize all weights in the network.
        Call like: model.reset_weights()
        """
        for m in self.modules():
            if isinstance(m, nn.Embedding) or m is self.action_head:
                continue
            elif hasattr(m, 'reset_parameters'):
                m.reset_parameters()
            else:
                classname = m.__class__.__name__
                if classname.find('Linear') != -1 or classname.find('Conv') != -1:
                    if hasattr(m, 'weight') and m.weight is not None:
                        torch.nn.init.kaiming_uniform_(m.weight, a=0, mode='fan_in', nonlinearity='relu')
                    if hasattr(m, 'bias') and m.bias is not None:
                        torch.nn.init.constant_(m.bias, 0)
        nn.init.zeros_(self.action_head.weight)
        nn.init.zeros_(self.action_head.bias)        
        