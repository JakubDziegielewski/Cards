from deck.deck import Deck
from phevaluator.evaluator import evaluate_cards
import numpy as np
import torch


class GameEnvironment:
    def __init__(self, players_number=2):
        self.deck = Deck()
        self.players_number = players_number
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def deal_cards(self) -> None:
        self.deck.shuffle()
        self.small_blind_player_cards = self.deck.draw_cards(2)
        self.big_blind_player_cards = self.deck.draw_cards(2)
        self.flop = self.deck.draw_cards(3)
        self.turn = self.deck.draw_cards(1)
        self.river = self.deck.draw_cards(1)
        self.small_blind_strength = evaluate_cards(
            *[
                card.get_tag()
                for card in np.concatenate(
                    (self.small_blind_player_cards, self.flop, self.turn, self.river)
                )
            ]
        )
        self.big_blind_strength = evaluate_cards(
            *[
                card.get_tag()
                for card in np.concatenate(
                    (self.big_blind_player_cards, self.flop, self.turn, self.river)
                )
            ]
        )

        self.cards_numbers_small_blind_player = torch.tensor(
            [card.get_card_number() for card in self.small_blind_player_cards],
            device=self.device,
        )
        self.cards_numbers_big_blind_player = torch.tensor(
            [card.get_card_number() for card in self.big_blind_player_cards],
            device=self.device,
        )
        self.cards_numbers_flop = torch.tensor(
            [card.get_card_number() for card in self.flop], device=self.device
        )
        self.cards_numbers_turn_and_river = torch.tensor([
            self.turn[0].get_card_number(),
            self.river[0].get_card_number(),
        ], device=self.device)

        self.card_tensors = [
            [
                torch.cat((self.cards_numbers_small_blind_player, torch.tensor([-1, -1, -1, -1, -1]))).reshape((1, 7)),
                torch.cat((self.cards_numbers_small_blind_player, self.cards_numbers_flop, torch.tensor([-1, -1]))).reshape((1, 7)),
                torch.cat((self.cards_numbers_small_blind_player, self.cards_numbers_flop, self.cards_numbers_turn_and_river[0:1], torch.tensor([-1]))).reshape((1, 7)),
                torch.cat((self.cards_numbers_small_blind_player, self.cards_numbers_flop, self.cards_numbers_turn_and_river)).reshape((1, 7))
            ],
            [
                torch.cat((self.cards_numbers_big_blind_player, torch.tensor([-1, -1, -1, -1, -1]))).reshape((1, 7)),
                torch.cat((self.cards_numbers_big_blind_player, self.cards_numbers_flop, torch.tensor([-1, -1]))).reshape((1, 7)),
                torch.cat((self.cards_numbers_big_blind_player, self.cards_numbers_flop, self.cards_numbers_turn_and_river[0:1], torch.tensor([-1]))).reshape((1, 7)),
                torch.cat((self.cards_numbers_big_blind_player, self.cards_numbers_flop, self.cards_numbers_turn_and_river)).reshape((1, 7))
            ]
        ]

    def return_cards(self) -> None:
        self.deck.return_cards(self.small_blind_player_cards)
        self.deck.return_cards(self.big_blind_player_cards)
        self.deck.return_cards(self.flop)
        self.deck.return_cards(self.turn)
        self.deck.return_cards(self.river)
