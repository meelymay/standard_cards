from deck import *
import random

class Player(object):
    def __init__(self, id):
        self.hand = []
        self.id = id

    def display_hand(self):
        print '----------'
        for card in self.hand:
            print card
        print '----------'

    def take(self, cards):
        self.hand += cards

    def ask(self, opponents):
        opponent = random.choice(opponents)
        rank = random.choice(self.hand).rank
        return (rank, opponent)

    def respond(self, rank):
        cards_of_rank = []
        for card in self.hand:
            if card.rank == rank:
                cards_of_rank.append(card)
        return cards_of_rank

    def discard(self, rank):
        print '!!!!!!!!'
        print self,'got a pair of',rank.name+'s!'
        self.hand = [c for c in self.hand if c.rank != rank]

    def empty(self):
        return len(self.hand) == 0
        
    def __str__(self):
        return 'Player' + str(self.id)

class ManualPlayer(Player):
    def discard(self, rank):
        print 'Congrats! You found a match in',rank
        super(ManualPlayer, self).discard(rank)

    def ask(self, opps):
        print '\nAsk away,', self
        self.display_hand()
        print [str(o) for o in opps]
        ask, opp = raw_input("RANK, OPP: ").split()
        
        rank = Rank[ask]
        opponent = [o for o in opps if o.id == int(opp)][0]

        return (rank, opponent)

class GoFish:
    def __init__(self, n):
        self.players = [Player(0), ManualPlayer(1)]
        self.deck = Deck()
        self.deal(7)
        self.winner = None

    def deal(self, n):
        for p in self.players:
            p.take(self.deck.draw(n=n))

    def play_round(self):
        for player in self.players:
            if self.winner:
                print self.winner, 'wins!!!'

            go_fish = False
            while not go_fish:
                opps = filter(lambda x: x.id != player.id,
                              self.players)
                (ask, opponent) = player.ask(opps)
                print player,'asks',opponent,'for',ask.name+'s'
                cards = opponent.respond(ask)
                if cards:
                    player.take(cards)
                    player.discard(ask)
                    if player.empty():
                        self.winner = player
                        break
                else:
                    go_fish = True
                    cards = self.deck.draw()
                    if cards:
                        print 'Go fish!\n\n'
                        player.take(cards)
                    else:
                        print 'You WOULD go fish...'

    def game_over(self):
        return self.winner

if __name__ == '__main__':
    fish = GoFish(2)
    while not fish.game_over():
        fish.play_round()
