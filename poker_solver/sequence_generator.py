from poker_solver.sequence import Sequence


class SequenceGenerator:
    def __init__(self):
        self.preflop_sequences = self._generate_preflop_sequences()
        self.flop_sequences = self._generate_later_sequences(self.preflop_sequences)
        self.turn_sequences = self._generate_later_sequences(self.flop_sequences)
        self.river_sequences = self._generate_later_sequences(self.turn_sequences)
        

    def _generate_preflop_sequences(self):
        preflop_sequences = [
            "B",
            "BF",
            "BC",
            "BB",
            "BCF",
            "BCP",
            "BCB",
            "BCBF",
            "BCBC",
            "BCBB",
            "BCBBF",
            "BCBBC",
            "BCBBB",
            "BCBBBF",
            "BCBBBC",
            "BBF",
            "BBC",
            "BBB",
            "BBBF",
            "BBBC",
            "BBBB",
            "BBBBF",
            "BBBBC"
        ]
        return [Sequence((sequence,)) for sequence in preflop_sequences]

    def _generate_later_sequences(self, previous_sequences):
        postflop_sequences = [
            "",
            "F",
            "P",
            "PF",
            "PP",
            "PB",
            "PBF",
            "PBC",
            "PBB",
            "PBBF",
            "PBBC",
            "PBBB",
            "PBBBF",
            "PBBBC",
            "PBBBB",
            "PBBBBF",
            "PBBBBC",
            "B",
            "BF",
            "BC",
            "BB",
            "BBF",
            "BBC",
            "BBB",
            "BBBF",
            "BBBC",
            "BBBB",
            "BBBBF",
            "BBBBC"
        ]
        return [Sequence((previous_sequence.betting_sequence + (postflop_sequence,))) for previous_sequence in previous_sequences for postflop_sequence in postflop_sequences if previous_sequence.ends_round and not previous_sequence.ends_hand]
    
    def get_all_sequences(self):
        return self.preflop_sequences + self.flop_sequences + self.turn_sequences + self.river_sequences