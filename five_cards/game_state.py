from five_cards.player import Player


class GameState:
    def __init__(self, number_of_players: int) -> None:
        self.number_of_players = number_of_players
        self.players = {id: Player(id) for id in range(number_of_players)}
        self.starting_player_id = 0

    def get_players(self) -> dict[int, Player]:
        return self.players

    def get_starting_player_id(self) -> int:
        return self.starting_player_id

    def set_starting_player_id(self, id: int) -> None:
        self.starting_player_id = id
