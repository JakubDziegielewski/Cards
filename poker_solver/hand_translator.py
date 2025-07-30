from deck.deck import Deck
from deck.card import Card, Suit
import numpy as np
from itertools import permutations
from collections import Counter

class HandTranslator:
    def __init__(self):
        self.starting_hands_translator = self._create_starting_hands_translation_dict()
    
    def _create_starting_hands_translation_dict(self):
        translation_dict = {}
        deck = Deck()
        for starting_hand in permutations(deck.cards, 2):
            key = tuple(starting_hand)
            value = self._translate_starting_hand_to_string(starting_hand)
            translation_dict[key] = value
        return translation_dict
        
    def _translate_starting_hand_to_string(self, cards: np.ndarray) -> str:
        sorted_hand = self._sort_cards(cards)
        suited = "s" if sorted_hand[0].suit == sorted_hand[1].suit else "o" 
        return "".join([str(x.rank.value) for x in sorted_hand]) + suited
    
    def _translate_board_to_string(self, board: np.ndarray) -> str:
        sorted_hand = self._sort_cards(board)
        return "".join([str(x.rank.value) for x in sorted_hand])

    def _sort_cards(self, cards: np.ndarray) -> np.ndarray:
        return np.array(sorted(cards, reverse=True, key=lambda x: (x.get_rank(), x.get_tag())), dtype=Card)
    
    def get_starting_hand_string(self, cards: np.ndarray) -> str:
        return(self.starting_hands_translator[tuple(cards)])
    
    def get_flop_string(self, starting_hand: np.ndarray, flop: np.ndarray) -> str:
        starting_hand_string = self.get_starting_hand_string(starting_hand)
        board_string = self._translate_board_to_string(flop)
        flop_suits = [card.get_suit() for card in flop]
        all_suits = [card.get_suit() for card in np.concatenate((starting_hand, flop))]
        flop_suits_counter = Counter(flop_suits)
        all_suits_coutner = Counter(all_suits)
        if flop_suits_counter.most_common(1)[0][1] == 3:
            flop_type = "_mono_"
            if all_suits_coutner.most_common(1)[0][1] == 5:
                flush = "f"
            elif all_suits_coutner.most_common(1)[0][1] == 4:
                if starting_hand[0].rank == starting_hand[1].rank:
                    flush = "d"
                else:
                    flush = "d_" + self._find_which_card_matches_suit(starting_hand, flop_suits_counter)
            else:
                flush = "n"
        elif flop_suits_counter.most_common(1)[0][1] == 2:
            flop_type = "_twoone_"
            if all_suits_coutner.most_common(1)[0][1] == 4:
                flush = "d"
            else:
                flush = "n"
        else:
            flop_type = "_rainbow_"
            flush = "n"
        return f"{starting_hand_string}_{board_string}{flop_type}{flush}"
    
    def get_turn_string(self, starting_hand: np.ndarray, flop: np.ndarray, turn:np.ndarray) -> str:
        starting_hand_string = self.get_starting_hand_string(starting_hand)
        board = np.concatenate((flop, turn))
        board_string = self._translate_board_to_string(board)
        board_suits = [card.get_suit() for card in board]
        all_suits = [card.get_suit() for card in np.concatenate((starting_hand, board))]
        board_suits_counter = Counter(board_suits)
        all_suits_coutner = Counter(all_suits)
        if board_suits_counter.most_common(1)[0][1] == 4:
            turn_type = "_mono_"
            if all_suits_coutner.most_common(1)[0][1] == 6:
                flush = "f"
            elif all_suits_coutner.most_common(1)[0][1] == 5:
                if starting_hand[0].rank == starting_hand[1].rank:
                    flush = "f"
                else:
                    flush = "f_" + self._find_which_card_matches_suit(starting_hand, board_suits_counter)
            else:
                flush = "n"
        elif board_suits_counter.most_common(1)[0][1] == 3:
            turn_type = "_threeone_"
            if all_suits_coutner.most_common(1)[0][1] == 5:
                flush = "f"
            elif all_suits_coutner.most_common(1)[0][1] == 4:
                if starting_hand[0].rank == starting_hand[1].rank:
                    flush = "d"
                else:
                    flush = "d_" + self._find_which_card_matches_suit(starting_hand, board_suits_counter)
            else:
                flush = "n"
        elif board_suits_counter.most_common(1)[0][1] == 2:
            if board_suits_counter.most_common(2)[1][1] == 2:
                turn_type = "_twotwo_"
                if all_suits_coutner.most_common(1)[0][1] == 4:
                    flush = "d"
                else:
                    flush = "n"
                    
            else:
                turn_type = "_twooneone_"
                if all_suits_coutner.most_common(1)[0][1] == 4:
                    flush = "d"
                else:
                    flush = "n"
        else:
            turn_type = "_rainbow_"
            flush = "n"
                
        return f"{starting_hand_string}_{board_string}{turn_type}{flush}"
    
    
    def get_river_string(self, starting_hand: np.ndarray, flop: np.ndarray, turn:np.ndarray, river:np.ndarray) -> str:
        starting_hand_string = self.get_starting_hand_string(starting_hand)
        board = np.concatenate((flop, turn, river))
        board_string = self._translate_board_to_string(board)
        board_suits = [card.get_suit() for card in board]
        all_cards =  np.concatenate((starting_hand, board))
        all_suits = [card.get_suit() for card in all_cards]
        board_suits_counter = Counter(board_suits)
        all_suits_coutner = Counter(all_suits)
        if board_suits_counter.most_common(1)[0][1] == 5:
            river_type = "_mono_"
            if all_suits_coutner.most_common(1)[0][1] == 7:
                flush = "f"
            elif all_suits_coutner.most_common(1)[0][1] == 6:
                highest_card_value = self._find_the_highest_flush_card(all_cards, all_suits_coutner.most_common(1)[0][0])
                if starting_hand[0].rank == starting_hand[1].rank:
                    flush = f"f_{highest_card_value}_high"
                else:
                    flush = f"f_{self._find_which_card_matches_suit(starting_hand, board_suits_counter)}_{highest_card_value}_high"
            else:
                flush = "n"
        elif board_suits_counter.most_common(1)[0][1] == 4:
            river_type = "_fourone_"
            if all_suits_coutner.most_common(1)[0][1] == 6:
                highest_card_value = self._find_the_highest_flush_card(all_cards, all_suits_coutner.most_common(1)[0][0])
                flush = f"f_{highest_card_value}_high"
            elif all_suits_coutner.most_common(1)[0][1] == 5:
                highest_card_value = self._find_the_highest_flush_card(all_cards, all_suits_coutner.most_common(1)[0][0])
                if starting_hand[0].rank == starting_hand[1].rank:
                    flush = f"f_{highest_card_value}_high"
                else:
                    flush = f"f_{self._find_which_card_matches_suit(starting_hand, board_suits_counter)}_{highest_card_value}_high"
            else:
                flush = "n"
        elif board_suits_counter.most_common(1)[0][1] == 3:
            river_type = "_threeoneone_"
            if all_suits_coutner.most_common(1)[0][1] == 5:
                highest_card_value = self._find_the_highest_flush_card(all_cards, all_suits_coutner.most_common(1)[0][0])
                flush = f"f_{highest_card_value}_high"
            else:
                flush = "n" 
        else:
            river_type = "_twooneoneone_"
            flush = "n"
                
        return f"{starting_hand_string}_{board_string}{river_type}{flush}"
    
    def _find_which_card_matches_suit(self, starting_hand: np.ndarray, board_suits_counter: Counter) -> str:
        higher_card = starting_hand[0] if starting_hand[0] > starting_hand[1] else starting_hand[1]
        if higher_card.get_suit() == board_suits_counter.most_common(1)[0][0]:
            return "higher"
        else:
            return "lower" 
    
    def _find_the_highest_flush_card(self, all_cards: np.ndarray, suit: Suit) -> str:
        def condition(card):
            return card.get_suit() == suit
        mask = np.vectorize(condition)(all_cards)
        filtered = all_cards[mask]
        return str(max(filtered).rank.value)