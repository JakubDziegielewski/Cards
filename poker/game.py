from poker.player import Player
from poker.game_state import GameState
from deck.deck import Deck
import numpy as np
from poker.hand import Hand
from phevaluator.evaluator import evaluate_cards


class Game:
    def __init__(
        self,
        init_number_of_players: int,
        init_stack_size: int,
        big_blind: int,
        deck: Deck = Deck(),
    ):
        self.game_state = GameState(
            np.array(
                [Player(i, init_stack_size) for i in range(init_number_of_players)]
            ),
            current_dealer=0,
        )
        self.big_blind = big_blind
        self.deck = deck

    def __repr__(self) -> str:
        return str(self.game_state)

    def play_hand(self, big_blind: int = 2):
        self.deck.init_deck()
        hand = Hand(self.game_state, self.deck, big_blind)
        hand.deal_cards()
        print(hand.players)
        first_to_act = (
            (self.game_state.current_dealer + 3) % self.game_state.players.size
            if self.game_state.players.size > 2
            else self.game_state.current_dealer
        )

        first_to_act_after_flop = (
            self.game_state.current_dealer + 1
        ) % self.game_state.players.size
        winner_id = None
        if hand.active_players - hand.players_all_in == 1:
            if hand.players.size == 3:
                winner_id = hand.play_betting_round(first_to_act)
                if winner_id is not None:
                    self.finish_game_after_betting(winner_id, hand)
                    return
            elif hand.players[hand.big_blind_player_id].is_all_in and hand.players[hand.big_blind_player_id].current_bet.size > hand.players[hand.small_blind_player_id].current_bet.size:
                winner_id = hand.play_betting_round(first_to_act)
                if winner_id is not None:
                    self.finish_game_after_betting(winner_id, hand)
                    return
        elif hand.active_players - hand.players_all_in > 1:
            winner_id = hand.play_betting_round(first_to_act, self.big_blind)
            if winner_id is not None:
                self.finish_game_after_betting(winner_id, hand)
                return
        elif (hand.active_players - hand.players_all_in == 1 and hand.players[hand.big_blind_player_id].is_all_in):
            winner_id = hand.play_betting_round(first_to_act, self.big_blind)
            if winner_id is not None:
                self.finish_game_after_betting(winner_id, hand)
                return
        hand.hand_state.public_cards = hand.flop
        print(hand.hand_state.public_cards)
        if hand.active_players - hand.players_all_in > 1:
            winner_id = hand.play_betting_round(first_to_act_after_flop, self.big_blind)
            if winner_id is not None:
                self.finish_game_after_betting(winner_id, hand)
                return
        hand.hand_state.public_cards = np.concatenate((hand.hand_state.public_cards, hand.turn))
        print(hand.hand_state.public_cards)
        if hand.active_players - hand.players_all_in > 1:
            hand.play_betting_round(first_to_act_after_flop, self.big_blind * 2)
            if winner_id is not None:
                self.finish_game_after_betting(winner_id, hand)
                return
        hand.hand_state.public_cards = np.concatenate((hand.hand_state.public_cards, hand.river))
        print(hand.hand_state.public_cards)
        if hand.active_players - hand.players_all_in > 1:
            winner_id = hand.play_betting_round(first_to_act_after_flop, self.big_blind * 2)
        if winner_id is not None:
            self.finish_game_after_betting(winner_id, hand)
            return
        else:
            self.define_winners(hand)

    def finish_game_after_betting(self, winner_id: int, hand: Hand) -> None:
        self.game_state.players[winner_id].stack += hand.hand_state.pot
        for player in self.game_state.players:
            player.current_bet.size = 0

    def define_winners(self, hand: Hand) -> None:
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
        self.calculate_earnings(results, hand)

    def calculate_earnings(self, results, hand) -> None:
        while hand.hand_state.pot > 1:  # TODO: add one chip to the player closest to the dealer
            best_hand = min(results.keys())
            winners_ids = results[best_hand]
            number_of_winners = len(winners_ids)
            winnings = 0
            for winner_id in winners_ids:
                winner = hand.players[winner_id]
                winner.stack += winner.current_bet.size
                hand.hand_state.pot -= winner.current_bet.size
                max_win_from_one_player = winner.current_bet.size // number_of_winners
                winner.current_bet.size = 0
                for i, p in enumerate(hand.players):
                    if i in winners_ids:
                        continue
                    winnings = min(max_win_from_one_player, p.current_bet.size)
                    p.current_bet.size -= winnings
                    hand.hand_state.pot -= winnings
                    winner.stack += winnings
            results.pop(best_hand)

    def check_for_eliminated_players(self) -> None:
        eliminated_players = []
        for i, player in enumerate(self.game_state.players):
            if player.stack == 0:
                eliminated_players.append(i)
        self.game_state.players = np.delete(self.game_state.players, eliminated_players)

    def play_game(self) -> int:
        rounds = 0
        while self.game_state.players.size > 1:
            rounds += 1
            self.play_hand(self.big_blind)
            print(self.game_state.players, end="\n\n")
            self.check_for_eliminated_players()
            self.game_state.change_dealer()
            if sum(x.stack for x in self.game_state.players) > 4000:
                exit(1)
        print(f"Rounds: {rounds}")
        return self.game_state.players[0].id
