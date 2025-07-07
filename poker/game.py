from poker.player import Player
from poker.game_state import GameState
from deck.deck import Deck
import numpy as np
from poker.hand import Hand
from phevaluator.evaluator import evaluate_cards
from collections import Counter



class Game:
    def __init__(self, init_number_of_players: int, init_stack_size: int, deck: Deck=Deck()):
        self.game_state = GameState(np.array([Player(i, init_stack_size) for i in range(init_number_of_players)]), current_dealer = 0)
        self.deck = deck
    
    def __repr__(self) -> str:
        return str(self.game_state)

    def play_hand(self, big_blind: int=2):
        self.deck.reset()
        hand = Hand(self.game_state, self.deck, big_blind)
        hand.deal_cards()
        print(hand.players)
        first_to_act = (self.game_state.current_dealer + 3) % self.game_state.players.size if self.game_state.players.size > 2 else  self.game_state.current_dealer
        winner_id = hand.betting_round(first_to_act)
        if winner_id is not None:
            self.game_state.players[winner_id].stack += hand.pot
        print(np.array2string(hand.flop, separator="; "))
        if hand.active_players - hand.players_all_in > 1:
            winner_id = hand.betting_round((self.game_state.current_dealer + 1) % self.game_state.players.size)
            if winner_id is not None:
                self.game_state.players[winner_id].stack += hand.pot
        print(hand.turn)
        if hand.active_players - hand.players_all_in > 1:
            hand.betting_round((self.game_state.current_dealer + 1) % self.game_state.players.size)
            if winner_id is not None:
                self.game_state.players[winner_id].stack += hand.pot
        print(hand.river)
        if hand.active_players - hand.players_all_in > 1:
            winner_id = hand.betting_round((self.game_state.current_dealer + 1) % self.game_state.players.size)
            if winner_id is not None:
                self.game_state.players[winner_id].stack += hand.pot
            else:
                results = {32767: []}
                for i, winner in enumerate(hand.players):
                    if winner.has_folded:
                        results[32767].append(i)
                    else:
                        cards = np.concatenate((hand.flop, hand.turn, hand.river, winner.cards))
                        evaluation = evaluate_cards(*[card.tag for card in cards])
                        if evaluation in results.keys():
                            results[evaluation].append(i)
                        else:
                            results[evaluation] = [i]
                        
                while hand.pot > 1: #TODO: add one chip to the player closest to the dealer
                    best_hand = min(results.keys())
                    winners_ids = results[best_hand]
                    number_of_winners = len(winners_ids)
                    winnings = 0
                    for winner_id in winners_ids:
                        winner = hand.players[winner_id]
                        winner.stack += winner.current_bet.size
                        hand.pot -= winner.current_bet.size
                        max_win_from_one_player = winner.current_bet.size // number_of_winners
                        print(winner.stack)
                        for i, p in enumerate(hand.players):
                            if i in winners_ids:
                                continue
                            winnings = min(max_win_from_one_player, p.current_bet.size)
                            p.current_bet.size -= winnings
                            hand.pot -= winnings
                            winner.stack += winnings
                    results.pop(best_hand)
        print(hand.flop, hand.turn, hand.river)
        print(self.game_state.players)
        
        