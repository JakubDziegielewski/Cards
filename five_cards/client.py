from socket import socket, AF_INET, SOCK_STREAM
import numpy as np
from deck.card import Card, Rank, Suit
from five_cards.bet import Bet
from five_cards.player import Player


class Client:
    def __init__(self, server_port: int = 10000) -> None:
        self.server_port = server_port
        self.socket = None
        self.id = None

    def connect_to_server(
        self,
    ) -> None:
        host = "127.0.0.1"
        port = self.server_port
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((host, port))
        self.socket = client_socket
        self.socket.settimeout(1)

    def receive_a_message(self, number_of_bytes: int = 1024) -> bytes:
        data = ""
        while data == "":
            try:
                data = self.socket.recv(number_of_bytes)
            except TimeoutError:
                print("Still waiting for the message")
        self.socket.sendall(b"ACK")
        return data

    def send_a_message(self, message: str) -> None:
        response = ""
        while response != b"ACK":
            try:
                self.socket.sendall(message.encode())
                response = self.socket.recv(1024)
            except TimeoutError:
                print("Still waiting for ack")

    def receive_cards(self) -> np.ndarray[Card]:
        data = self.receive_a_message(1).decode()
        number_of_cards = int(data)
        cards = np.zeros(number_of_cards, dtype=Card)
        message = self.receive_a_message().decode().strip().split(" ")
        for i in range(number_of_cards):
            rank = message[2 * i]
            if rank.isdigit():
                rank = int(rank)
            suit = message[2 * i + 1]
            cards[i] = Card(Rank(rank), Suit(suit))
        return cards

    def receive_cards_per_player_info(self) -> dict[int, Player]:
        number_of_players = int(self.receive_a_message(1).decode())
        cards_per_player = {}
        for _ in range(number_of_players):
            message = self.receive_a_message().decode()
            split_message = message.split(" ")
            cards_per_player[int(split_message[0])] = int(split_message[1])
        return cards_per_player

    def receive_current_bet_history(self) -> list[(int, Bet)]:
        number_of_bets = int(self.receive_a_message(1).decode())

        if number_of_bets == 0:
            return []
        bet_history = []
        for _ in range(number_of_bets):
            message = self.receive_a_message().decode()
            split_message = message.split(" ")
            rank = split_message[2]
            if rank.isdigit():
                rank = int(rank)
            bet_history.append(
                (
                    int(split_message[0]),
                    Bet(int(split_message[1]), Rank(rank)),
                )
            )
        return bet_history
    
    def choose_your_action(self) -> int:
        while action != "1" and action != "2":
            action = input(
                "\nOptions:\n1. Call\n2. Bet\nChoose action: "
            )
            if action != "1" and action != "2":
                print("\nYou did not choose a correct action!")
        return int(action)

    def construct_a_bet(self) -> Bet:
        print("Construct your bet!")
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

    def send_a_bet(self, bet: Bet) -> None:
        message = f"{bet.get_quantity()} {bet.get_card_rank().value}"
        self.send_a_message(message)
        
    def play_a_hand(self) -> None:
        print("Next hand is starting\n")
        print(f"You are: Player {self.id}")
        cards_per_player = self.receive_cards_per_player_info()
        for id in cards_per_player.keys():
            print(f"Player {id} has {cards_per_player[id]} cards")
        cards = self.receive_cards()
        print("\nYour cards:")
        for card in cards:
            print(card)
        message = ""
        while message != b"Hand is over":
            message = self.receive_a_message()
            if message == b"your move":
                bet_history = self.receive_current_bet_history()
                action = 0
                if len(bet_history) == 0:
                    print("You have to make the first bet")
                    action = 2
                else:
                    for bet in bet_history:
                        print(f"Player {bet[0]}; {bet.__str__()}")
                    action = self.choose_your_action()
                if action == 1:
                    pass #RETURN CALL
                else:
                    bet = self.construct_a_bet()
                    self.send_a_bet(bet)
            else:
                print(message.decode())
        


    def run_client(self) -> None:
        self.connect_to_server()
        data = self.receive_a_message().decode()  # Get your id number
        self.id = int(data)
        self.play_a_hand()
