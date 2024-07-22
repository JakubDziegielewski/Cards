from socket import socket, AF_INET, SOCK_STREAM
from five_cards.game import Game
from five_cards.call import Call
from five_cards.bet import Bet
from five_cards.hand import Hand
import numpy as np
from deck.card import Card, Rank, Suit


class Server:
    def __init__(self, number_of_players: int = 3, port_number: int = 10000) -> None:
        self.number_of_players: int = number_of_players
        self.port_number: int = port_number
        self.connections: list[socket] = []

    def start_server(self) -> socket:
        host = "127.0.0.1"
        port = self.port_number
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((host, port))

        print(f"Listening on {(host, port)}")
        return server_socket

    def wait_for_players(self, server_socket: socket) -> None:
        while len(self.connections) < self.number_of_players:
            server_socket.listen(self.number_of_players)
            conn, address = server_socket.accept()  # accept new connection
            print("Connection from: " + str(address))
            self.connections.append(conn)
        for connection in self.connections:
            connection.settimeout(1)

    def start_game(self) -> Game:
        game = Game(self.number_of_players)
        for id, _ in enumerate(self.connections):
            self.send_message_to_a_player(id, f"{id}")

        return game

    def send_message_to_a_player(self, id: int, message: str) -> None:
        response = ""
        while response != b"ACK":
            try:
                self.connections[id].send(message.encode())
                response = self.connections[id].recv(1024)
            except TimeoutError:
                pass

    def receive_a_message(self, id: int) -> bytes:
        data = ""
        while data == "":
            try:
                data = self.connections[id].recv(1024)
            except TimeoutError:
                pass
        self.connections[id].sendall(b"ACK")
        return data

    def send_cards(self, id: int, cards: np.ndarray[Card]) -> None:
        number_of_cards = len(cards)
        self.send_message_to_a_player(id, number_of_cards.__str__())
        message = ""
        for card in cards:
            rank = card.get_rank().value
            if type(rank) is int:
                rank = str(rank)
            suit = card.get_suit().value
            message += rank + " " + suit + " "
        self.send_message_to_a_player(id, message)

    def allow_a_player_to_make_decision(self, id: int) -> None:
        self.send_message_to_a_player(id, "your move")

    def send_number_of_cards(self, hand: Hand) -> None:
        cards_per_player = hand.get_number_of_cards_per_player()
        number_of_players = len(cards_per_player)
        self.send_message_to_all_players(number_of_players.__str__())
        for id in cards_per_player.keys():
            message = f"{id} {cards_per_player[id]}"
            self.send_message_to_all_players(message)

    def send_message_to_all_players(self, message: str) -> None:
        for id in range(self.number_of_players):
            self.send_message_to_a_player(id, message)

    def send_bet_history(self, bet_history: list[tuple[int, Bet]], id: int) -> None:
        number_of_bets = len(bet_history)
        self.send_message_to_a_player(id, number_of_bets.__str__())
        for bet in bet_history:
            message = f"{bet[0]} {bet[1].get_quantity()} {bet[1].get_card_rank().value}"
            self.send_message_to_a_player(id, message)

    def receive_a_bet(self, id: int) -> Bet:
        message = self.receive_a_message(id).decode()
        split_message = message.split(" ")
        rank = split_message[1]
        if rank.isdigit():
            rank = int(rank)
        return Bet(int(split_message[0]), Rank(rank))

    def perform_bet_action(self, hand: Hand, current_player_id: int) -> Bet:
        bet = self.receive_a_bet(current_player_id)
        return bet

    def perform_call_action(self, hand: Hand) -> int:
        calling_player_id = hand.get_hand_state().get_current_player_id()
        called_player_id = hand.get_id_of_called_player(calling_player_id)
        current_bet = hand.get_hand_state().get_current_bet()
        actual_quantity = hand.calculate_actual_quantity(current_bet[1].get_card_rank())
        loosing_player_id = (
            calling_player_id
            if actual_quantity >= current_bet[1].get_quantity()
            else called_player_id
        )
        self.send_message_to_all_players(
            f"Player {called_player_id} got called by Player {calling_player_id}"
        )
        self.send_message_to_all_players(f"Called bet: {current_bet[1].__str__()}")
        self.send_message_to_all_players(f"Actual quantity: {actual_quantity}")
        self.send_message_to_all_players(f"Player {loosing_player_id} lost this hand")

        return loosing_player_id

    def finish_hand(self, game: Game, loosing_player_id: int) -> None:
        game.calculate_id_of_next_starting_player()
        loosing_player = game.get_game_state().get_players()[loosing_player_id]
        loosing_player.add_one_card()
        self.send_message_to_a_player(loosing_player_id, "You lost this hand")
        if loosing_player.check_if_lost():
            if loosing_player_id == game.get_game_state().get_starting_player_id():
                game.calculate_id_of_next_starting_player()
            self.send_message_to_all_players(f"Player {loosing_player_id} is out")
            game.get_game_state().get_players().pop(loosing_player_id)
        self.send_message_to_all_players("Hand is over\n")
        if loosing_player.check_if_lost():
            self.send_message_to_a_player(loosing_player_id, "You are out")

    def send_hand_info_to_current_player(self, hand: Hand) -> None:
        current_player_id = hand.get_hand_state().get_current_player_id()
        self.allow_a_player_to_make_decision(current_player_id)
        bet_history = hand.get_hand_state().get_bet_history()
        self.send_bet_history(bet_history, current_player_id)

    def perform_bet_validation_actions(
        self, hand: Hand, bet: Bet, current_player_id: int
    ) -> None:
        hand.update_a_bet(bet)
        self.send_message_to_a_player(current_player_id, "True")
        self.send_message_to_all_players(
            f"Player {current_player_id} bet {bet.__str__()}"
        )

    def play_hand(self, game: Game) -> None:
        hand = game.start_hand()
        self.send_number_of_cards(hand)
        for id in game.get_game_state().get_players().keys():
            cards = hand.get_players()[id].get_cards()
            self.send_cards(id, cards)
        decision = ""
        while decision != b"call":
            self.send_hand_info_to_current_player(hand)
            current_player_id = hand.get_hand_state().get_current_player_id()
            decision = self.receive_a_message(current_player_id)
            while decision == b"bet":
                bet = self.perform_bet_action(hand, current_player_id)
                bet_validated = hand.get_hand_state().validate_a_bet(bet)
                if bet_validated:
                    self.perform_bet_validation_actions(hand, bet, current_player_id)
                    decision = ""
                else:
                    self.send_message_to_a_player(current_player_id, "False")
                    decision = self.receive_a_message(current_player_id)
        loosing_player_id = self.perform_call_action(hand)
        self.finish_hand(game, loosing_player_id)
        hand.return_cards(game.get_deck())

    def play_game(self, game: Game) -> None:
        while len(game.get_game_state().get_players()) > 1:
            self.send_message_to_all_players("Next hand is starting\n")
            self.play_hand(game)
        self.send_message_to_all_players("Game Over")
        winner = max(game.get_game_state().get_players().keys())
        self.send_message_to_all_players(f"{winner}")

    #        action = game.get_console_interface.decide_on_action(hand)
    #        while type(action) is not Call:
    #            hand.update_a_bet(action)
    #            action = game.console_interface.decide_on_action(hand)
    #        calling_player_id = hand.get_hand_state().get_current_player_id()
    #        called_player_id = game.get_id_of_called_player(hand, calling_player_id)
    #        current_bet = hand.get_hand_state().get_current_bet()
    #        actual_quantity = game.calculate_actual_quantity(
    #            hand, current_bet.get_card_rank()
    #        )
    #        loosing_player_id = (
    #            calling_player_id
    #            if actual_quantity >= current_bet.get_quantity()
    #            else called_player_id
    #        )
    #        game.calculate_id_of_next_starting_player()
    #        loosing_player = game.game_state.get_players().get(loosing_player_id)
    #        loosing_player.add_one_card()
    #        player_eliminated = loosing_player.check_if_lost()
    #        if player_eliminated:
    #            if loosing_player_id == game.game_state.get_starting_player_id():
    #                game.calculate_id_of_next_starting_player()
    #            game.game_state.get_players().pop(loosing_player_id)
    #
    #        self.console_interface.print_hand_result(
    #            hand,
    #            called_player_id,
    #            calling_player_id,
    #            current_bet,
    #            actual_quantity,
    #            player_eliminated,
    #        )
    #        hand.return_cards(self.deck)
    #    winner = max(self.game_state.get_players().keys())
    #    self.console_interface.print_winner(winner)

    def run_server(self) -> None:
        try:
            socket = self.start_server()
            self.wait_for_players(socket)
            game = self.start_game()
            self.play_game(game)
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            socket.close()
            for connection in self.connections:
                connection.close()
