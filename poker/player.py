import numpy as np
from deck.card import Card
from poker.bet import Bet
from poker.call import Call
from poker.fold import Fold
from poker.check import Check


class Player:
    def __init__(self, id: int, stack: int):
        self.id = id
        self.cards = None
        self.stack = stack
        self.current_bet = Bet(0)
        self.is_all_in = False
        self.has_folded = False

    def get_cards(self) -> np.ndarray[Card, 2] | None:
        return self.cards

    def set_cards(self, cards: np.ndarray[Card, 2]) -> None:
        self.cards = cards

    def get_stack(self) -> int:
        return self.stack

    def set_stack(self, stack: int) -> None:
        self.stack = stack
    
    def __repr__(self) -> str:
        if self.cards is not None:
            return f"Player {self.id}; cards: {self.cards[0]} and {self.cards[1]}; stack: {self.stack}"
        else:
            return f"Player {self.id}; stack: {self.stack}"
        
    def make_a_bet(self, size: int) -> Bet:
        max_size = self.find_max_bet_size()
        if max_size <= size:
            size = max_size
            self.is_all_in = True
        new_bet = Bet(size)
        self.stack -= size - self.current_bet.size
        self.current_bet = new_bet
        return new_bet
    
    def call_a_bet(self, bet: Bet) -> Call:
        max_size = self.find_max_bet_size()
        call_size = bet.size
        if bet.size >= max_size:
            call_size = max_size
            self.is_all_in = True
        
        
        call = Call(Bet(call_size))
        self.stack -= call.size - self.current_bet.size
        self.current_bet = Bet(call_size)
        return call

    def find_max_bet_size(self) -> int:
        return self.current_bet.size + self.stack
        
    def fold(self):
        pass
    
    def make_decision(self, current_bet: Bet, bet_size:int, number_of_bets:int) -> Bet | Call | Fold:
        print(f"Current bet: {current_bet.size}")
        legal_actions = ["fold"]
        if self.is_check_legal(current_bet):
            legal_actions.append("check")
        else:
            legal_actions.append("call")
        if number_of_bets < 4 and self.is_bet_legal(current_bet):
            legal_actions.append("bet")
        chosen_action = " "
        while chosen_action not in ["1", "2", "3"]:
            print("Choose action:")    
            for i, action in enumerate(legal_actions, start=1):
                print(f"{i}. {action}")
            chosen_action = input("Enter selection: ")
            #chosen_action = "2"
            #action = np.random.choice(legal_actions)
            #lookup_table = {
            #    "fold": "1",
            #    "check": "2",
            #    "call": "2",
            #    "bet": "3"
            #}
            #chosen_action = lookup_table[action]
        if chosen_action == "1":
            self.has_folded = True
            return Fold()
        if chosen_action == "2":
            if "check" in legal_actions:
                return Check()
            call = self.call_a_bet(current_bet)
            return Call(call)
        if chosen_action == "3":
            correct_value = False
            while not correct_value:
                #bet_size = int(input("Enter bet size: "))
                bet_size = current_bet.size + bet_size
                if bet_size > current_bet.size:
                    correct_value = True
            return self.make_a_bet(bet_size)
                
             
            
                
    def is_check_legal(self, bet: Bet) -> bool:
        return self.current_bet.size == bet.size

    def is_bet_legal(self, bet: Bet) -> bool:
        return self.current_bet.size + self.stack > bet.size
    
    def is_call_legal(self, bet: Bet) -> bool:
        return not self.is_check_legal(bet)
    