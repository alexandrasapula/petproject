import random


class Shoe:
    def __init__(self, num_decks=4):
        self.num_decks = num_decks
        self.cards = self.create_shoe()
        self.shuffle()

    def create_shoe(self):
        suits = ["Hearts", "Diamands", "Clubs", "Spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        deck = [{"rank": rank, "suit": suit} for suit in suits for rank in ranks]
        return deck * self.num_decks

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if len(self.cards) < 20:
            self.reset()
        return self.cards.pop()

    def reset(self):
        self.cards = self.create_shoe()
        self.shuffle()
