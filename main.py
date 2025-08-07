from poker_solver.hand_translator import HandTranslator
from deck.deck import Deck
import numpy as np
from time import time 
from poker.game import Game
from poker_solver.sequence_generator import SequenceGenerator
from poker_solver.poker_solver import PokerSolver
import pickle
import json

buckets = 10

with open('poker_solvr_10.pickle', 'rb') as f:
    solver = pickle.load(f)
     
"""with open('poker_solver_10_150_000_iterations.pickle', 'rb') as f:
    solver_one = pickle.load(f)"""
      
"""print("start_trianing")
print("12:15")
start = time()
solver.train_solver(50_000)
end = time()
print(f"Time: {end - start}")
with open('poker_solvr_10.pickle', 'wb') as f:
    pickle.dump(solver, f, protocol=pickle.HIGHEST_PROTOCOL)"""

#for k, v in solver.node_groups.items():
#    if len(k) == 1 and k[-1] == "BC":
#        for i in range(buckets):
#            print(np.round(v[i].get_average_strategy(), 3), v[i].visited)

s = 0
print("\n")
for k, v in solver.node_groups.items():
    if len(k) == 4 and k[0] == "BCP" and k[1] == "BBC" and k[2] == "BBC" and k[-1] == "P":
        for i in range(buckets):
            print(np.round(v[i].get_average_strategy(), 3), v[i].visited)
            s += v[i].visited

print(s)

result = 0
for _ in range(1):
    game = Game(2, 100000, 2, solver, solver)
    winner = game.play_game()
    if winner == 0:
        result += 1

"""
end = list()
sequence_generator = SequenceGenerator()
for x in sequence_generator.preflop_sequences:
    last_seq = x.betting_sequence[-1]
    if last_seq not in end and x.ends_round:
        end.append(last_seq)
        
for x in sequence_generator.flop_sequences:
    last_seq = x.betting_sequence[-1]
    if last_seq not in end and x.ends_round:
        end.append(last_seq)

for e in end:
    print(e)
sequence_list = sequence_generator.get_all_sequences()"""


"""
with open("poker/ehs/normalized/postriver_ehs_normal.json", "r") as f:
    river_strengths = json.load(f) 
hand_translator = HandTranslator()
deck = Deck()
x = 10
for perm in range(1000):
    deck.shuffle()
    cards = np.concatenate((deck.draw_card_by_tag("As"), deck.draw_card_by_tag("Ad")))
    flop = deck.draw_cards(3)
    turn = deck.draw_cards(1)
    river = deck.draw_cards(1)
    river_string = hand_translator.get_river_string(cards, flop, turn, river)
    if river_strengths[river_string] < 0.5:
        print(cards, flop, turn, river, river_string, river_strengths[river_string])
    deck.return_cards(cards)
    deck.return_cards(flop)
    deck.return_cards(turn)
    deck.return_cards(river)
"""