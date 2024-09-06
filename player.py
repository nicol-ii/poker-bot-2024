'''
Simple example pokerbot, written in Python.

Variation of Texas Hold 'Em Poker 
- postflop, players bet on a third hand card
- the winning bid is added to the pot and winning player is awarded a third card

Main notes:
- generally, we used Texas Hold Ranges preflop, Monte Carlo sims postflop, and random elements based on opponent aggression 
- preflop is hard coded on Texas Hold ranges
- preflop also helps determine opp aggression
- immediate postflop run Monte Carlo (size=200) to determine hand strength
- value of winning bid is 2x preflop pot: calculate bid
'''

TABLE = {'AA': 85, 'KK': 83, 'QQ': 80, 'JJ': 78, 'TT': 75, '99': 72, '88': 69,
         '77': 67, '66': 64, '55': 61, '44': 58, '33': 55, '22': 51,
         'AK': 66, 'AQ': 65, 'AJ': 65, 'AT': 64, '9A': 62, '8A': 61, '7A': 60,
         '6A': 59, '5A': 60, '4A': 59, '3A': 58, '2A': 57,
         'KQ': 62, 'JK': 62, 'KT': 61, '9K': 59, '8K': 58, '7K': 57, '6K': 56,
         '5K': 55, '4K': 54, '3K': 54, '2K': 53,
         'JQ': 59, 'QT': 59, '9Q': 57, '8Q': 55, '7Q': 54, '6Q': 53, '5Q': 52,
         '4Q': 51, '3Q': 50, '2Q': 49,
         'JT': 57, '9J': 55, '8J': 53, '7J': 52, '6J': 50, '5J': 49, '4J': 48,
         '3J': 48, '2J': 47,
         'T9': 53, 'T8': 52, 'T7': 50, 'T6': 48, 'T5': 47, 'T4': 46, 'T3': 45,
         'T2': 44,
         '89': 50, '79': 48, '69': 47, '59': 45, '49': 43, '39': 43, '29': 42,
         '78': 47, '68': 46, '58': 44, '48': 42, '38': 40, '28': 40,
         '67': 45, '57': 43, '47': 41, '37': 39, '27': 37,
         '56': 43, '46': 41, '36': 39, '26': 37,
         '45': 41, '35': 39, '25': 37,
         '34': 38, '24': 36,
         '23': 35}

TABLE2 = {'AA': 169, 'AKs': 164, 'AQs': 162, 'AJs': 160, 'ATs': 157, 'A9s': 150, 'A8s': 147, 'A7s': 145, 'A6s': 140, 'A5s': 142, 'A4s': 136, 'A3s': 134, 'A2s': 130,
          'AK': 163, 'KK': 168,  'KQs': 155, 'KJs': 153, 'KTs': 149, 'K9s': 137, 'K8s': 129, 'K7s': 126, 'K6s': 122, 'K5s': 116, 'K4s': 110, 'K3s': 105, 'K2s': 104,
          'AQ': 159, 'KQ': 151,  'QQ': 167,  'QJs': 146, 'QTs': 143, 'Q9s': 131, 'Q8s': 119, 'Q7s': 108, 'Q6s': 107, 'Q5s': 96,  'Q4s': 92,  'Q3s': 85,  'Q2s': 79,
          'AJ': 156, 'KJ': 144,  'QJ': 132,  'JJ': 166,  'JTs': 139, 'J9s': 128, 'J8s': 115, 'J7s': 102, 'J6s': 90,  'J5s': 81,  'J4s': 75,  'J3s': 71,  'J2s': 61,
          'AT': 152, 'KT': 135,  'QT': 126,  'JT': 120,  'TT': 165,  'T9s': 125, 'T8s': 114, 'T7s': 99,  'T6s': 86,  'T5s': 66,  'T4s': 58,  'T3s': 56,  'T2s': 50,
          'A9': 141, 'K9': 118,  'Q9': 106,  'J9': 100,  'T9': 97,   '99': 161,  '98s': 111, '97s': 95,  '96s': 83,  '95s': 68,  '94s': 49,  '93s': 43,  '92s': 39,
          'A8': 133, 'K8': 101,  'Q8': 89,   'J8': 82,   'T8': 80,   '98': 78,   '88': 158,  '87s': 98,  '86s': 88,  '85s': 67,  '84s': 51,  '83s': 33,  '82s': 28,
          'A7': 123, 'K7': 94,   'Q7': 74,   'J7': 69,   'T7': 65,   '97': 60,   '87': 63,   '77': 154,  '76s': 87,  '75s': 73,  '74s': 55,  '73s': 35,  '72s': 20,
          'A6': 117, 'K6': 91,   'Q6': 72,   'J6': 52,   'T6': 48,   '96': 42,   '86': 45,   '76': 53,   '66': 148,  '65s': 76,  '64s': 57,  '63s': 40,  '62s': 22,
          'A5': 121, 'K5': 84,   'Q5': 59,   'J5': 44,   'T5': 29,   '95': 27,   '85': 30,   '75': 34,   '65': 38,   '55': 138,  '54s': 62,  '53s': 47,  '52s': 32,
          'A4': 113, 'K4': 77,   'Q4': 54,   'J4': 36,   'T4': 23,   '94': 13,   '84': 16,   '74': 17,   '64': 21,   '54': 26,   '44': 127,  '43s': 37,  '42s': 24,
          'A3': 109, 'K3': 70,   'Q3': 46,   'J3': 31,   'T3': 18,   '93': 12,   '83': 7,    '73': 8,    '63': 10,   '53': 14,   '43': 11,   '33': 112,  '32s': 19,
          'A2': 103, 'K2': 64,   'Q2': 41,   'J2': 25,   'T2': 15,   '92': 9,    '82': 5,    '72': 2,    '62': 3,    '52': 6,    '42': 4,    '32': 1,    '22': 93}

from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction, BidAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot
from collections import deque
import random
import eval7



class Player(Bot):
    '''
    A pokerbot.
    '''
    flops_reached = 0 # start tracking the number of flops reached past round 50
    flops_small_bets = 0 # tracking the number of bets between 1/8 and 1/2 pot, inclusive
    flops_large_bets = 0 # tracking the number of bets between 1/2 and pot, inclusive
    flops_overbets = 0 # tracking the number of bets greater than pot


    opp_preflop_range = 100
    opp_range = 100
    my_preflop_range = 100
    prev_bids = deque()
    prev_bids_sum = 0
    prev_action = 0 # 0 = check, 1 = call, 2 = bet/raise
    opp_aggressiveness = 0 # postflop changes: check -10; call -5; bet +(30 * percentage of pot); raise +(30 * percentage of pot + 15)
    dealer = False



    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.

        Arguments:
        Nothing.

        Returns:
        Nothing.
        '''
        pass

    def get_string(self, hole):
        cardvalues = [hole[0][0], hole[1][0]]
        card1suit = hole[0][1]
        card2suit = hole[1][1]
        tempstring = cardvalues[0] + cardvalues[1]
        if tempstring not in TABLE2:
            tempstring = cardvalues[1] + cardvalues[0]

        if card1suit == card2suit:
            return (tempstring + 's')
        else:
            return (tempstring)


    def calc_strength(self, hole, iters, community, won_bid, opp_range):
        '''
        Using MC with iterations to evalute hand strength
        Args:
        hole - our hole cards
        iters - number of times we run MC
        community - community cards
        won_bid - whether we won the auction or not
        '''
        deck = eval7.Deck() # deck of cards
        hole_cards = [eval7.Card(card) for card in hole] # our hole cards in eval7 friendly format


        # If the community cards are not empty, we need to remove them from the deck
        # because we don't want to draw them again in the MC

        community_cards = [eval7.Card(card) for card in community]
        for card in community_cards: #removing the current community cards from the deck
            deck.cards.remove(card)

        for card in hole_cards: #removing our hole cards from the deck
            deck.cards.remove(card)

        #the score is the number of times we win, tie, or lose
        score = 0
        valid_iters = 0

        for _ in range(iters): # MC the probability of winning
            deck.shuffle()

            #Let's see how many community cards we still need to draw
            _COMM = 5 - len(community) # number of community cards we need to draw

            _OPP = 2

            draw = deck.peek(_COMM + _OPP + 2)
            hole_new = hole_cards.copy()
            opp_hole = draw[0:_OPP]

            opp_hole_str = [str(opp_hole[0]), str(opp_hole[1])]
            opp_hole_strength = TABLE2[self.get_string(opp_hole_str)]
            if opp_hole_strength <= (100 - opp_range) * 1.69:
                continue

            valid_iters += 1

            alt_community = draw[_OPP:len(draw) - 2] # the community cards that we draw in the MC
            extra_card_2 = draw[-1]

            # won_bid = 0: we win, 1: they win, 2: tie
            if won_bid != 0:
                opp_hole.append(extra_card_2)

            if community == []: # if there are no community cards, we only need to compare our hand to the opp hand
                our_hand = hole_new  + alt_community
                opp_hand = opp_hole  + alt_community
            else:
                our_hand = hole_new + community_cards + alt_community
                opp_hand = opp_hole + community_cards + alt_community


            our_hand_value = eval7.evaluate(our_hand)
            opp_hand_value = eval7.evaluate(opp_hand)

            if our_hand_value > opp_hand_value:
                score += 2
            if our_hand_value == opp_hand_value:
                score += 1

        hand_strength = score/ (2 * valid_iters) # win probability

        return hand_strength

    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        my_cards = round_state.hands[active]  # your cards
        big_blind = bool(active)  # True if you are the big blind

        self.dealer = not big_blind
        self.opp_preflop_range = 100
        self.opp_range = 100
        self.my_preflop_range = 100
        self.my_range = 100
        self.opp_aggressiveness = 50
        self.prev_action = 0

    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        terminal_state: the TerminalState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        #my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        #previous_state = terminal_state.previous_state  # RoundState before payoffs
        #street = previous_state.street  # 0, 3, 4, or 5 representing when this round ended
        #my_cards = previous_state.hands[active]  # your cards
        #opp_cards = previous_state.hands[1-active]  # opponent's cards or [] if not revealed
        pass

    def get_action(self, game_state, round_state, active):
        '''
        Where the magic happens - your code should implement this function.
        Called any time the engine needs an action from your bot.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Your action.
        '''
        # May be useful, but you may choose to not use.
        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        street = round_state.street  # 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        my_cards = round_state.hands[active]  # your cards
        board_cards = round_state.deck[:street]  # the board cards
        my_pip = round_state.pips[active]  # the number of chips you have contributed to the pot this round of betting
        opp_pip = round_state.pips[1-active]  # the number of chips your opponent has contributed to the pot this round of betting
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        my_bid = round_state.bids[active]  # How much you bid previously (available only after auction)
        opp_bid = round_state.bids[1-active]  # How much opponent bid previously (available only after auction)
        continue_cost = opp_pip - my_pip  # the number of chips needed to stay in the pot
        my_contribution = STARTING_STACK - my_stack  # the number of chips you have contributed to the pot
        opp_contribution = STARTING_STACK - opp_stack  # the number of chips your opponent has contributed to the pot

        _MONTE_CARLO_ITERS = 600

        my_action = None

        min_raise, max_raise = round_state.raise_bounds()
        pot_total = my_contribution + opp_contribution
        bet_percent = continue_cost / (pot_total - continue_cost)

        # fold when we're ahead
        if (game_state.bankroll - my_contribution > (1.5 * (NUM_ROUNDS - game_state.round_num)) + 1):
            if BidAction in legal_actions:
                return BidAction(0)
            if FoldAction in legal_actions:
                return FoldAction()
            return CheckAction()

        # preflop logic
        if street == 0:
            starting_strength = TABLE2[self.get_string(my_cards)]
            if my_pip == 1: # first to act in the dealer
                if starting_strength >= 0.2 * 169:
                    self.my_preflop_range = 80
                    if RaiseAction in legal_actions:
                        self.opp_preflop_range = 50 + random.randint(0, 10)
                        return RaiseAction(7)
                    return CallAction()
                return FoldAction()
            if continue_cost == 0: # limped to us in big blind
                if starting_strength >= 0.2 * 169:
                    self.my_preflop_range = 80
                    if RaiseAction in legal_actions:
                        self.opp_preflop_range = 50 + random.randint(0, 10)
                        return RaiseAction(9)
                    return CallAction
                return CheckAction()
            if continue_cost <= 12: # usually raised once to us in the big blind
                self.opp_preflop_range = 75 + random.randint(0, 10)
                if starting_strength >= 0.45 * 169:
                    self.my_preflop_range = 55
                    if RaiseAction in legal_actions:
                        if starting_strength >= 0.8 * 169:
                            self.my_preflop_range = 20
                            self.opp_preflop_range = 22 + random.randint(0, 6)
                            return RaiseAction(min(3 * (opp_pip), max_raise))
                        return CallAction()
                    else:
                        return CallAction()
                return FoldAction()
            if continue_cost <= 30: # usually 3 bet to us in the dealer
                self.opp_preflop_range = 22 + random.randint(0, 6)
                if starting_strength >= 0.8 * 169:
                    self.my_preflop_range = 20
                    if RaiseAction in legal_actions:
                        if starting_strength >= 0.9 * 169:
                            self.my_preflop_range = 10
                            self.opp_preflop_range = 11 + random.randint(0, 2)
                            return RaiseAction(min(int(2.5 * (opp_pip)), max_raise))
                        return CallAction()
                    return CallAction()
                return FoldAction()
            else: # 4 bet or more
                self.opp_preflop_range = 11 + random.randint(0, 2)
                if starting_strength >= 0.9 * 169:
                    self.my_preflop_range = 10
                    return CallAction()
                return FoldAction()

        if BidAction in legal_actions:
            opp_bid_percent_average = self.prev_bids_sum / max(len(self.prev_bids), 1)
            opp_bid_average = opp_bid_percent_average * pot_total
            if opp_bid_average > min(2 * pot_total, 150):
                return BidAction(min(int(opp_bid_average * 0.8), 150, my_stack))
            else:
                return BidAction(min(int(random.uniform(1.8, 2.2) * pot_total), 150, my_stack))

        if street == 3 and my_pip == 0:
            opp_bid_percent = opp_bid / (2 * min(my_contribution, opp_contribution - opp_pip))
            if opp_bid_percent > 0:
                if len(self.prev_bids) < 5:
                    self.prev_bids.append(opp_bid_percent)
                    self.prev_bids_sum += opp_bid_percent
                else:
                    self.prev_bids.append(opp_bid_percent)
                    self.prev_bids_sum += opp_bid_percent
                    old_bid_percent = self.prev_bids.popleft()
                    self.prev_bids_sum -= old_bid_percent

        if my_bid > opp_bid:
            won_bid = 0
        elif my_bid == opp_bid:
            won_bid = 1
        else:
            won_bid = 2

        if continue_cost > 0:
            if my_pip == 0:
                opp_action = 2 # opp bet
            else:
                opp_action = 3 # opp raised
        if continue_cost == 0:
            if self.dealer:
                opp_action = 0 # opp checked
            else: # new street
                if self.prev_action == 0 or self.prev_action == 1: # we checked or called last street to end action
                    opp_action = 4 # already factored in their previous action
                else: # we bet or raised last street, opponent must have ended action
                    opp_action = 1

        # update aggressiveness based on opponent action
        if opp_action == 0:
            self.opp_aggressiveness -= 15
        if opp_action == 1:
            self.opp_range *= 0.6
        if opp_action == 2:
            self.opp_range *= max(0.7, 1 - bet_percent / 2)
            self.opp_aggressiveness += 15 * bet_percent + 15
        if opp_action == 3:
            self.opp_range *= max(0.7, 1 - bet_percent)
            self.opp_aggressiveness += 20 * bet_percent + 25

        aggressiveness_scaled = min(max(self.opp_aggressiveness, -50), 75)

        range_bluff = self.opp_range * (continue_cost / pot_total) * (0.7 + (-aggressiveness_scaled + 75) / 125)

        # raise logic
        if continue_cost == 0:
            raise_amount = int(0.03 * street * street * pot_total)
        else:
            if continue_cost > 50:
                raise_amount = max(int(opp_pip * 2.7), int(0.03 * street * street * (pot_total - continue_cost)), int(0.5 * (pot_total - continue_cost)))
            else:
                raise_amount = max(int(opp_pip * 3.2), int(0.03 * street * street * (pot_total - continue_cost)), int(0.5 * (pot_total - continue_cost)))
        if won_bid == 0: # we won the bid, raise larger than normal
            raise_amount = int (raise_amount * 1.15)
        if won_bid == 1: # we lost the bid, raise smaller than normal
            raise_amount = int (raise_amount * 0.85)

        # # ensure raises are legal
        raise_amount = max([min_raise, raise_amount]) #getting the max of the min raise and the raise amount
        raise_amount = min([max_raise, raise_amount]) #getting the min of the max raise and the raise amount
        # # we want to do this so that we don't raise more than the max raise or less than the min raise

        if RaiseAction in legal_actions:
            aggressive_action = RaiseAction(raise_amount)
        elif CallAction in legal_actions:
            aggressive_action = CallAction()
        elif CheckAction in legal_actions:
            aggressive_action = CheckAction()

        if CheckAction in legal_actions:
            passive_action = CheckAction()
        else:
            passive_action = CallAction()

        if FoldAction in legal_actions:
            give_up = FoldAction()
        else:
            give_up = CheckAction()

        #running monte carlo simulation when we have community cards vs when we don't
        raw_strength = self.calc_strength(my_cards, _MONTE_CARLO_ITERS, board_cards, won_bid, self.opp_preflop_range)

        pot_odds = float(continue_cost/(pot_total + continue_cost))
        strength = (max(0, (raw_strength * 100 - (100 - self.opp_range))) + min(range_bluff, max(raw_strength * 100 - 50, 0))) / (self.opp_range + range_bluff)
        if street != 5:
            if self.dealer:
                if won_bid == 0:
                    if strength >= pot_odds * 0.8:
                        if strength > 0.6:
                            my_action = aggressive_action
                        else:
                            my_action = passive_action
                    elif aggressiveness_scaled <= 0:
                        bluff_chance = 0.5
                        if random.random() < bluff_chance:
                            my_action = aggressive_action
                    else:
                        my_action = give_up
                else:
                    if strength >= pot_odds * 0.8:
                        if strength > 0.8 and random.random() < strength:
                            my_action = aggressive_action
                        else:
                            my_action = passive_action
                    elif aggressiveness_scaled <= 0:
                        bluff_chance = 0.1
                        if random.random() < bluff_chance:
                            my_action = aggressive_action
                    else:
                        my_action = give_up
            else:
                if won_bid == 0:
                    if strength >= pot_odds * 0.8:
                        if strength > 0.7:
                            my_action = aggressive_action
                        else:
                            my_action = passive_action
                    elif aggressiveness_scaled <= 0:
                        bluff_chance = 0.4
                        if random.random() < bluff_chance:
                            my_action = aggressive_action
                    else:
                        my_action = give_up
                else:
                    if strength >= pot_odds * 0.8:
                        if strength > 0.8 and random.random() < strength:
                            my_action = aggressive_action
                        else:
                            my_action = passive_action
                    elif aggressiveness_scaled <= 0:
                        bluff_chance = 0.1
                        if random.random() < bluff_chance:
                            my_action = aggressive_action
                    else:
                        my_action = give_up
        else:
            if strength >= pot_odds:
                if strength > 0.9:
                    my_action = aggressive_action
                if strength > 0.7 and random.random() < strength:
                    my_action = aggressive_action
                else:
                    my_action = passive_action
            else:
                my_action = give_up

        # update our previous action
        if isinstance(my_action, RaiseAction):
            self.prev_action = 2
        if isinstance(my_action, CallAction):
            self.prev_action = 1
        if isinstance(my_action, CheckAction):
            self.prev_action = 0
        return my_action


if __name__ == '__main__':
    run_bot(Player(), parse_args())
