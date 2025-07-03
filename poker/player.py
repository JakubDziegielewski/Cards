import numpy as np
from deck.card import Card


class Player:
    def __init__(self, id: int, stack: int):
        self.id = id
        self.cards = None
        self.stack = stack

    def get_cards(self) -> np.ndarray[Card, 2] | None:
        return self.cards

    def set_cards(self, cards: np.ndarray[Card, 2]) -> None:
        self.cards = cards

    def get_stack(self) -> int:
        return self.stack

    def set_stack(self, stack: int) -> None:
        self.stack = stack
    
    def __repr__(self) -> str:
        if self.cards is not None:
            return f"Player {self.id}; cards: {self.cards[0]} and {self.cards[1]}; stack: {self.stack}"
        else:
            return f"Player {self.id}; stack: {self.stack}"
        
