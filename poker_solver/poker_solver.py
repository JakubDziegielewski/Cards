from deck.deck import Deck
from deck.card import Card, Rank, Suit
import json
from poker_solver.hand_translator import HandTranslator
from poker_solver.sequence_generator import SequenceGenerator
from poker_solver.node import Node
from poker_solver.node_group import NodeGroup
import numpy as np
from phevaluator.evaluator import evaluate_cards
from functools import cache

class PokerSolver:
    def __init__(self, buckets:int) -> None:
        self.buckets = buckets
        self.node_groups = {}
        self.hand_translator = HandTranslator()
        with open("poker/ehs/normalized/preflop_ehs_normal.json", "r") as f:
            self.preflop_strengths = json.load(f) 
        with open("poker/ehs/normalized/postflop_ehs_normal.json", "r") as f:
            self.flop_strengths = json.load(f) 
        with open("poker/ehs/normalized/postturn_ehs_normal.json", "r") as f:
            self.turn_strengths = json.load(f) 
        with open("poker/ehs/normalized/postriver_ehs_normal.json", "r") as f:
            self.river_strengths = json.load(f)
        self.deck = Deck()
        sequence_generator = SequenceGenerator()
        for sequence in sequence_generator.get_all_sequences():
            self.node_groups[sequence.betting_sequence] = NodeGroup(sequence, buckets)
    
    
    def find_result(self, betting_sequence:tuple) -> int:
        reward = PokerSolver.calculate_reward(betting_sequence)
        if betting_sequence[-1][-1] == "F":
            if len(betting_sequence[-1]) % 2 == 1:
                return reward
            else:
                return -reward
        else:
            if self.small_blind_strength < self.big_blind_strength:
                return reward
            elif self.small_blind_strength > self.big_blind_strength:
                return -reward
            else:
                return 0
    
    @cache
    @staticmethod
    def calculate_reward(betting_sequence:tuple):
        if betting_sequence[0] == "BF":
            return 1
        if betting_sequence[0] == "BCF":
            return 2
        reward = 0
        for i, sequence in enumerate(betting_sequence):
            multiplier = 1 if i < 2 else 2
            result = sequence.count("B") * 2
            if sequence[-1] == "F":
                result -= 2
            reward += max(0, result * multiplier)
        return reward
    
    
    def counterfactual_regret_minimization(self, betting_sequence:tuple, small_blind_player_turn:bool, pi_one:float, pi_two:float)->float:
        node_group = self.node_groups[betting_sequence]
        if node_group.ends_hand:
            return self.find_result(betting_sequence)
        elif node_group.ends_round:
            betting_sequence = betting_sequence + ("",)
            return self.counterfactual_regret_minimization(betting_sequence, False, pi_one, pi_two)
        phase = len(betting_sequence) - 1
        bucket_number = self.small_blind_cards_buckets[phase] if small_blind_player_turn else self.big_blind_cards_buckets[phase]
        node = self.node_groups[betting_sequence][bucket_number]
        node.visited += 1
        counterfactual_value = 0
        strategy = self.regret_matching(node)
        if betting_sequence[-1] in ("", "P", "BC"):
            actions = ("F", "P", "B")
        elif node.num_actions == 3:
            actions = ("F", "C", "B")
        else:
            actions = ("F", "C")
        action_counterfactual_values = np.zeros(len(actions))
        for i, action in enumerate(actions):
            last_sequence = betting_sequence[-1] + action
            new_sequence = betting_sequence[:-1] + (last_sequence,)
            if small_blind_player_turn:
                action_counterfactual_values[i] = self.counterfactual_regret_minimization(new_sequence, not small_blind_player_turn, strategy[i] * pi_one, pi_two)
            else:
                action_counterfactual_values[i] = self.counterfactual_regret_minimization(new_sequence, not small_blind_player_turn, pi_one, strategy[i] * pi_two)
            counterfactual_value += strategy[i] * action_counterfactual_values[i]
        if small_blind_player_turn:
            regret_reach = pi_two
            strategy_reach = pi_one
            for i, action in enumerate(actions):
                node.regret_sum[i] += regret_reach * (action_counterfactual_values[i] - counterfactual_value)
                node.strategy_sum[i] += strategy_reach * strategy[i]
        else:
            regret_reach = pi_one
            strategy_reach = pi_two
            for i, action in enumerate(actions):
                node.regret_sum[i] -= regret_reach * (action_counterfactual_values[i] - counterfactual_value)
                node.strategy_sum[i] += strategy_reach * strategy[i]
        return counterfactual_value

    
    def train_solver(self, iterations: int) -> None:
        for i in range(iterations):
            self._deal_cards()
            self.counterfactual_regret_minimization(("B",), True, 1, 1)
            self._return_cards()
            if ((i + 1) % 10000) == 0:
                print(i)
    
    def find_bucket_number(self, phase: int, cards: np.ndarray) -> int:
        if phase == 0:
            cards_string = self.hand_translator.get_starting_hand_string(cards)
            cards_strenght = self.preflop_strengths[cards_string]
        elif phase == 1:
            cards_string = self.hand_translator.get_flop_string(cards, self.flop)
            cards_strenght = self.flop_strengths[cards_string]
        elif phase == 2:
            cards_string = self.hand_translator.get_turn_string(cards, self.flop, self.turn)
            cards_strenght = self.turn_strengths[cards_string]
        else:
            cards_string = self.hand_translator.get_river_string(cards, self.flop, self.turn, self.river)
            cards_strenght = self.river_strengths[cards_string]
        bucket_number = min(int(cards_strenght * self.buckets), self.buckets - 1)
        return bucket_number
        

    
    def regret_matching(self, node) -> np.ndarray:
        positive_regrets = np.where(node.regret_sum > 0)
        if len(positive_regrets[0]) == 0:
            return np.ones(node.regret_sum.shape) / node.regret_sum.shape
        positive_regrets_sum = np.sum(node.regret_sum[positive_regrets])
        strategy = np.zeros(node.regret_sum.shape)
        strategy[positive_regrets] += node.regret_sum[positive_regrets] / positive_regrets_sum
        return strategy
        
            
    def _deal_cards(self) -> None:
        self.deck.shuffle()
        self.small_blind_cards = self.deck.draw_cards(2)
        self.big_blind_cards = self.deck.draw_cards(2)
        self.flop = self.deck.draw_cards(3)
        self.turn = self.deck.draw_cards(1)
        self.river = self.deck.draw_cards(1)
        self.small_blind_cards_buckets = [self.find_bucket_number(phase, self.small_blind_cards) for phase in range(4)]
        self.big_blind_cards_buckets = [self.find_bucket_number(phase, self.big_blind_cards) for phase in range(4)]
        self.small_blind_strength = evaluate_cards(*[card.get_tag() for card in np.concatenate((self.small_blind_cards, self.flop, self.turn, self.river))])
        self.big_blind_strength = evaluate_cards(*[card.get_tag() for card in np.concatenate((self.big_blind_cards, self.flop, self.turn, self.river))])
    
    def _return_cards(self) -> None:
        self.deck.return_cards(self.small_blind_cards)
        self.deck.return_cards(self.big_blind_cards)
        self.deck.return_cards(self.flop)
        self.deck.return_cards(self.turn)
        self.deck.return_cards(self.river)