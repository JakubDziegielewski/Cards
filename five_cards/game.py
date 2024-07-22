from five_cards.game_state import GameState
from five_cards.hand import Hand
from deck.deck import Deck
from deck.card import Card, Rank
from five_cards.call import Call

import numpy as np


class Game:
    def __init__(self, number_of_players) -> None:
        self.game_state = GameState(number_of_players)
        self.deck = Deck([2, 9, 10, "J", "Q", "K", "A"])
        

    def calculate_id_of_next_starting_player(self) -> None:
        id_of_starting_player = self.game_state.get_starting_player_id()
        list_of_ids = list(self.game_state.get_players().keys())
        starting_player_index = list_of_ids.index(id_of_starting_player)
        next_strting_player_index = (starting_player_index + 1) % len(
            self.game_state.get_players()
        )
        self.game_state.set_starting_player_id(list_of_ids[next_strting_player_index])

    def get_game_state(self) -> GameState:
        return self.game_state

    def get_deck(self) -> Deck:
        return self.deck

    def start_hand(self) -> Hand:
        starting_player_id = self.game_state.starting_player_id
        hand = Hand(self.game_state.players, starting_player_id)
        hand.deal_cards(self.deck)
        return hand
