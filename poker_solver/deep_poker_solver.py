from deck.deck import Deck
from poker_solver.deep_cfr_model import DeepCFRModel
from poker_solver.deep_strategy_model import DeepStrategyModel
from poker_solver.advantage_memory import AdvantageMemory
from poker_solver.strategy_memory import StrategyMemory
from poker_solver.game_environment import GameEnvironment
from poker_solver.card_embedding import CardEmbedding
import torch
import torch.nn as nn
from functools import cache
from time import time


class DeepPokerSolver:
    def __init__(
        self,
        ncardtypes,
        nbets,
        nactions,
        num_players=2,
        dim=64,
        max_advantage_memory=40_000_000,
        max_strategy_memory=40_000_000,
        batch_size=10_000,
        traversals: int = 10_000,
        network_training_iterations: int = 32_000,
    ):
        self.card_embeddings = nn.ModuleList(
            [CardEmbedding(dim) for _ in range(ncardtypes)]
        )
        self.advantage_nets = [
            DeepCFRModel(
                ncardtypes=ncardtypes,
                nbets=nbets,
                nactions=nactions,
                card_embeddings=self.card_embeddings,
            )
            for _ in range(num_players)
        ]
        if torch.cuda.is_available():
            self.device = "cuda"
            for net in self.advantage_nets:
                net.cuda()
        else:
            self.device = "cpu"
        self.strategy_net = (
            DeepStrategyModel(
                ncardtypes=ncardtypes,
                nbets=nbets,
                nactions=nactions,
                card_embeddings=self.card_embeddings,
            ).cuda()
            if self.device == "cuda"
            else DeepStrategyModel(
                ncardtypes=ncardtypes,
                nbets=nbets,
                nactions=nactions,
                card_embeddings=self.card_embeddings,
            )
        )
        self.advantage_memories = [
            AdvantageMemory(max_advantage_memory) for _ in range(num_players)
        ]
        self.strategy_memory = StrategyMemory(max_strategy_memory)
        self.batch_size = batch_size
        self.traversals = traversals
        self.network_training_iterations = network_training_iterations
        self.deck = Deck()

    def traverse(
        self,
        game_environment: GameEnvironment,
        betting_sequence: tuple,
        player: int,
        iteration: int,
    ):
        if DeepPokerSolver.betting_sequence_ends_hand(betting_sequence):
            return DeepPokerSolver.find_result(game_environment, betting_sequence)
        elif DeepPokerSolver.betting_sequence_ends_round(betting_sequence):
            betting_sequence = betting_sequence + ("",)
            return self.traverse(game_environment, betting_sequence, player, iteration)
        elif len(betting_sequence[-1]) % 2 != player:
            legal_actions = self.define_legal_actions(betting_sequence[-1])
            net = self.advantage_nets[player]
            round = len(betting_sequence) - 1
            input_card_tensor = game_environment.card_tensors[player][round].to(
                self.device
            )
            bet_tensor = DeepPokerSolver.betting_sequence_to_tensor(
                betting_sequence
            ).to(self.device)
            with torch.no_grad():
                outputs = net(input_card_tensor, bet_tensor).squeeze(0)
            action_counterfactual_values = torch.zeros(3, device=self.device)
            if len(legal_actions) == 2:
                strategy = torch.zeros(3, device=self.device)
                strategy[:-1] = self.regret_matching(outputs[:-1])
                action_counterfactual_values[-1] = -4_294_967_296
                # action_counterfactual_values[-1] = -float("inf")
            else:
                strategy = self.regret_matching(outputs)
            for i, action in enumerate(legal_actions):
                last_sequence = betting_sequence[-1] + action
                new_sequence = betting_sequence[:-1] + (last_sequence,)
                action_counterfactual_values[i] = self.traverse(
                    game_environment, new_sequence, player, iteration
                )
            node_value = (strategy * action_counterfactual_values).sum()
            sampled_advantages = action_counterfactual_values - node_value
            if player == 1:  # minimizing player
                sampled_advantages = -sampled_advantages
            self.advantage_memories[player].add(
                input_card_tensor, bet_tensor, sampled_advantages
            )
            return node_value
        else:
            current_player = 1 - player
            legal_actions = self.define_legal_actions(betting_sequence[-1])
            net = self.advantage_nets[current_player]
            round = len(betting_sequence) - 1
            input_card_tensor = game_environment.card_tensors[current_player][round].to(
                self.device
            )
            bet_tensor = DeepPokerSolver.betting_sequence_to_tensor(
                betting_sequence
            ).to(self.device)
            with torch.no_grad():
                outputs = net(input_card_tensor, bet_tensor).squeeze(0)
            if len(legal_actions) == 2:
                strategy = torch.zeros(3, device=self.device)
                strategy[:-1] = self.regret_matching(outputs[:-1])
            else:
                strategy = self.regret_matching(outputs)
            self.strategy_memory.add(input_card_tensor, bet_tensor, strategy)
            action = legal_actions[strategy.multinomial(1)]
            last_sequence = betting_sequence[-1] + action
            new_sequence = betting_sequence[:-1] + (last_sequence,)
            return self.traverse(game_environment, new_sequence, player, iteration)

    def deep_counterfactual_regret_minimization(
        self,
        iterations: int
    ):
        game_environment = GameEnvironment(2)
        for iteration in range(iterations):
            for player in (0, 1):
                start = time()
                for _ in range(self.traversals):
                    game_environment.deal_cards()
                    self.traverse(game_environment, ("B",), player, iteration)
                    game_environment.return_cards()
                end = time()
                print(f"Traversals time: {end - start}")
            for player in (0, 1):
                self.advantage_nets[player].reset_weights()
                start = time()
                for _ in range(self.network_training_iterations):
                    self.train_advantage_net(
                        player,
                        torch.optim.Adam(
                            self.advantage_nets[player].parameters(), lr=1e-4
                        ),
                    )
                end = time()
                print(f"Advantage network training time: {end - start}")
            start = time()
            for _ in range(self.network_training_iterations):
                self.train_strategy_net(
                    torch.optim.Adam(self.strategy_net.parameters(), lr=1e-4)
                )
            end = time()
            print(f"Strategy network training time: {end - start}")

    def train_advantage_net(self, player, optimizer, loss_fn=nn.MSELoss()):
        memory = self.advantage_memories[player]
        net = self.advantage_nets[player]
        if len(memory) < self.batch_size:
            print(f"Advantage memory len: {len(memory)}")
            return
        batch = memory.sample(self.batch_size)
        cards_tensors, bet_tensors, advantages = zip(*batch)

        cards_tensors = (
            torch.stack(cards_tensors).reshape(self.batch_size, -1).to(self.device)
        )
        bet_tensors = (
            torch.stack(bet_tensors).reshape((self.batch_size, -1)).to(self.device)
        )
        advantages = (
            torch.stack(advantages).reshape((self.batch_size, -1)).to(self.device)
        )
        preds = net(cards_tensors, bet_tensors)
        loss = loss_fn(preds, advantages)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    def train_strategy_net(
        self, optimizer, loss_fn=nn.KLDivLoss(reduction="batchmean")
    ):
        memory = self.strategy_memory
        net = self.strategy_net
        if len(memory) < self.batch_size:
            print(f"Strategy memory len: {len(memory)}")
            return
        batch = memory.sample(self.batch_size)
        cards_tensors, bet_tensors, strategies = zip(*batch)
        cards_tensors = torch.stack(cards_tensors).reshape(self.batch_size, -1)
        bet_tensors = torch.stack(bet_tensors).reshape((self.batch_size, -1))
        strategies = torch.stack(strategies).reshape((self.batch_size, -1))
        preds = net(cards_tensors, bet_tensors)
        loss = loss_fn(preds, strategies)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    @staticmethod
    @cache
    def betting_sequence_to_tensor(betting_sequence: tuple) -> torch.Tensor:
        result_tensor = -torch.ones((4, 6))
        for i, betting_round in enumerate(betting_sequence):
            value = 2 if i < 2 else 4
            result_tensor[i] = DeepPokerSolver.betting_round_to_ints(
                betting_round, value
            )
        return result_tensor.reshape((1, -1))

    @staticmethod
    @cache
    def betting_round_to_ints(betting_round: str, value: int) -> list:
        result_list = [-1] * 6
        for i, action in enumerate(betting_round):
            if i > 5:
                pass
            result_list[i] = value if action == "B" else 0
        return torch.tensor(result_list)

    def define_legal_actions(self, betting_round: str) -> tuple:
        if betting_round in ("", "P", "BC"):
            return ("F", "P", "B")
        elif betting_round.count("B") < 4:
            return ("F", "C", "B")
        else:
            return ("F", "C")

    def regret_matching(self, regrets) -> torch.Tensor:
        positive_regrets = torch.where(regrets > 0)
        if len(positive_regrets[0]) == 0:
            return (
                torch.ones(regrets.shape, device=self.device, dtype=torch.float)
                / regrets.shape[0]
            )
        positive_regrets_sum = torch.sum(regrets[positive_regrets])
        strategy = torch.zeros(regrets.shape, device=self.device, dtype=torch.float)
        strategy[positive_regrets] += regrets[positive_regrets] / positive_regrets_sum
        return strategy

    @staticmethod
    def find_result(game_environment: GameEnvironment, betting_sequence: tuple) -> int:
        reward = DeepPokerSolver.calculate_reward(betting_sequence)
        if betting_sequence[-1][-1] == "F":
            if len(betting_sequence[-1]) % 2 == 1:
                return reward
            else:
                return -reward
        else:
            if (
                game_environment.small_blind_strength
                < game_environment.big_blind_strength
            ):
                return reward
            elif (
                game_environment.small_blind_strength
                > game_environment.big_blind_strength
            ):
                return -reward
            else:
                return 0

    @cache
    @staticmethod
    def calculate_reward(betting_sequence: tuple):
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
                betting_sequence[-1][-1] == "C" and len(betting_sequence[-1]) > 2
            )

    @staticmethod
    @cache
    def betting_sequence_ends_hand(betting_sequence: tuple) -> bool:
        if betting_sequence[-1] == "":
            return False
        return betting_sequence[-1][-1] == "F" or (
            len(betting_sequence) == 4
            and DeepPokerSolver.betting_sequence_ends_round(betting_sequence)
        )
