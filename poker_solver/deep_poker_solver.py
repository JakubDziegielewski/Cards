from deck.deck import Deck
from poker_solver.card_embedding import CardEmbedding
from poker_solver.deep_cfr_model import DeepCFRModel
from poker_solver.advantage_memory import AdvantageMemory
from poker_solver.strategy_memory import StrategyMemory
from poker_solver.game_environment import GameEnvironment
import torch
import torch.nn as nn
from functools import cache


class DeepPokerSolver:
    def __init__(self, ncardtypes, nbets, nactions, num_players=2, max_advantage_memory = 40_000_000, max_strategy_memory = 40_000_000, batch_size = 4_000):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.advantage_nets = [
            DeepCFRModel(ncardtypes=ncardtypes, nbets=nbets, nactions=nactions).to(
                self.device
            )
            for _ in range(num_players)
        ]
        for advantage_net in self.advantage_nets:
            nn.init.zeros_(advantage_net.action_head.weight)
            nn.init.zeros_(advantage_net.action_head.bias)
        self.strategy_net = DeepCFRModel(ncardtypes=ncardtypes, nbets=nbets, nactions=nactions).to(self.device)
        self.advantage_memories = [AdvantageMemory(max_advantage_memory) for _ in range(num_players)]
        self.strategy_memory = StrategyMemory(max_strategy_memory)
        self.batch_size = batch_size
        self.deck = Deck()
    
    def traverse(self, game_environment: GameEnvironment, betting_sequence:tuple, player:int):
        if DeepPokerSolver.betting_sequence_ends_hand(betting_sequence):
            return DeepPokerSolver.find_result(game_environment, betting_sequence)
        elif DeepPokerSolver.betting_sequence_ends_round(betting_sequence):
             betting_sequence = betting_sequence + ("",)
             return self.traverse(game_environment, betting_sequence, player)
        elif len(betting_sequence[-1]) % 2 != player:
            legal_actions = self.define_legal_actions(betting_sequence[-1])
            net = self.advantage_nets[player]
            round = len(betting_sequence) - 1
            input_card_tensor = game_environment.card_tensors[player][round]
            print(legal_actions)
            print(input_card_tensor)
            bet_tensor = DeepPokerSolver.betting_sequence_to_tensor(betting_sequence)
            print(bet_tensor)
            with torch.no_grad():
                outputs = net(input_card_tensor, DeepPokerSolver.betting_sequence_to_tensor(betting_sequence))
            print(outputs)
            with torch.no_grad():
                pass
    
    @staticmethod
    @cache
    def betting_sequence_to_tensor(betting_sequence: tuple) -> torch.tensor:
        result_tensor = -torch.ones((4, 6))
        for i, betting_round in enumerate(betting_sequence):
            value = 2 if i < 2 else 4
            result_tensor[i] = DeepPokerSolver.betting_round_to_ints(betting_round, value)
        return result_tensor.reshape((1, -1))
   
    @staticmethod
    @cache
    def betting_round_to_ints(betting_round: str, value: int) -> list:
        result_list = [-1] * 6
        for i, action in enumerate(betting_round):
            result_list[i] = value if action == "B" else 0
        return torch.tensor(result_list)
    
    
    def define_legal_actions(self, betting_sequence: str) -> tuple:
        if betting_sequence in ("", "P", "BC"):
            return ("F", "P", "B")
        elif betting_sequence[-1].count("B") < 4:
            return ("F", "C", "B")
        else:
            return ("F", "C")
        
    def regret_matching(self, regrets) -> torch.Tensor:
        positive_regrets = torch.where(regrets > 0)
        if len(positive_regrets[0]) == 0:
            return torch.ones(regrets.shape) / regrets.shape
        positive_regrets_sum = torch.sum(regrets[positive_regrets])
        strategy = torch.zeros(regrets.shape)
        strategy[positive_regrets] += regrets[positive_regrets] / positive_regrets_sum
        return strategy
    
    @staticmethod
    def find_result(game_environment: GameEnvironment, betting_sequence:tuple) -> int:
        reward = DeepPokerSolver.calculate_reward(betting_sequence)
        if betting_sequence[-1][-1] == "F":
            if len(betting_sequence[-1]) % 2 == 1:
                return reward
            else:
                return -reward
        else:
            if game_environment.small_blind_strength < game_environment.big_blind_strength:
                return reward
            elif game_environment.small_blind_strength > game_environment.big_blind_strength:
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
    
    @staticmethod
    @cache
    def betting_sequence_ends_round(betting_sequence) -> bool:
        if betting_sequence[-1] == "":
            return False
        if len(betting_sequence) > 1:
            return (
                betting_sequence[-1][-1] in ["C", "F"]
                or betting_sequence[-1][-2:] == "PP"
            )
        else:
            return betting_sequence[-1][-1] in ["P", "F"] or (
                betting_sequence[-1][-1] == "C"
                and len(betting_sequence[-1]) > 2
            )
    
    @staticmethod
    @cache
    def betting_sequence_ends_hand(betting_sequence: tuple) -> bool:
        if betting_sequence[-1] == "":
            return False
        return betting_sequence[-1][-1] == "F" or (
            len(betting_sequence) == 4 and DeepPokerSolver.betting_sequence_ends_round(betting_sequence)
        )
        
    
    