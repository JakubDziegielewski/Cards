from poker.player import Player
from poker.game_state import GameState
from deck.deck import Deck
import numpy as np
from poker.hand import Hand


class Game:
    def __init__(self, init_number_of_players: int, init_stack_size: int, deck: Deck=Deck()):
        self.game_state = GameState(np.array([Player(i, init_stack_size) for i in range(init_number_of_players)]), current_dealer = 0)
        self.deck = deck
    
    def __repr__(self) -> str:
        return str(self.game_state)

    def start_hand(self):
        self.deck.reset()
        hand = Hand(self.game_state, self.deck)
        hand.deal_cards()
        print(hand.players)