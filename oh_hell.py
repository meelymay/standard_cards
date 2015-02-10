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
        print str(self)+"'s hand:"
        print '----------'
        for card in self.hand:
            print card
        print '----------'

    def make_bid(self, forbidden=None):
        legal = [b for b in range(len(self.hand)+1) if b != forbidden]
        self.bid = random.choice(legal)

        print self,'bids',self.bid
        return self.bid

    def play(self, suit):
        legal = [c for c in self.hand if c.suit == suit]
        if not legal:
            legal = self.hand
        card = random.choice(legal)
        self.hand.remove(card)

        print self,'plays\t\t\t',card
        return card

    def calc_score(self, num_cards):
        print self,
        if self.tricks != self.bid:
            print 'missed!',
            self.score += 0
        elif self.bid == 0:
            self.score += 5 + num_cards
            print 'made %s.' % 0,
        else:
            self.score += 10 + self.bid**2
            print 'made %s.' % self.bid,
        print '\tScore:',self.score
        self.tricks = 0

    def take_trick(self):
        self.tricks += 1

    def __str__(self):
        return 'Player' + str(self.id)

class ManualPlayer(Player):
    def play(self, lead_suit):
        cards = []
        legal = [c for c in self.hand if c.suit == lead_suit]
        if not legal:
            legal = self.hand
        if len(legal) == 1:
            cards = legal

        while not cards:
            self.display_hand()
            (rank, suit) = raw_input('Choose a card to play: ').split()
            cards = [c for c in legal if c.rank == Rank[rank] and c.suit == Suit[suit]]

        card = cards[0]
        print self,'plays',card
        self.hand.remove(card)
        return card

    def make_bid(self, forbidden=None):
        self.display_hand()
        bid = forbidden
        while bid not in [i for i in range(len(self.hand)+1) if i != forbidden]:
            bid = int(raw_input('Bid anything but %s: ' % forbidden))

        self.bid = bid
        return self.bid

class OhHell:
    def __init__(self, n):
        self.players = [Player(i) for i in range(n-1)]+[ManualPlayer(n-1)]
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
        winner = trick[max(highests, key=lambda x: (x.rank.value-2)%len(Rank))]
        print self.players[winner],'takes the trick!'
        return winner

    # returns a card representing trump, or None for no trump
    def choose_trump(self):
        trump_card = None
        self.trump = None
        if self.round % 5 != 0 and self.num_tricks*len(self.players) != 52:
            trump_card = self.deck.draw()[0]
            self.trump = trump_card.suit

        print '\n\n****************\nRound',self.round,'!'
        print '\t\t\t\tTRUMP:',trump_card

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
        leader = (self.dealer+1) % len(self.players)
        for t in range(self.num_tricks):
            print '\nTrick',t
            self.lead_suit = None
            trick = {}
            for i in range(len(self.players)):
                player_index = (leader + i) % len(self.players)
                player = self.players[player_index]

                card = player.play(self.lead_suit)
                self.lead_suit = card.suit if not self.lead_suit else self.lead_suit
                trick[card] = player_index
            leader = self.find_winner(trick)
            self.players[leader].take_trick()

        print '##### SCORES ######'
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
