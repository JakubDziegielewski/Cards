from deck.deck import *
import numpy as np

np.random.seed(1)
full_deck = Deck()


def test_bottom_draw_and_return():
    full_deck.shuffle()
    bottom_card = full_deck.get_bottom_card()
    next_bottom_card = full_deck.cards[3]
    fifth_card = full_deck.cards[4]
    top_card = full_deck.get_top_card()
    drawn_cards = full_deck.draw_cards(3, position="bottom")
    assert next_bottom_card == full_deck.get_bottom_card()
    assert fifth_card == full_deck.cards[1]
    assert top_card == full_deck.get_top_card()
    full_deck.return_cards(drawn_cards, position="bottom")
    assert bottom_card == full_deck.get_bottom_card()
    assert top_card == full_deck.get_top_card()


def test_top_draw_and_return():
    full_deck.shuffle()
    top_card = full_deck.get_top_card()
    next_top_card = full_deck.cards[full_deck.deck_size - 4]
    bottom_card = full_deck.get_bottom_card()
    drawn_cards = full_deck.draw_cards(3)
    assert next_top_card == full_deck.get_top_card()
    assert bottom_card == full_deck.get_bottom_card()
    full_deck.return_cards(drawn_cards)
    assert top_card == full_deck.get_top_card()
    assert bottom_card == full_deck.get_bottom_card()
