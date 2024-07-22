from deck.card import Rank
from five_cards.bet import Bet
import numpy as np


class Player:
    def __init__(self, id: int) -> None:
        self.id = id
        self.number_of_cards = 1
        self.cards = None

    def check_if_lost(self) -> bool:
        return self.number_of_cards > 5

    def add_one_card(self) -> None:
        self.number_of_cards += 1

    def get_id(self) -> int:
        return self.id

    def get_cards(self) -> np.ndarray:
        return self.cards

    def set_cards(self, cards: np.array) -> None:
        self.cards = cards

    def get_number_of_cards(self) -> int:
        return self.number_of_cards

    def call_a_bet() -> None:
        pass

    def make_a_bet(self, quantity: int, card_rank: Rank) -> Bet:
        return Bet(quantity, card_rank)

    def __eq__(self, value: object) -> bool:
        if type(value) is not Player:
            return False
        return self.id == value.id
