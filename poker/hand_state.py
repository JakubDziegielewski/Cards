
class HandState:
    def __init__(self):
        self.current_round = 0
        self.current_bet = None
        self.pot = 0
        self.history = {
            0: "",
            1: "",
            2: "",
            3: "",
        }
        self.public_cards = None
    
    def next_round(self) -> None:
        self.current_round += 1 
    
    def add_action(self, action_symbol: str) -> None:
       self.history[self.current_round] += action_symbol