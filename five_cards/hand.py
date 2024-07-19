from five_cards.hand_state import HandState
from deck.deck import Deck
from five_cards.player import Player
from five_cards.bet import Bet


class Hand:
    def __init__(self, players: dict, starting_player_id: int) -> None:
        self.players = players
        self.starting_player_id = starting_player_id
        self.number_of_cards_per_player = {
            player.get_id(): player.get_number_of_cards()
            for player in self.players.values()
        }
        self.cards_on_table = sum(self.number_of_cards_per_player.values())
        self.hand_state = HandState(starting_player_id)
        self.is_finished = False

    def deal_cards(self, deck: Deck) -> None:
        deck.shuffle()
        for key in self.players.keys().__iter__():
            player = self.players[key]
            number_of_cards = player.get_number_of_cards()
            drawn_cards = deck.draw_cards(number_of_cards)
            player.set_cards(drawn_cards)

    def return_cards(self, deck: Deck) -> None:
        for key in self.players.keys().__iter__():
            player = self.players[key]
            deck.return_cards(player.get_cards())

    def get_players(self) -> dict:
        return self.players

    def get_hand_state(self) -> HandState:
        return self.hand_state

    def update_a_bet(self, bet: Bet) -> None:
        self.hand_state.set_current_bet(bet)
        self.change_turn()

    def change_turn(self) -> None:
        current_player_id = self.hand_state.get_current_player_id()
        list_of_ids = list(self.players.keys())
        index = list_of_ids.index(current_player_id)
        index = (index + 1) % len(self.players)
        next_player_id = list_of_ids[index]
        self.hand_state.set_current_player_id(next_player_id)

    def get_current_player(self) -> Player:
        current_player_id = self.hand_state.get_current_player_id()
        return self.players[current_player_id]

    def get_number_of_cards_per_player(self) -> dict:
        return self.number_of_cards_per_player
