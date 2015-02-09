from collections import defaultdict
from deck import *
import random

class Player(object):
    def __init__(self, id):
        self.hand = []
        self.id = id
        self.score = 0
        self.tricks = 0

    def take(self, cards):
        self.hand += cards

    def display_hand(self):
        print '----------'
        for card in self.hand:
            print card
        print '----------'

    def make_bid(self, forbidden=None):
        legal = [b for b in range(len(self.hand)+1) if b != forbidden]
        self.bid = random.choice(legal)

        print self,'makes bid',self.bid
        return self.bid

    def play(self, suit):
        legal = [c for c in self.hand if c.suit == suit]
        if not legal:
            legal = self.hand
        card = random.choice(legal)
        self.hand.remove(card)

        print self,'plays',card
        return card

    def calc_score(self, num_cards):
        if self.tricks != self.bid:
            self.score += 0
        if self.bid == 0:
            self.score += 5 + num_cards
        else:
            self.score += 10 + self.bid**2
        self.tricks = 0

    def take_trick(self):
        self.tricks += 1

    def __str__(self):
        return 'Player' + str(self.id)

class ManualPlayer(Player):
    def play(self, suit):
        pass

    def make_bid(self, forbidden=None):
        pass

class OhHell:
    def __init__(self, n):
        self.players = [Player(i) for i in range(n)]
        self.deck = Deck()
        self.max_tricks = 52/len(self.players)
        self.num_tricks = 1
        self.round = 1
        self.dealer = 0

    def deal(self, n):
        for p in self.players:
            p.take(self.deck.draw(n=n))

    def find_winner(self, trick):
        highests = [card for card in trick if card.suit == self.trump]
        if not highests:
            highests = [card for card in trick if card.suit == self.lead_suit]
        return trick[max(highests, key=lambda x: (x.rank.value-1)%len(Rank))]

    # returns a card representing trump, or None for no trump
    def choose_trump(self):
        if self.round % 5 != 0 and self.num_tricks*len(self.players) != 52:
            self.trump = self.deck.draw()[0].suit
        else:
            self.trump = None

        print '\n\n****************\nRound',self.round,'!'
        print 'The trump is',self.trump

    def set_num_tricks(self):
        if self.round <= self.max_tricks:
            self.num_tricks = self.round 
        else:
            self.num_tricks = self.round - self.max_tricks

    def play_round(self):
        self.set_num_tricks()
        self.deal(self.num_tricks)
        self.choose_trump()

        # bid
        total_bid = 0
        for i in range(1, len(self.players)):
            player_index = (self.dealer + i) % len(self.players)
            player = self.players[player_index]
            bid = player.make_bid()
            total_bid += bid
        self.players[self.dealer].make_bid(forbidden=self.num_tricks-total_bid)

        # play
        leader = self.dealer
        self.lead_suit = None
        print 'num tricks',self.num_tricks
        for t in range(self.num_tricks):
            print '\nTrick',t
            trick = {}
            for i in range(len(self.players)):
                player_index = (leader + i) % len(self.players)
                player = self.players[player_index]
                print player,"'s hand:"
                player.display_hand()

                card = player.play(self.lead_suit)
                self.lead_suit = card.suit if not self.lead_suit else self.lead_suit
                trick[card] = player_index
            leader = self.find_winner(trick)
            self.players[leader].take_trick()

        for p in self.players:
            p.calc_score(self.num_tricks)

        self.deck.shuffle()
        self.round += 1
        self.dealer = (self.dealer + 1) % len(self.players)

    def game_over(self):
        return self.round > self.max_tricks and self.num_tricks == 1

if __name__ == '__main__':
    hell = OhHell(3)
    while not hell.game_over():
        hell.play_round()
