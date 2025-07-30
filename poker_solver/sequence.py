from typing import Tuple


class Sequence:
    def __init__(self, sequence: Tuple):
        self.betting_sequence = sequence
        self.ends_round = self._ends_round()
        self.ends_hand = self._ends_hand()

    def _ends_round(self) -> bool:
        if self.betting_sequence[-1] == "":
            return False
        if len(self.betting_sequence) > 1:
            return (
                self.betting_sequence[-1][-1] in ["C", "F"]
                or self.betting_sequence[-1][-2:] == "PP"
            )
        else:
            return self.betting_sequence[-1][-1] in ["P", "F"] or (
                self.betting_sequence[-1][-1] == "C"
                and len(self.betting_sequence[-1]) > 2
            )

    def _ends_hand(self) -> bool:
        if self.betting_sequence[-1] == "":
            return False
        return self.betting_sequence[-1][-1] == "F" or (
            len(self.betting_sequence) == 4 and self.ends_round
        )

    def __repr__(self):
        return str(self.betting_sequence)