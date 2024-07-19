import numpy as np
from typing import Literal
from deck.card import *


class Deck:
    def __init__(self, ranks: list = None, suits: list = None) -> None:
        self.ranks = ranks
        self.suits = suits
        self.reset()
        self.deck_size = self.cards.size

    def reset(self) -> None:
        if self.ranks is None and self.suits is None:
            self.cards = np.array([Card(rank, suit) for rank in Rank for suit in Suit])
        elif self.suits is None:
            self.cards = np.array(
                [Card(rank, suit) for rank in map(Rank, self.ranks) for suit in Suit]
            )
        elif self.ranks is None:
            self.cards = np.array(
                [Card(rank, suit) for rank in Rank for suit in map(Suit, self.suits)]
            )
        else:
            self.cards = np.array(
                [
                    Card(rank, suit)
                    for rank in map(Rank, self.ranks)
                    for suit in map(Suit, self.suits)
                ]
            )

    def shuffle(self) -> None:
        np.random.shuffle(self.cards[: self.deck_size])

    def draw_cards(
        self, number_of_cards: int, position: Literal["top", "bottom"] = "top"
    ) -> np.array:
        if position == "top":
            drawn_cards = self.cards[self.deck_size - number_of_cards : self.deck_size]
        elif position == "bottom":
            drawn_cards = self.cards[:number_of_cards]
            self.cards = np.roll(self.cards, -number_of_cards)
        self.deck_size -= number_of_cards
        return drawn_cards

    def return_cards(
        self, returned_cards: np.array, position: Literal["top", "bottom"] = "top"
    ) -> None:
        if position == "top":
            self.cards[self.deck_size : self.deck_size + returned_cards.size] = (
                returned_cards
            )
        elif position == "bottom":
            self.cards = np.roll(self.cards, returned_cards.size)
            self.cards[: returned_cards.size] = returned_cards
        self.deck_size += returned_cards.size

    def get_top_card(self) -> Card:
        return self.cards[self.deck_size - 1]

    def get_bottom_card(self) -> Card:
        return self.cards[0]

    def get_cards(self) -> np.array:
        return self.cards[: self.deck_size]
