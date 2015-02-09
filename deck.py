from enum import Enum
import random

class Suit(Enum):
    spades = 0
    hearts = 1
    diamonds = 2
    clubs = 3


class Rank(Enum):
    _K = 13
    _Q = 12
    _J = 11
    _10 = 10
    _9 = 9
    _8 = 8
    _7 = 7
    _6 = 6
    _5 = 5
    _4 = 4
    _3 = 3
    _2 = 2
    _A = 1

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank.name + ' of ' + self.suit.name

class Deck:
    def __init__(self):
        self.pile = self.create_cards()
        self.out = []

    def draw(self, n=1):
        cards = []
        for i in range(n):
            if len(self.pile) == 0:
                return cards
            card = random.choice(self.pile)
            self.pile.remove(card)
            self.out.append(card)
            cards.append(card)
        return cards

    def shuffle(self):
        self.pile += self.out

    def create_cards(self):
        deck = []
        for suit in Suit:
            for rank in Rank:
                deck.append(Card(suit, rank))
        return deck

    def __str__(self):
        s = ''
        for card in self.pile:
            s += str(card) + '\n'
        return s

if __name__ == '__main__':
    for suit in Suit:
        print suit

    for rank in Rank:
        print rank

    deck = Deck()
    print deck
