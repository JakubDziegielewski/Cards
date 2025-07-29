from deck.deck import Deck
from deck.card import Card, Rank, Suit

class PokerSolver:
    def __init__(self, bucket_number:int) -> None:
        self.nodes = None
    
    