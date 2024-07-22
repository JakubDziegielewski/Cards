from five_cards.hand_state import HandState
from deck.deck import Deck
from deck.card import Card, Rank
from five_cards.player import Player
from five_cards.bet import Bet
import numpy as np



class Hand:
    def __init__(self, players: dict[int, Player], starting_player_id: int) -> None:
        self.players = players
        self.starting_player_id = starting_player_id
        self.number_of_cards_per_player = {
            player.get_id(): player.get_number_of_cards()
            for player in self.players.values()
        }
        self.cards_on_table = sum(self.number_of_cards_per_player.values())
        self.hand_state = HandState(starting_player_id)

    def deal_cards(self, deck: Deck) -> None:
        deck.shuffle()
        for player in self.players.values():
            number_of_cards = player.get_number_of_cards()
            drawn_cards = deck.draw_cards(number_of_cards)
            player.set_cards(drawn_cards)

    def return_cards(self, deck: Deck) -> None:
        cards_for_return = np.array([])
        for player in self.players.values():
            cards_for_return = np.append(cards_for_return, player.get_cards())
        deck.return_cards(cards_for_return)
        for player in self.players.values():
            player.set_cards(None)


    def get_players(self) -> dict[int, Player]:
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

    def get_number_of_cards_per_player(self) -> dict[int, int]:
        return self.number_of_cards_per_player
    
    def get_id_of_called_player(self, calling_player_id: int) -> int:
        list_of_ids = list(self.players.keys())
        calling_player_index = list_of_ids.index(calling_player_id)
        called_player_index = (calling_player_index - 1) % len(self.get_players())
        return list_of_ids[called_player_index]
    
    def calculate_actual_quantity(self, card_rank: Rank) -> int:
        actual_quantity = 0
        for player in self.players.values():
            ranks = map(Card.get_rank, player.get_cards())
            ranks = np.fromiter(ranks, dtype=Rank)
            actual_quantity += sum(ranks == card_rank)
            actual_quantity += sum(ranks == Rank(2))
        return actual_quantity
