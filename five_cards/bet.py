from deck.card import Rank


class Bet:
    def __init__(self, quantity: int, card_rank: Rank) -> None:
        if quantity < 1 or quantity > 8:
            raise ValueError("Invalid number of cards!")
        self.quantity = quantity
        self.card_rank = card_rank

    def __eq__(self, value: object) -> bool:
        if type(value) is not Bet:
            return False
        return self.quantity == value.quantity and self.card_rank == value.card_rank

    def __gt__(self, other):
        if other is None:
            return True
        if type(other) is not Bet:
            raise ValueError("Cannot compare these two objects")
        return self.quantity > other.quantity or (
            self.quantity == other.quantity and self.card_rank > other.card_rank
        )

    def __str__(self) -> str:
        suffix = "" if self.quantity == 1 else "s"
        return str(self.quantity) + " " + self.card_rank.name + suffix

    def get_quantity(self) -> int:
        return self.quantity

    def get_card_rank(self) -> Rank:
        return self.card_rank
