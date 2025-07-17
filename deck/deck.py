import numpy as np
from typing import Literal
from deck.card import *


class Deck:
    def __init__(self, ranks: list = None, suits: list = None) -> None:
        self.ranks = ranks
        self.suits = suits
        self.init_deck()
        self.deck_size = self.cards.size
        self.init_cards = self.cards
        self.init_size = self.init_cards.size

    def init_deck(self) -> None:
        if self.ranks is None and self.suits is None:
            self.cards = np.array([Card(rank, suit) for rank in Rank for suit in Suit], dtype=Card)
        elif self.suits is None:
            self.cards = np.array(
                [Card(rank, suit) for rank in map(Rank, self.ranks) for suit in Suit], dtype=Card
            )
        elif self.ranks is None:
            self.cards = np.array(
                [Card(rank, suit) for rank in Rank for suit in map(Suit, self.suits)], dtype=Card
            )
        else:
            self.cards = np.array(
                [
                    Card(rank, suit)
                    for rank in map(Rank, self.ranks)
                    for suit in map(Suit, self.suits)
                ], dtype=Card
            )
        self.deck_size = self.cards.size

    def reset(self) -> None:
        self.cards = np.array(self.init_cards, dtype=Card)
        self.deck_size = self.init_size

    def shuffle(self) -> None:
        np.random.shuffle(self.cards)

    def draw_cards(
        self, number_of_cards: int, position: Literal["top", "bottom"] = "top"
    ) -> np.ndarray:
        if position == "top":
            self.cards, drawn_cards = self.cards[:self.deck_size - number_of_cards], self.cards[self.deck_size - number_of_cards:]
        elif position == "bottom":
            self.cards, drawn_cards = self.cards[number_of_cards:], self.cards[:number_of_cards]
        self.deck_size -= number_of_cards
        return drawn_cards

    def return_cards(
        self, returned_cards: np.ndarray, position: Literal["top", "bottom"] = "top"
    ) -> None:
        if position == "top":
            self.cards = np.concatenate((self.cards, returned_cards))
        elif position == "bottom":
            self.cards = np.concatenate((returned_cards, self.cards))
        self.deck_size += returned_cards.size

    def get_top_card(self) -> Card:
        return self.cards[self.deck_size - 1]

    def get_bottom_card(self) -> Card:
        return self.cards[0]

    def get_cards(self) -> np.array:
        return self.cards[: self.deck_size]

    def draw_card_by_tag(self, tag: str) -> np.ndarray:
        cards = self.get_cards()
        index = next((i for i, card in enumerate(cards) if card.get_tag() == tag), None)
        first_half = self.get_cards()[:index]
        second_half = self.get_cards()[index + 1 :]
        card = cards[index]
        self.cards[:self.deck_size] = np.concatenate((first_half, second_half, [card]))
        return self.draw_cards(1)
        
