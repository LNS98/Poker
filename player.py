# class Player:
#
#
#     def __init__(self, player_name, intial_bank):
#         self.player_name = player_name
#         self.hand = []
#         self.tot_money = intial_bank
#         self.curr_bet_size = 0
#         self.has_folded = False
#
#     def add_card(self, card):
#         self.hand.append(card)
#
#
#     def _make_bet(self, bet_amount, min_bet):
#
#         # allowed to bet
#         if self.tot_money - bet_amount >= 0 and bet_amount >= min_bet:
#             self.tot_money -= bet_amount
#             # make a class attribute to store current bet size
#             self.curr_bet_size = bet_amount
#             return True
#         else:
#             print("Bet size to big or under the minimum")
#             print("Min bet size: {}".format(min_bet))
#             print("Your total chips is {}".format(self.tot_money))
#             return False
#
#     def _make_call(self, bet_amount, min_bet):
#
#         # allowed to bet
#         if self.tot_money - bet_amount >= 0 and bet_amount >= min_bet:
#             self.tot_money -= bet_amount
#             # make a class attribute to store current bet size
#             self.curr_bet_size = bet_amount
#             return True
#         else:
#             print("Bet size to big or under the minimum")
#             print("Min bet size: {}".format(min_bet))
#             print("Your total chips is {}".format(self.tot_money))
#             return False
#
#
#     def tot_hand(self, board_cards):
#
#         # create a 13x4 array with all 0s
#         cards_array = [[0 for i in range(13)] for i in range(4)]
#         all_cards = board_cards + self.hand
#
#         # fill the scores array
#         for card in all_cards:
#             row, col = card.numeric_value()-2, card.suite_value()
#             cards_array[col][row] += 1
#
#         same_card = [sum(cards_array[j][i] for j in range(4)) for i in range(13)]
#
#         # get an estimate of stregnth of the card
#         value = sum(10*(same_card[i])**3 + (same_card[i])*i for i in range(len(same_card)))
#
#         return value
#
#
#     def _reset_hand(self):
#         self.hand = []
#         self.has_folded = False
#         self.curr_bet_size = 0
#
#


class Player:


    def __init__(self, player_name, intial_bank):
        self.player_name = player_name
        self.hand = []
        self.tot_money = intial_bank
        self.curr_bet_size = 0
        self.has_folded = False

    def add_card(self, card):
        self.hand.append(card)

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

        # check if he is allowed to check, bet or if someone has already betted
        if highest_raise == 0:
            # check if the moved type is valid
            while not valid_move:
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

            while not valid_move:
                move = input("{}, would you like to fold, call, raise? ".format(self.player_name))

                if move == "fold":
                    self.has_folded = True
                    valid_move = True
                    bet_amount = 0
                elif move == "call":
                    bet_amount = highest_raise - self.curr_bet_size
                    valid_move = self._make_bet(bet_amount, min_bet)

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
