"""
Ex2: Create a class Deck that uses a class Card . Each card has a suit (♥, ◆, ♣,
♠) and a value (A,2,3,4,5,6,7,8,9,10,J,Q,K). The deck should have a list of all possible cards (you
should use list comprehension to set this attribute). The Deck class has a method deal to deal a single
card from the deck (i.e. to remove the last card from the deck) and a method shuffle which raises a
ValueError if the deck does not have all the cards, otherwise returns the cards in a random order.
"""

import random
random.seed(7)
from player import Player

class Deck:

    suits = ["♥", "◆", "♣", "♠"]
    values = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

    def __init__(self):

        self.deck = [Card(suite, value) for suite in self.suits for value in self.values]

    def deal(self):
        return self.deck.pop()

    def shuffle(self):

        if len(self.deck) != 52:
            return ValueError

        random.shuffle(self.deck)

    def disp_deck(self):
        print([str(card) for card in self.deck])


class Card:


    def __init__(self, suite, value):

        self.suite = suite
        self.value = value

    def numeric_value(self):

        if self.value == "A":
            return 14
        elif self.value == "J":
            return 11
        elif self.value == "Q":
            return 12
        elif self.value == "K":
            return 13
        else:
            return int(self.value)

    def suite_value(self):

        if self.suite == "♥":
            return 3
        if self.suite == "◆":
            return 2
        if self.suite == "♣":
            return 1
        if self.suite == "♠":
            return 0


    def __str__(self):

        return "({}, {})".format(self.value, self.suite)


class Board:


    def __init__(self, order_players):

        self.cards = []
        self.pot = 0
        self.bet_round = {player:0 for player in order_players}

    def add_player_to_board(self, player):
        self.order_players.append(player)
        self.bet_round[player] = 0

    def remove_player_from_board(self, player):
        try:
            indx_player = self.order_players.index(player)
            del self.player_order[indx_player]
        except:
            print("The player named is not playing")

    def new_turn(self, players):

        self.cards = []
        self.pot = 0

        self.bet_round = {player:0 for player in players}


    def restart_bet_round(self, players):
        self.bet_round = {player:0 for player in players}

        # reset curent bet size for all the players
        for player in players:
            player.curr_bet_size = 0


    def _add_bet(self, player, bet_size):

        # get the player index
        self.bet_round[player] += bet_size
        self.pot += bet_size

    def _add_cards(self, card):

        self.cards.append(card)

    def disp_cards(self):
        print("Cards:", [str(card) for card in self.cards])



class Game:

    def  __init__(self, min_bet, players):
        self.deck = Deck()
        self.board = Board(players)
        self.tot_players = len(players)
        self.player_order = players
        self.players_in_round = players.copy()
        self.min_bet = min_bet


    def add_player(self, player):
        self.tot_players += 1
        self.player_order.append(player)
        # add it also to the board
        self.board.add_player_to_board(player)


    def remove_player(self, player):

        try:
            indx_player = self.player_order.index(player)
            del self.player_order[indx_player]
            self.tot_players -= 1
            self.board.remove_player_from_board(player)
        except:
            print("The player named is not playing")


    def disp_players(self):
        print(" ".join(self.player_order))

    def find_winner(self):
        # check each player against each other player
        best_player = None
        best_score = 0
        for player in self.players_in_round:

            # evalaute player1 cards
            player_tot = player.tot_hand(self.board.cards)
            # max scores will win
            if player_tot > best_score:
                best_score = player_tot
                best_player = player

        return best_player

    def deal_cards(self):

        # deal 2 cards to each player
        for i in range(2):
            for player in self.player_order:
                player.add_card(self.deck.deal())
                # player.disp_hand()


    def bet_round(self):

        i = 0
        j = 0
        while True:

            player = self.players_in_round[i]

            # display the cards as the player moves
            print("\n"*100)
            player.disp_hand()
            self.board.disp_cards() # don't show this preflop
            print("Pot size:", self.board.pot)
            # get the bet of the player
            bet = player.make_move(max(self.board.bet_round.values()), self.min_bet)
            # check if a bet has been made, if so re-set j
            if bet > max(self.board.bet_round.values()):
                j = 0

            self.board._add_bet(player, bet)

            # check if the player has folded, if so remove him
            if player.has_folded:
                del self.players_in_round[i]


            # incerease the counter
            i = (i + 1) % len(self.players_in_round)
            j += 1

            # check that there is no more betting needed
            if j >= len(self.players_in_round):
                # check if there is only one player left
                if len(self.players_in_round) == 1:
                    return True
                else:
                    return False

    def turn_cards(self, num_cards):

        # add three cards to the face up on the board
        for i in range(num_cards):
            self.board.cards.append(self.deck.deal())
            # self.board.disp_cards()
        # re initilaise values for betting round
        self.board.restart_bet_round(self.players_in_round)

    def end_turn(self, player_winner):
        # give all the money to the winner
        player_winner.tot_money += self.board.pot
        # reset the players
        for player in self.player_order:
            player._reset_hand()
            # if the player has no more chips remove him
            if player.tot_money == 0:
                self.remove_player(player)


        # change order of players as on board and get a new deck
        new_order = [self.player_order[(i+1)%len(self.player_order)] for i in range(len(self.player_order))]

        self.player_order = new_order
        self.players_in_round = new_order.copy()
        # reset the board
        self.board.new_turn(self.player_order)

        self.deck = Deck()

    def disp_standings(self):
        # disp the winning annd current state of each player
        for player in self.player_order:
            print("{} has {} chips".format(player.player_name, player.tot_money))

        cont = input("Press anything to continue")

    def play(self):

        while len(self.player_order) > 1:
            self.deck.shuffle()

            self.deal_cards()
            stop_playing = self.bet_round()
            for num in [3, 1, 1]:
                if stop_playing:
                    break
                # play the flop the turn and the river
                self.turn_cards(num)
                stop_playing = self.bet_round()


            # show hands and determine winner
            print("\n"*100)
            self.board.disp_cards()
            # only display if more than 1 players has reached the end
            if len(self.players_in_round) > 1:
                for player in self.players_in_round:
                    print("{}'s Hand:".format(player.player_name), [str(card) for card in player.hand])

            winner = self.find_winner() # turn winner
            print("Winner is", winner.player_name)

            self.end_turn(winner)
            self.disp_standings()

        print("Game ended. Winner is", self.player_order[0].player_name)




if __name__ == "__main__":


    lst_players = [Player("Emma", 100), Player("Lorenzo", 100)]

    poker = Game(10, lst_players)

    poker.play()
