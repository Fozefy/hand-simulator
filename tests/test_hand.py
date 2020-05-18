import pytest
from collections import Counter
import hand as h

def test_init():
    hand = h.Hand('')
    assert len(hand.deck) == 60

def test_process():
    hand = h.Hand("tests/testdeck.txt")
    assert len(hand.deck) == 14
    assert hand.deck[0] == "testcard1"
    assert hand.deck[4] == "testcard3"
    assert hand.deck[10] == "testcard5"
    assert hand.decklist["testcard2"] == 2
    assert hand.decklist["testcard4"] == 4
    hand = h.Hand("tests/mini_testdeck.txt")
    assert len(hand.deck) == 6
    assert hand.deck[0] == "card1"
    assert hand.decklist["card2"] == 2

def test_new_hand():
    hand = h.Hand("tests/testdeck.txt")
    hand.new_hand()
    assert hand.size == 7
    assert 2 <= len(hand.cards) <= 5 #the types of cards selected
    hand.new_hand(14)
    assert hand.size == 14
    assert len(hand.cards) == 5 #All cards selected
    assert "testcard1" in hand.cards
    assert hand.card_counts["testcard3"] == 3

def test_generate_subset_hands():
    hand = h.Hand("tests/testdeck.txt")
    assert hand.size == 0
    assert hand.num_subets() == 0
    hand.generate_subset_hands(1)
    assert hand.size < 0
    assert hand.num_subets() == 0

    hand.new_hand(7)
    hand.generate_subset_hands(1)
    assert hand.size == 6
    assert hand.num_subets() == 7

    hand.new_hand(7)
    hand.generate_subset_hands(2)
    assert hand.size == 5
    assert hand.num_subets() == 21

def test_set_hand():
    hand = h.Hand("tests/testdeck.txt")
    newHand = ['testcard2','testcard3']
    hand.set_hand(newHand)
    assert hand.card_counts['testcard3'] == 1
    assert hand.card_counts['testcard2'] == 1
    newHand.append('testcard2')
    hand.set_hand(newHand)
    assert hand.card_counts['testcard3'] == 1
    assert hand.card_counts['testcard2'] == 2

def test_select_random_remaining():
    hand = h.Hand("tests/mini_testdeck.txt")
    newHand = ['card2', 'card3', 'card3', 'card3', 'card1']
    hand.draw_card(0)
    hand.draw_card(1)
    hand.draw_card(3)
    hand.draw_card(4)
    hand.draw_card(5)
    assert hand.select_random_remaining() == 2

    hand.new_hand(0)
    hand.draw_card(1)
    hand.draw_card(2)
    hand.draw_card(3)
    hand.draw_card(4)
    chosenNums = []
    chosenNums.append(hand.select_random_remaining())
    hand.draw_card(chosenNums[0])
    chosenNums.append(hand.select_random_remaining())
    assert Counter(chosenNums) == Counter([0,5])

    hand.draw_card(chosenNums[1])
    with pytest.raises(Exception):
        #Test selecting from an empty deck
        hand.select_random_remaining()

def test_draw_card():
    hand = h.Hand("tests/testdeck.txt")
    hand.draw_card()
    assert hand.size == 1
    hand.new_hand(7)
    hand.draw_card()
    hand.draw_card()
    assert hand.size == 9
    hand.new_hand(11)
    hand.draw_card()
    hand.draw_card()
    hand.draw_card()
    assert hand.size == 14 #We should now have the full deck
    assert hand.card_counts["testcard4"] == 4
    assert hand.card_counts["testcard5"] == 4
    
    #Test specific draw
    hand.new_hand(0)
    hand.draw_card(0)
    assert hand.size == 1
    assert hand.card_counts["testcard1"] == 1
    with pytest.raises(Exception):
        #Test selecting a drawn card
        hand.draw_card(0)