from five_cards.player import Player
from five_cards.bet import Bet
from five_cards.call import Call
from five_cards.hand import Hand
from deck.card import Rank
from os import system


class ConsoleInterface:
    def __init__(self) -> None:
        pass

    def decide_on_action(self, hand: Hand) -> Call | Bet:
        system("cls")
        action = ""
        decision = None
        hand_state = hand.get_hand_state()
        current_bet = hand_state.get_current_bet()
        player = hand.get_current_player()
        print(f"Player {player.get_id()}")
        input("Press enter when ready")
        print("\nYour cards:")
        for card in sorted(player.cards):
            print(card)
        self.print_cards_number(hand)
        print(f"\nCurrent bet: {current_bet}")
        while action != "1" and action != "2":
            if current_bet is None:
                action = "2"
            else:
                action = input(
                    "\nOptions:\n1.Call\n2.Bet\n3.Print betting history\nChoose action: "
                )
            if action == "1":
                decision = Call()
            elif action == "2":
                decision = self.construct_a_bet()
                if not decision > current_bet:
                    print("\nBet too small!")
                    print(f"\nCurrent player: {player.get_id()}")
                    action = ""
            elif action == "3":
                self.print_bet_history(hand)
            else:
                print("\nYou did not choose a correct action!")

        return decision

    def print_bet_history(self, hand: Hand) -> None:
        print("\nBet history:")
        for players_bet in hand.get_hand_state().get_bet_history():
            print(f"Player: {players_bet[0]}, bet: {players_bet[1]}")

    def print_cards_number(self, hand: Hand) -> None:
        print("\nNumber of cards for each player:")
        for cards_number in hand.get_number_of_cards_per_player().items():
            print(f"Player: {cards_number[0]}, number of cards: {cards_number[1]}")

    def construct_a_bet(self) -> Bet:
        user_input = ""
        quantity = 0
        while not user_input.isdigit() or quantity < 1 or quantity > 8:
            user_input = input("\nChoose quantity: [1 - 8]: ")
            if not user_input.isdigit():
                print("\nYou did not enter a number!")
                continue
            quantity = int(user_input)
            if quantity < 1:
                print("\nNumber too low!")
            elif quantity > 8:
                print("\nNumber too high")

        card_rank = ""
        while not card_rank in [9, 10, "J", "Q", "K", "A"]:
            card_rank = input("\nChoose card rank [9, 10, J, Q, K, A]: ")
            if card_rank.isdigit():
                card_rank = int(card_rank)
            if not card_rank in [9, 10, "J", "Q", "K", "A"]:
                print("\nYou did not enter a correct value!")
        return Bet(quantity, Rank(card_rank))

    def print_winner(self, id: int) -> None:
        print(f"\nPlayer {id} is the winner!")

    def print_hand_result(
        self,
        hand: Hand,
        called_player_id: int,
        calling_player_id: int,
        bet: Bet,
        actual_quantity: int,
        player_eliminated: bool,
    ) -> None:
        self.print_all_cards(hand)
        print(f"\nCalled player: {called_player_id}")
        print(f"Calling player: {calling_player_id}")
        print(f"Goal: {bet}")
        print(f"Actual quantity: {actual_quantity}")
        losing_player_id = (
            called_player_id
            if bet.get_quantity() > actual_quantity
            else calling_player_id
        )
        print(f"Player {losing_player_id} lost this hand!")
        if player_eliminated:
            print(f"Player {losing_player_id} is out!")
        input("Press enter to continue")

    def print_all_cards(self, hand: Hand) -> None:
        for player in hand.get_players().values():
            print(f"\nPlayer {player.get_id()}")
            for card in sorted(player.get_cards()):
                print(card)
