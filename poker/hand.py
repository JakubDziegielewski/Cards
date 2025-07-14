from poker.game_state import GameState
from deck.deck import Deck
from deck.card import Card, Rank, Suit
from poker.hand_state import HandState
from poker.bet import Bet
from poker.call import Call
from poker.fold import Fold
import numpy as np

class Hand:
    def __init__(self, init_game_state: GameState, deck: Deck, big_blind:int = 2):
        self.game_state = init_game_state
        self.players = self.game_state.players
        self.acted_in_round = np.zeros(self.players.shape, dtype=bool) #table of booleans indicating if a player acted in the current round of betting
        self.has_folded = np.zeros(self.players.shape, dtype=bool) #table of booleans indicating if a player folded
        self.hand_state = HandState()
        self.deck = deck
        self.big_blind = big_blind
        self.dealer = self.game_state.current_dealer
        self.small_blind_player_id, self.big_blind_player_id = self.define_big_and_small_blinds(self.dealer)
        self.active_players = self.players.size
        self.players_all_in = 0
        
    
    def deal_cards(self) -> None:
        self.deck.reset()
        self.deck.shuffle()
        for player in self.players:
            cards = self.deck.draw_cards(2)
            player.set_cards(cards)
            player.has_folded = False
            player.is_all_in = False
        self.flop = self.deck.draw_cards(3)
        if self.flop.size < 3:
            print("here")
        self.turn = self.deck.draw_cards(1)
        self.river = self.deck.draw_cards(1)
        #self.players[0].cards = np.array([Card(Rank(6), Suit("diamond")), Card(Rank("T"), Suit("diamond"))])
        #self.players[1].cards = np.array([Card(Rank("K"), Suit("diamond")), Card(Rank("T"), Suit("heart"))])
        #self.players[2].cards = np.array([Card(Rank("Q"), Suit("spade")), Card(Rank(2), Suit("heart"))])
        #self.flop = np.array([Card(Rank(5), Suit("heart")), Card(Rank(2), Suit("diamond")), Card(Rank("Q"), Suit("heart"))])
        #self.turn = np.array([Card(Rank("J"), Suit("diamond"))])
        #self.river = np.array([Card(Rank(4), Suit("club"))])
        small_bet = self.players[self.small_blind_player_id].make_a_bet(self.big_blind//2)
        if self.players[self.small_blind_player_id].is_all_in:
            self.players_all_in += 1
        big_bet = self.players[self.big_blind_player_id].make_a_bet(self.big_blind)
        if self.players[self.big_blind_player_id].is_all_in:
            self.players_all_in += 1
        self.hand_state.pot = small_bet.size + big_bet.size
        self.hand_state.current_bet = Bet(self.big_blind)

    def define_big_and_small_blinds(self, dealer):
        if self.players.size == 2:
            small_blind_player_id = dealer
            big_blind_player_id = (dealer + 1) % 2
        else:
            small_blind_player_id = (dealer + 1) % self.players.size
            big_blind_player_id = (dealer + 2) % self.players.size
        return small_blind_player_id, big_blind_player_id

    def play_betting_round(self, current_player_id, bet_size) -> int | None:
        self.acted_in_round = np.zeros(self.acted_in_round.shape, dtype=bool)
        #current_player_id = (self.big_blind_player_id + 1) % self.players.size
        number_of_bets = 0
        while not all(self.acted_in_round) and self.active_players > 1:
            current_player = self.players[current_player_id]
            if current_player.has_folded or current_player.is_all_in:
                self.acted_in_round[current_player_id] = True
                current_player_id = (current_player_id + 1) % self.players.size
                continue
            print(f"Current player: {current_player.id}")
            
            current_player_bet_size = current_player.current_bet.size
            decision = current_player.make_decision(self.hand_state, bet_size=bet_size, number_of_bets=number_of_bets)
            print(type(decision))
            if type(decision) is Fold:
                self.acted_in_round[current_player_id] = True
                self.active_players -= 1
                if self.active_players == 1:
                    index = [i for i, player in enumerate(self.players) if not player.has_folded][0]
                    return index
            elif type(decision) is Bet:
                number_of_bets += 1
                self.acted_in_round = np.zeros(self.acted_in_round.shape, dtype=bool)
                self.hand_state.current_bet = decision
                self.acted_in_round[current_player_id] = True
                self.hand_state.pot += self.hand_state.current_bet.size - current_player_bet_size
                if current_player.is_all_in:
                    self.players_all_in += 1
            elif type(decision) is Call:
                self.acted_in_round[current_player_id] = True
                self.hand_state.pot += decision.size - current_player_bet_size
                if current_player.is_all_in:
                    self.players_all_in += 1
            else:
                self.acted_in_round[current_player_id] = True
            current_player_id = (current_player_id + 1) % self.players.size
    
    
        
        
    
    
    