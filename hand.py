import numpy as np
from collections import Counter
import scipy.stats as sps
import itertools


class Hand:
    def __init__(self, deck_name):
        self.deck_name = deck_name
        self.num_subsets = 0
        self.subsetIndex = -1
        self.subsetHands = None
        if deck_name:
            self.deck, self.decklist = self.process(deck_name)
        else:
            self.deck = ["Storm Crow"] * 60
            self.decklist = dict(Counter(self.deck))
        self.new_hand(0) #init hand vars

    def hand_as_str(self):
        return str(self.card_counts)

    def process(self, filename):
        with open(filename, "r") as file:
            file_read = [line.strip().split(" ", 1)
                         for line in file if len(line.split()) > 0]
        deck = []
        for [number, card] in file_read:
            deck += [card] * int(number)
        decklist = dict(Counter(deck))
        return deck, decklist

    def set_deck(self, new_deck):
        if isinstance(new_deck, list):
            self.deck = new_deck
            self.decklist = dict(Counter(new_deck))
        elif isinstance(new_deck, dict):
            deck = []
            for card, number in new_deck.items():
                deck += [card] * int(number)
            self.deck = deck
            self.decklist = dict(Counter(new_deck))
        elif isinstance(new_deck, str):
            self.deck, self.decklist = self.process(new_deck)
        else:
            print("ERROR: invalid deck format")
            return False
        return True

    def get_deck(self):
        return self.deck.copy()

    def get_decklist(self):
        return dict(self.decklist.copy())

    def num_subets(self):
        return self.num_subsets

    def chooseSubset(self, index):
        self.subsetIndex = index
        if index is None:
            self.card_counts = self.origHand
        else:
            self.card_counts = Counter(self.subsetHands[self.subsetIndex])
        self.cards = set(self.card_counts.keys())
        self.size = sum(self.card_counts.values())

    def nextSubset(self):
        self.subsetIndex += 1
        self.card_counts = Counter(self.subsetHands[self.subsetIndex])
        self.cards = set(self.card_counts.keys())
        self.size = sum(self.card_counts.values())

    def generate_subset_hands(self, numHide, noRemoveList = []):
        self.origHand = self.card_counts.copy()
        counterAsList = sorted(self.card_counts.elements())

        handSubsets = list(itertools.combinations(counterAsList, self.size - numHide))

        def equalNumberOfNotToBeRemovedCards(subsetHand, noRemoveList):
            handCount = Counter(subsetHand)
            for cardNameToNotBeRemoved in noRemoveList:
                #if the number of cardName in the subset hand is less than the original hand
                if(self.origHand[cardNameToNotBeRemoved] != handCount[cardNameToNotBeRemoved]):
                    return False
            return True

        self.subsetHands = [x for x in handSubsets if equalNumberOfNotToBeRemovedCards(x, noRemoveList)]
        self.num_subsets = len(self.subsetHands)
        self.subsetIndex = -1
        self.size = self.size - numHide

    def scry_bottom(self):
        self.card_counts[self.lastDraw] += -1
        self.draw_card()
        self.size += -1 #Set size after so we don't redraw this card

    def select_random_remaining(self):
        deckSize = len(self.deck)
        if (deckSize <= self.size):
            raise Exception("The deck is empty.")

        remainingDeck = [i for i in range(deckSize) if i not in self.draws]
        return np.random.choice(remainingDeck)

    def draw_card(self, choice = None):
        if choice is None:
            choice = self.select_random_remaining()
        elif choice in self.draws:
            raise Exception("Chosen card already drawn.")

        self.draws = np.append(self.draws, choice)
        
        self.add_card_to_cur_hand(choice)

        return choice

    def add_card_to_cur_hand(self, choice):
        self.lastDraw = self.deck[choice]
        self.card_counts[self.lastDraw] += 1
        self.cards = set(self.card_counts.keys())
        self.size += 1

        return choice

    def new_hand(self, size=7):
        self.size = size
        self.draws = np.random.choice(len(self.deck), size, replace=False)
        self.card_counts = Counter([self.deck[i] for i in self.draws])
        self.cards = set(self.card_counts.keys())
        return self.card_counts.copy()

    def set_hand(self, newHand):
        self.size = len(newHand)
        self.card_counts = Counter(newHand)
        self.cards = set(self.card_counts.keys())

        if self.subsetHands is not None:
            for i in range(0, len(self.subsetHands)):
                if self.card_counts == Counter(self.subsetHands[i]):
                    return i

        return None

    def has_tron(self):
        check = [0] * 4
        if "Urza's Tower" in self.cards:
            check[0] = 1
        if "Urza's Mine" in self.cards:
            check[1] = 1
        if "Urza's Power Plant" in self.cards:
            check[2] = 1
        if "Expedition Map" in self.cards:
            check[3] = 1
        return float(sum(check) >= 3)

    def contains(self, cards):
        if isinstance(cards, str):
            return 1.0*(cards in self.cards)
        return float(len(self.cards & set(cards)) > 0)

    def count_of(self, cards):
        if isinstance(cards, str):
            return float(self.card_counts[cards])
        return float(sum([self.card_counts[card] for card in cards]))

    def handsize(self):
        return self.size

    def expect(self, cards, size=7):
        if isinstance(cards, str):
            n = self.decklist[cards]
        elif isinstance(cards, list):
            n = sum([self.decklist[card] for card in cards])
        else:
            return 0
        if n == 0:
            return 0
        return sps.hypergeom.mean(len(self.deck), n, size)
