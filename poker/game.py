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
        hand = Hand(self.game_state, self.deck, 2)
        hand.deal_cards()
        print(hand.players)
        first_to_act = (self.game_state.current_dealer + 3) % self.game_state.players.size if self.game_state.players.size > 2 else  self.game_state.current_dealer
        hand.betting_round(first_to_act)
        print(np.array2string(hand.flop, separator="; "))
        if hand.active_players - hand.players_all_in > 1:
            hand.betting_round((self.game_state.current_dealer + 1) % self.game_state.players.size)
        print(hand.turn)
        if hand.active_players - hand.players_all_in > 1:
            hand.betting_round((self.game_state.current_dealer + 1) % self.game_state.players.size)
        print(hand.river)
        if hand.active_players - hand.players_all_in > 1:
            hand.betting_round((self.game_state.current_dealer + 1) % self.game_state.players.size)
        print(self.game_state.players)
        
        