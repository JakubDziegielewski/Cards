from five_cards.game_state import GameState
from five_cards.hand import Hand
from deck.deck import Deck
from deck.card import Card, Rank
from five_cards.call import Call
from five_cards.console_interface import ConsoleInterface
import numpy as np


class Game:
    def __init__(self, number_of_players) -> None:
        self.game_state = GameState(number_of_players)
        self.deck = Deck([2, 9, 10, "J", "Q", "K", "A"])
        self.console_interface = ConsoleInterface()

    def play_game(self) -> None:
        while len(self.game_state.get_players().keys()) > 1:
            hand = self.start_hand()
            action = self.console_interface.decide_on_action(hand)
            while type(action) is not Call:
                hand.update_a_bet(action)
                action = self.console_interface.decide_on_action(hand)
            calling_player_id = hand.get_hand_state().get_current_player_id()
            called_player_id = self.get_id_of_called_player(hand, calling_player_id)
            current_bet = hand.get_hand_state().get_current_bet()
            actual_quantity = self.calculate_actual_quantity(
                hand, current_bet.get_card_rank()
            )
            loosing_player_id = (
                calling_player_id
                if actual_quantity >= current_bet.get_quantity()
                else called_player_id
            )
            self.calculate_id_of_next_starting_player()
            loosing_player = self.game_state.get_players().get(loosing_player_id)
            loosing_player.add_one_card()
            player_eliminated = loosing_player.check_if_lost()
            if player_eliminated:
                if loosing_player_id == self.game_state.get_starting_player_id():
                    self.calculate_id_of_next_starting_player()
                self.game_state.get_players().pop(loosing_player_id)

            self.console_interface.print_hand_result(
                hand,
                called_player_id,
                calling_player_id,
                current_bet,
                actual_quantity,
                player_eliminated,
            )
            hand.return_cards(self.deck)
        winner = max(self.game_state.get_players().keys())
        self.console_interface.print_winner(winner)

    def get_id_of_called_player(self, hand: Hand, calling_player_id: int) -> int:
        list_of_ids = list(hand.get_players().keys())
        calling_player_index = list_of_ids.index(calling_player_id)
        called_player_index = (calling_player_index - 1) % len(hand.get_players())
        return list_of_ids[called_player_index]

    def calculate_id_of_next_starting_player(self) -> None:
        id_of_starting_player = self.game_state.get_starting_player_id()
        list_of_ids = list(self.game_state.get_players().keys())
        starting_player_index = list_of_ids.index(id_of_starting_player)
        next_strting_player_index = (starting_player_index + 1) % len(
            self.game_state.get_players()
        )
        self.game_state.set_starting_player_id(list_of_ids[next_strting_player_index])

    def calculate_actual_quantity(self, hand: Hand, card_rank: Rank) -> int:
        actual_quantity = 0
        for player in hand.players.values():
            ranks = map(Card.get_rank, player.get_cards())
            ranks = np.fromiter(ranks, dtype=Rank)
            actual_quantity += sum(ranks == card_rank)
            actual_quantity += sum(ranks == Rank(2))
        return actual_quantity

    def get_name_state(self) -> GameState:
        return self.game_state

    def get_deck(self) -> Deck:
        return self.deck

    def start_hand(self) -> Hand:
        starting_player_id = self.game_state.starting_player_id
        hand = Hand(self.game_state.players, starting_player_id)
        hand.deal_cards(self.deck)
        return hand
