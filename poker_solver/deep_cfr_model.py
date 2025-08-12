import torch
import torch.nn as nn
import torch.nn.functional as F
from poker_solver.card_embedding import CardEmbedding

class DeepCFRModel(nn.Module):
    def __init__(self, ncardtypes, nbets, nactions, dim=64):
        super(DeepCFRModel, self).__init__()
        self.card_embeddings = nn.ModuleList(
            [CardEmbedding(dim) for _ in range(ncardtypes)]
        )
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.card1 = nn.Linear(dim * ncardtypes, dim * ncardtypes, device=self.device)
        self.card2 = nn.Linear(dim * ncardtypes, dim * ncardtypes, device=self.device)
        self.card3 = nn.Linear(dim * ncardtypes, dim, device=self.device)
        
        self.bet1 = nn.Linear(nbets * 2, dim, device=self.device)
        self.bet2 = nn.Linear(dim, dim, device=self.device)
        
        self.comb1 = nn.Linear(2 * dim, dim, device=self.device)
        self.comb2 = nn.Linear(dim, dim, device=self.device)
        self.comb3 = nn.Linear(dim, dim, device=self.device)
        self.action_head = nn.Linear(dim, nactions, device=self.device)
        
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
        bet_occured = bets.ge(0).to(self.device)
        bet_feats = torch.cat([bet_size, bet_occured.float()], dim=1).to(self.device)
        y = F.relu(self.bet1(bet_feats))
        y = F.relu(self.bet2(y) + y)
        
        z = torch.cat([x, y], dim=1)
        z = F.relu(self.comb1(z))            
        z = F.relu(self.comb2(z) + z)            
        z = F.relu(self.comb3(z) + z) 
        
        z = (z - torch.mean(z)) / torch.std(z)
        return self.action_head(z)
           