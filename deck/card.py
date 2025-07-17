from enum import Enum


class Rank(Enum):
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = "T"
    Jack = "J"
    Queen = "Q"
    King = "K"
    Ace = "A"

    def __gt__(self, other: object):
        if type(other) is not Rank:
            raise ValueError("Cannot compare these two objects")
        face_values = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
        self_value = self.value
        other_value = other.value
        if type(self.value) is str:
            self_value = face_values[self_value]
        if type(other_value) is str:
            other_value = face_values[other_value]
        return self_value > other_value

    def __lt__(self, other: object):
        if type(other) is not Rank:
            raise ValueError("Cannot compare these two objects")
        return other > self


class Suit(Enum):
    Spade = "spade"
    Club = "club"
    Diamond = "diamond"
    Heart = "heart"


class Card:
    def __init__(self, rank: Rank, suit: Suit) -> None:
        if type(rank) is not Rank:
            raise ValueError("Invalid Rank value")
        if type(suit) is not Suit:
            raise ValueError("Invalid Suit value")
        self.rank = rank
        self.suit = suit
        self.tag = str(self.rank.value) + self.suit.value[0]
        self.card_number = Card.define_card_number(rank, suit)
        
    @staticmethod
    def define_card_number(rank: Rank, suit: Suit) -> int:
        suit_table = {"club": 0, "diamond": 1, "heart": 2, "spade": 3}
        face_values = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
        value = rank.value
        if type(rank.value) is str:
            value = face_values[rank.value]
        return 4 * (value - 2) + suit_table[suit.value]
            

    def __repr__(self) -> str:
        return self.rank.name + " of " + self.suit.name + "s"

    def __eq__(self, card: object) -> bool:
        if type(card) is not Card:
            return False
        return self.rank == card.rank and self.suit == card.suit

    def __lt__(self, other: object) -> bool:
        return self.rank < other.get_rank()

    def __gt__(self, other: object) -> bool:
        return self.rank > other.get_rank()

    def get_rank(self) -> Rank:
        return self.rank

    def get_suit(self) -> Suit:
        return self.suit
    
    def get_tag(self) -> str:
        return self.tag