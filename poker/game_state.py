import numpy as np
from poker.player import Player

class GameState:
    def __init__(self, players: np.ndarray[Player], current_dealer: int = 0):
        self.players = players
        self.current_dealer = current_dealer
    
    def change_dealer(self) -> None:
        self.current_dealer = (self.current_dealer + 1) % self.players.size
    
    def __repr__(self):
        array_string = np.array2string(self.players, separator='\n')
        return f"{array_string}; current dealer: {self.current_dealer}"
        