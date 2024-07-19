from five_cards.bet import Bet


class HandState:
    def __init__(self, current_player_id: int) -> None:
        self.current_player_id = current_player_id
        self.current_bet = None
        self.bet_history = list()

    def get_current_player_id(self) -> int:
        return self.current_player_id

    def set_current_player_id(self, player_id: int) -> None:
        self.current_player_id = player_id

    def get_current_bet(self) -> Bet:
        return self.current_bet

    def set_current_bet(self, bet) -> None:
        self.current_bet = bet
        self.bet_history.append((self.current_player_id, self.current_bet))

    def get_bet_history(self) -> list:
        return self.bet_history
