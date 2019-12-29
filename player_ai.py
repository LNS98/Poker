import random

class Player:


    def __init__(self, player_name, intial_bank):
        self.player_name = player_name
        self.hand = []
        self.tot_money = intial_bank
        self.curr_bet_size = 0
        self.has_folded = False

    def add_card(self, card):
        self.hand.append(card)


    def _make_bet(self, bet_amount, min_bet):

        # allowed to bet
        if self.tot_money - bet_amount >= 0 and bet_amount >= min_bet:
            self.tot_money -= bet_amount
            # make a class attribute to store current bet size
            self.curr_bet_size = bet_amount

            return True
        else:
            print("Bet size to big or under the minimum")
            print("Min bet size: {}".format(min_bet))
            print("Your total chips is {}".format(self.tot_money))
            return False

    def _make_call(self, bet_amount, min_bet):

        # allowed to bet
        if self.tot_money - bet_amount > 0:
            self.tot_money -= bet_amount
            # make a class attribute to store current bet size
            self.curr_bet_size = bet_amount
            return True
        elif self.tot_money - bet_amount <= 0:
            # make a class attribute to store current bet size
            self.curr_bet_size = self.tot_money
            self.tot_money = 0
            return "all_in"

        else:
            print("Bet size to big or under the minimum")
            print("Min bet size: {}".format(min_bet))
            print("Your total chips is {}".format(self.tot_money))
            return False

    def tot_hand(self, board_cards):

        # create a 13x4 array with all 0s
        cards_array = [[0 for i in range(13)] for i in range(4)]
        all_cards = board_cards + self.hand

        # fill the scores array
        for card in all_cards:
            row, col = card.numeric_value()-2, card.suite_value()
            cards_array[col][row] += 1

        same_card = [sum(cards_array[j][i] for j in range(4)) for i in range(13)]

        # get an estimate of stregnth of the card
        value = sum(10*(same_card[i])**3 + (same_card[i])*i for i in range(len(same_card)))

        return value


    def _reset_hand(self):
        self.hand = []
        self.has_folded = False
        self.curr_bet_size = 0



class PlayerRandom(Player):

    def __init__(self, player_name, inital_bank):
        super().__init__(player_name, inital_bank)

    def disp_hand(self):
        # the AI will not show cards as it can remeber them
        return None

    def make_move(self, highest_raise, min_bet):

        # check to see if the moved type is valid
        valid_move = False

        while not valid_move:
            # see if it has to bet, check or fold, call, raise
            if highest_raise == 0:

                # choose randomly between [check, bet]
                move = random.choice(["check", "bet"])

                if move == "bet":
                    # choose randomly an amount between min bet size and its total money
                    bet_amount = random.choice([x for x in range(int(min_bet), int(self.tot_money), 10)])
                    valid_move = self._make_bet(bet_amount, min_bet)

                else:
                    bet_amount = 0
                    valid_move = True
            else:
                # choose randomly between [check, bet]
                move = random.choice(["fold", "call", "raise"])

                if move == "fold":
                    bet_amount = 0
                elif move == "call":
                    bet_amount = highest_raise - self.curr_bet_size
                    valid_move = self._make_call(bet_amount, min_bet)
                else:
                    # choose randomly an amount between min bet size and its total money
                    bet_amount = random.choice([x for x in range(int(min_bet), int(self.tot_money), 10)])
                    valid_move = self._make_bet(bet_amount, highest_raise + min_bet)

            return bet_amount




class PlayerHuman(Player):


    def __init__(self, player_name, intial_bank):
        super().__init__(player_name, intial_bank)

    def disp_hand(self):
        show = input("{}, would you like to see your cards? (type 'yes' or 'no')".format(self.player_name))
        if show == "yes":
            print("\n" * 100)
            print("{}'s Hand:".format(self.player_name), [str(card) for card in self.hand])
            finished = input("Press Enter when finished")
            print("\n" * 100)

    def make_move(self, highest_raise, min_bet):

        # check to see if the moved type is valid
        valid_move = False

        while not valid_move:
            # check if he is allowed to check, bet or if someone has already betted
            if highest_raise == 0:
                # check if the moved type is valid
                    move = input("{}, would you like to check, bet? ".format(self.player_name))

                    if move == "check":
                        valid_move = True
                        bet_amount = 0

                    elif move == "bet":
                        try:
                            bet_amount = float(input("How much would you like to bet?"))
                            valid_move = self._make_bet(bet_amount, min_bet)
                        except:
                            print("Must type an number")

                    else:
                        print("The move selected is not valid")
                        print("Please type 'check' or 'bet'")

            else:
                    move = input("{}, would you like to fold, call, raise? ".format(self.player_name))

                    if move == "fold":
                        self.has_folded = True
                        valid_move = True
                        bet_amount = 0
                    elif move == "call":
                        bet_amount = highest_raise - self.curr_bet_size
                        valid_move = self._make_call(bet_amount, min_bet)
                        # check if player is all in
                        if valid_move == "all_in":
                            bet_amount = self.curr_bet_size
                            valid_move = True

                    elif move == "raise":
                        try:
                            bet_amount = float(input("How much would you like to raise?"))
                            valid_move = self._make_bet(bet_amount, highest_raise + min_bet)
                        except:
                            print("Must type an number")

                    else:
                        print("The move selected is not valid")
                        print("Please type 'fold', 'call' or 'raise'")

        return bet_amount
