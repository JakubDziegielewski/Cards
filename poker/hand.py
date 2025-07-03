from poker.game_state import GameState
from deck.deck import Deck
from poker.hand_state import HandState
class Hand:
    def __init__(self, init_game_state: GameState, deck: Deck):
        self.game_state = init_game_state
        self.players = self.game_state.players
        self.hand_state = HandState()
        self.deck = deck
        self.pot = 0
    
    def deal_cards(self) -> None:
        self.deck.shuffle()
        for player in self.players:
            cards = self.deck.draw_cards(2)
            player.set_cards(cards)
        dealer = self.game_state.current_dealer
        if self.players.size == 2:
            small_blind = dealer
            big_blind = (dealer + 1) % 2
        else:
            small_blind = (dealer + 1) % self.players.size
            big_blind = (dealer + 2) % self.players.size
        
    