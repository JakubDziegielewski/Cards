from poker.game_state import GameState
from deck.deck import Deck
from poker.hand_state import HandState
from poker.bet import Bet
from poker.call import Call
import numpy as np

class Hand:
    def __init__(self, init_game_state: GameState, deck: Deck, big_blind = 2):
        self.game_state = init_game_state
        self.players = self.game_state.players
        self.acted_in_round = np.zeros(self.players.shape, dtype=bool) #table of booleans indicating if a player acted in the current round of betting
        self.has_folded = np.zeros(self.players.shape, dtype=bool) #table of booleans indicating if a player folded
        self.hand_state = HandState()
        self.deck = deck
        self.pot = 0
        self.big_blind = big_blind
        self.current_bet = Bet(big_blind)
        
    
    def deal_cards(self) -> None:
        self.deck.shuffle()
        for player in self.players:
            cards = self.deck.draw_cards(2)
            player.set_cards(cards)
        dealer = self.game_state.current_dealer
        self.small_blind_player_id, self.big_blind_player_id = self.define_big_and_small_blinds(dealer)
        small_bet = self.players[self.small_blind_player_id].make_a_bet(self.big_blind//2)
        big_bet = self.players[self.big_blind_player_id].make_a_bet(self.big_blind)
        self.pot = small_bet.size + big_bet.size

    def define_big_and_small_blinds(self, dealer):
        if self.players.size == 2:
            small_blind_player_id = dealer
            big_blind_player_id = (dealer + 1) % 2
        else:
            small_blind_player_id = (dealer + 1) % self.players.size
            big_blind_player_id = (dealer + 2) % self.players.size
        return small_blind_player_id, big_blind_player_id

    def betting_round(self):
        current_player_id = (self.big_blind_player_id + 1) % self.players.size
        while not all(self.acted_in_round):
            current_player = self.players[current_player_id]
            current_player_bet_size = current_player.current_bet.size
            decision = current_player.make_decision(self.current_bet, self.players)
            if type(decision) is Bet:
                self.acted_in_round = np.zeros(self.acted_in_round.shape, dtype=bool)
                self.current_bet = decision
            self.acted_in_round[current_player_id] = True
            self.pot += self.current_bet.size - current_player_bet_size
            current_player_id = (current_player_id + 1) % self.players.size
        print(self.pot)
            
        
        
    
    
    