from deck.deck import Deck
from deck.card import Card
from poker_solver.hand_translator import HandTranslator
import numpy as np


hand_translator = HandTranslator()
deck = Deck()

def test_starting_hand_translation():
    starting_hand = np.concatenate((deck.draw_card_by_tag("Ad"), deck.draw_card_by_tag("As")))
    assert hand_translator.get_starting_hand_string(starting_hand) == "AAo"
    deck.return_cards(starting_hand)
    starting_hand = np.concatenate((deck.draw_card_by_tag("Kd"), deck.draw_card_by_tag("As")))
    assert hand_translator.get_starting_hand_string(starting_hand) == "AKo"
    deck.return_cards(starting_hand)
    starting_hand = np.concatenate((deck.draw_card_by_tag("Ks"), deck.draw_card_by_tag("As")))
    assert hand_translator.get_starting_hand_string(starting_hand) == "AKs"
    deck.return_cards(starting_hand)
    starting_hand = np.concatenate((deck.draw_card_by_tag("As"), deck.draw_card_by_tag("Ks")))
    assert hand_translator.get_starting_hand_string(starting_hand) == "AKs"
    deck.return_cards(starting_hand)
    starting_hand = np.concatenate((deck.draw_card_by_tag("As"), deck.draw_card_by_tag("Kd")))
    assert hand_translator.get_starting_hand_string(starting_hand) == "AKo"
    deck.return_cards(starting_hand)
    starting_hand = np.concatenate((deck.draw_card_by_tag("9s"), deck.draw_card_by_tag("2d")))
    assert hand_translator.get_starting_hand_string(starting_hand) == "92o"
    deck.return_cards(starting_hand)
    starting_hand = np.concatenate((deck.draw_card_by_tag("Ts"), deck.draw_card_by_tag("Kd")))
    assert hand_translator.get_starting_hand_string(starting_hand) == "KTo"
    deck.return_cards(starting_hand)
    starting_hand = np.concatenate((deck.draw_card_by_tag("2s"), deck.draw_card_by_tag("2d")))
    assert hand_translator.get_starting_hand_string(starting_hand) == "22o"
    deck.return_cards(starting_hand)
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    assert hand_translator.get_starting_hand_string(starting_hand) == "Q4s"
    deck.return_cards(starting_hand)

def test_flop_translation():
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2c")))
    assert hand_translator.get_flop_string(starting_hand, flop) == "Q4s_AK2_mono_f"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kh"), deck.draw_card_by_tag("Ah"), deck.draw_card_by_tag("2h")))
    turn = deck.draw_card_by_tag("6h")
    assert hand_translator.get_turn_string(starting_hand, flop, turn) == "Q4s_AK62_mono_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2d")))
    assert hand_translator.get_flop_string(starting_hand, flop) == "Q4s_AK2_twoone_d"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("Ad"), deck.draw_card_by_tag("2d")))
    assert hand_translator.get_flop_string(starting_hand, flop) == "Q4s_AK2_twoone_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("As"), deck.draw_card_by_tag("2d")))
    assert hand_translator.get_flop_string(starting_hand, flop) == "Q4s_AK2_rainbow_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4s"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2c")))
    assert hand_translator.get_flop_string(starting_hand, flop) == "Q4o_AK2_mono_d_higher"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qs")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2c")))
    assert hand_translator.get_flop_string(starting_hand, flop) == "Q4o_AK2_mono_d_lower"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4s"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2h")))
    assert hand_translator.get_flop_string(starting_hand, flop) == "Q4o_AK2_twoone_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4s"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("As"), deck.draw_card_by_tag("2h")))
    assert hand_translator.get_flop_string(starting_hand, flop) == "Q4o_AK2_rainbow_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    
def test_turn_translation():
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2c")))
    turn = deck.draw_card_by_tag("6c")
    assert hand_translator.get_turn_string(starting_hand, flop, turn) == "Q4s_AK62_mono_f"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kh"), deck.draw_card_by_tag("Ah"), deck.draw_card_by_tag("2h")))
    turn = deck.draw_card_by_tag("6h")
    assert hand_translator.get_turn_string(starting_hand, flop, turn) == "Q4s_AK62_mono_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2c")))
    turn = deck.draw_card_by_tag("6h")
    assert hand_translator.get_turn_string(starting_hand, flop, turn) == "Q4s_AK62_threeone_f"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kh"), deck.draw_card_by_tag("Ah"), deck.draw_card_by_tag("2h")))
    turn = deck.draw_card_by_tag("6d")
    assert hand_translator.get_turn_string(starting_hand, flop, turn) == "Q4s_AK62_threeone_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kh"), deck.draw_card_by_tag("Ah"), deck.draw_card_by_tag("2c")))
    turn = deck.draw_card_by_tag("6c")
    assert hand_translator.get_turn_string(starting_hand, flop, turn) == "Q4s_AK62_twotwo_d"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kh"), deck.draw_card_by_tag("Ah"), deck.draw_card_by_tag("2d")))
    turn = deck.draw_card_by_tag("6d")
    assert hand_translator.get_turn_string(starting_hand, flop, turn) == "Q4s_AK62_twotwo_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2h")))
    turn = deck.draw_card_by_tag("6d")
    assert hand_translator.get_turn_string(starting_hand, flop, turn) == "Q4s_AK62_twooneone_d"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kh"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2h")))
    turn = deck.draw_card_by_tag("6d")
    assert hand_translator.get_turn_string(starting_hand, flop, turn) == "Q4s_AK62_twooneone_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qs")))
    flop = np.concatenate((deck.draw_card_by_tag("Ks"), deck.draw_card_by_tag("As"), deck.draw_card_by_tag("2s")))
    turn = deck.draw_card_by_tag("6s")
    assert hand_translator.get_turn_string(starting_hand, flop, turn) == "Q4o_AK62_mono_f_higher"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4s"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Ks"), deck.draw_card_by_tag("As"), deck.draw_card_by_tag("2s")))
    turn = deck.draw_card_by_tag("6s")
    assert hand_translator.get_turn_string(starting_hand, flop, turn) == "Q4o_AK62_mono_f_lower"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qs")))
    flop = np.concatenate((deck.draw_card_by_tag("Ks"), deck.draw_card_by_tag("As"), deck.draw_card_by_tag("2c")))
    turn = deck.draw_card_by_tag("6s")
    assert hand_translator.get_turn_string(starting_hand, flop, turn) == "Q4o_AK62_threeone_d_higher"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4s"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kd"), deck.draw_card_by_tag("As"), deck.draw_card_by_tag("2s")))
    turn = deck.draw_card_by_tag("6s")
    assert hand_translator.get_turn_string(starting_hand, flop, turn) == "Q4o_AK62_threeone_d_lower"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qs")))
    flop = np.concatenate((deck.draw_card_by_tag("Kd"), deck.draw_card_by_tag("Ad"), deck.draw_card_by_tag("2d")))
    turn = deck.draw_card_by_tag("6s")
    assert hand_translator.get_turn_string(starting_hand, flop, turn) == "Q4o_AK62_threeone_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qs")))
    flop = np.concatenate((deck.draw_card_by_tag("Ks"), deck.draw_card_by_tag("As"), deck.draw_card_by_tag("2d")))
    turn = deck.draw_card_by_tag("6d")
    assert hand_translator.get_turn_string(starting_hand, flop, turn) == "Q4o_AK62_twotwo_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qs")))
    flop = np.concatenate((deck.draw_card_by_tag("Ks"), deck.draw_card_by_tag("As"), deck.draw_card_by_tag("2d")))
    turn = deck.draw_card_by_tag("6h")
    assert hand_translator.get_turn_string(starting_hand, flop, turn) == "Q4o_AK62_twooneone_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qs")))
    flop = np.concatenate((deck.draw_card_by_tag("Ks"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2d")))
    turn = deck.draw_card_by_tag("6h")
    assert hand_translator.get_turn_string(starting_hand, flop, turn) == "Q4o_AK62_rainbow_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    

def test_river_translation():
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2c")))
    turn = deck.draw_card_by_tag("6c")
    river = deck.draw_card_by_tag("Tc")
    assert hand_translator.get_river_string(starting_hand, flop, turn, river) == "Q4s_AKT62_mono_f"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kh"), deck.draw_card_by_tag("Ah"), deck.draw_card_by_tag("2h")))
    turn = deck.draw_card_by_tag("6h")
    river = deck.draw_card_by_tag("Th")
    assert hand_translator.get_river_string(starting_hand, flop, turn, river) == "Q4s_AKT62_mono_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2c")))
    turn = deck.draw_card_by_tag("6h")
    river = deck.draw_card_by_tag("Tc")
    assert hand_translator.get_river_string(starting_hand, flop, turn, river) == "Q4s_AKT62_fourone_f_A_high"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("3c"), deck.draw_card_by_tag("2c")))
    turn = deck.draw_card_by_tag("6h")
    river = deck.draw_card_by_tag("Tc")
    assert hand_translator.get_river_string(starting_hand, flop, turn, river) == "Q4s_KT632_fourone_f_K_high"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("5c"), deck.draw_card_by_tag("6c"), deck.draw_card_by_tag("2c")))
    turn = deck.draw_card_by_tag("6h")
    river = deck.draw_card_by_tag("Tc")
    assert hand_translator.get_river_string(starting_hand, flop, turn, river) == "Q4s_T6652_fourone_f_Q_high"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Ks"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2s")))
    turn = deck.draw_card_by_tag("6s")
    river = deck.draw_card_by_tag("Ts")
    assert hand_translator.get_river_string(starting_hand, flop, turn, river) == "Q4s_AKT62_fourone_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2h")))
    turn = deck.draw_card_by_tag("6s")
    river = deck.draw_card_by_tag("Tc")
    assert hand_translator.get_river_string(starting_hand, flop, turn, river) == "Q4s_AKT62_threeoneone_f_A_high"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kh"), deck.draw_card_by_tag("Ah"), deck.draw_card_by_tag("2h")))
    turn = deck.draw_card_by_tag("6s")
    river = deck.draw_card_by_tag("Tc")
    assert hand_translator.get_river_string(starting_hand, flop, turn, river) == "Q4s_AKT62_threeoneone_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2h")))
    turn = deck.draw_card_by_tag("6h")
    river = deck.draw_card_by_tag("Ts")
    assert hand_translator.get_river_string(starting_hand, flop, turn, river) == "Q4s_AKT62_twooneoneone_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4s"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2c")))
    turn = deck.draw_card_by_tag("6c")
    river = deck.draw_card_by_tag("Tc")
    assert hand_translator.get_river_string(starting_hand, flop, turn, river) == "Q4o_AKT62_mono_f_higher_A_high"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qs")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2c")))
    turn = deck.draw_card_by_tag("6c")
    river = deck.draw_card_by_tag("Tc")
    assert hand_translator.get_river_string(starting_hand, flop, turn, river) == "Q4o_AKT62_mono_f_lower_A_high"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4s"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kh"), deck.draw_card_by_tag("Ah"), deck.draw_card_by_tag("2h")))
    turn = deck.draw_card_by_tag("6h")
    river = deck.draw_card_by_tag("Th")
    assert hand_translator.get_river_string(starting_hand, flop, turn, river) == "Q4o_AKT62_mono_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4s"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("As"), deck.draw_card_by_tag("2c")))
    turn = deck.draw_card_by_tag("6c")
    river = deck.draw_card_by_tag("Tc")
    assert hand_translator.get_river_string(starting_hand, flop, turn, river) == "Q4o_AKT62_fourone_f_higher_K_high"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4c"), deck.draw_card_by_tag("Qs")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2c")))
    turn = deck.draw_card_by_tag("6c")
    river = deck.draw_card_by_tag("Ts")
    assert hand_translator.get_river_string(starting_hand, flop, turn, river) == "Q4o_AKT62_fourone_f_lower_A_high"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4s"), deck.draw_card_by_tag("Qd")))
    flop = np.concatenate((deck.draw_card_by_tag("Kc"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2c")))
    turn = deck.draw_card_by_tag("6c")
    river = deck.draw_card_by_tag("Td")
    assert hand_translator.get_river_string(starting_hand, flop, turn, river) == "Q4o_AKT62_fourone_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4s"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Ks"), deck.draw_card_by_tag("As"), deck.draw_card_by_tag("2s")))
    turn = deck.draw_card_by_tag("6c")
    river = deck.draw_card_by_tag("Tc")
    assert hand_translator.get_river_string(starting_hand, flop, turn, river) == "Q4o_AKT62_threeoneone_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)
    
    starting_hand = np.concatenate((deck.draw_card_by_tag("4s"), deck.draw_card_by_tag("Qc")))
    flop = np.concatenate((deck.draw_card_by_tag("Kh"), deck.draw_card_by_tag("Ac"), deck.draw_card_by_tag("2c")))
    turn = deck.draw_card_by_tag("6s")
    river = deck.draw_card_by_tag("Td")
    assert hand_translator.get_river_string(starting_hand, flop, turn, river) == "Q4o_AKT62_twooneoneone_n"
    deck.return_cards(starting_hand)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)