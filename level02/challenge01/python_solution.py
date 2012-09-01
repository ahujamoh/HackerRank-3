#!/bin/python
"""
The seed code provided by HackerRank
#!/bin/python

def calculate_bid(player,pos,first_moves,second_moves):
    #your logic here
    return 0

#gets the id of the player
player = input()

scotch_pos = input()         #current position of the scotch

first_moves = [int(i) for i in raw_input().split()]
second_moves = [int(i) for i in raw_input().split()]
bid = calculate_bid(player,scotch_pos,first_moves,second_moves)
print bid
"""
import random


class GameBoard(object):

    def __init__(self, position):
        self.update_board(position)
        self.board_length = 11
        self.board = range(self.board_length)
        self.board[self.position] = 'SS'

    def update_board(self, position):
        self.position = position

    def player_one_distance(self):
        return self.position

    def player_two_distance(self):
        return self.board_length - self.position - 1

    def __str__(self):
        front = '%02d-'*len(self.board[:self.position])
        back = '%02d-'*len(self.board[self.position+1:])
        return '%s-SS-%s' % (front.strip('-') % tuple(self.board[:self.position]),
                             back.strip('-') % tuple(self.board[self.position+1:]))

class Player(object):

    def __init__(self, player_num, board, bids, record):
        self.bids = bids
        self.balance = 100
        self.board = board
        self.player_number = player_num
        for (i, m) in enumerate(self.bids):
            if record[i].upper() == 'W':
                self.balance -= m

    def update_board(self, position):
        self.board.update_board(position)

    def print_board(self):
        print str(self.board)

    def distance(self):
        p = 'one' if self.player_number == 1 else 'two'
        func = getattr(self.board, 'player_%s_distance' % p)
        return func()

def print_config(label, player, opponent):
    print ''
    print '%s Board Configuration:' % label
    player.print_board()
    print '%s Distances:' % label
    print '    Player distance: %d' % player.distance()
    print '    Opponent distance: %d' % opponent.distance()

def win_loss(player, opponent):
    record = list()
    ties = 0
    if not isinstance(player, list):
        player = player.bids
        opponent = opponent.bids
    for (i, bid) in enumerate(player):
        if bid > opponent[i]:
            record.append('W')
        elif bid < opponent[i]:
            record.append('L')
        else:
            ties += 1
            if ties % 2 == 0:
                r = 'W' if player.player_number == 2 else 'L'
            else:
                r = 'L' if player.player_number == 2 else 'W'
            record.append(r)
    return record

def post_win_average(opponent, records):
    return post_outcome_average(opponent, records, 'W')

def post_loss_average(opponent, records):
    return post_outcome_average(opponent, records, 'L')

def post_outcome_average(opponent, records, outcome):
    l = list()
    for (i, o) in enumerate(records):
        if o == outcome.upper():
            try:
                l.append(opponent.bids[i+1])
            except IndexError:
                pass

    if not len(l):
        return -1
    elif len(l) == 1:
        return l[0]
    return sum(l)/float(len(l))

def leading_bid(player, opponent):
    try:
        last_outcome = win_loss(player, opponent)[-1]
        op_avg_for_outcome = post_outcome_average(opponent, last_outcome, last_outcome)
    except IndexError:
        op_avg_for_outcome = -1
    #print 'Average: %d' % op_avg_for_outcome
    if opponent.balance > player.balance:
        # We're behind in funds
        # Try to draw them out of funds
        rand_bid = random.randint(1, 5)
        while rand_bid > player.balance:
            rand_bid = random.randint(1, 5)
        return rand_bid

    elif opponent.balance < player.balance:
        # We're ahead in funds
        const_drain = opponent.balance/player.distance()
        if op_avg_for_outcome != -1 and const_drain < op_avg_for_outcome:
            if player.balance/op_avg_for_outcome >= player.distance():
                return op_avg_for_outcome + 1
        return const_drain

    else:
        # We have equal amounts of cash
        if op_avg_for_outcome != -1:
            if player.balance/op_avg_for_outcome >= player.distance():
                return op_avg_for_outcome + 1
            else:
                for p in range(op_avg_for_outcome, 0, -1):
                    if player.balance/p >= player.distance():
                        return p
        rand_bid = random.randint(1, 5)
        while rand_bid > player.balance:
            rand_bid = random.randint(1, 5)
        return rand_bid


def trailing_bid(player, opponent):
    last_outcome = win_loss(player, opponent)[-1]
    if opponent.balance > player.balance:
        # We're behind in funds
        pass
    elif opponent.balance < player.balance:
        # We're ahead in funds
        pass
    else:
        # We have equal amounts of cash
        pass


def calculate_bid(pnum, pos, first_bids, second_bids):
    bid = None
    onum = 2 if pnum == 1 else 1

    board = GameBoard(pos)
    pbids = first_bids if pnum == 1 else second_bids
    obids = first_bids if onum == 1 else second_bids

    precord = win_loss(pbids, obids)
    orecord = list()
    for r in precord:
        if r == 'W':
            orecord.append('L')
        else:
            orecord.append('W')

    player = Player(pnum, board, pbids, precord)
    opponent = Player(onum, board, obids, orecord)

    #print_config('Starting', player, opponent)

    if player.distance < opponent.distance:
        #bid = trailing_bid(player, opponent)
        bid = leading_bid(player, opponent)

    elif player.distance > opponent.distance:
        bid = leading_bid(player, opponent)

    else:
        # This is either th first bid or we've returned to tie state
        bid = random.randint(1, 5)


    return bid


player = input()
player = int(player)

scotch_pos = input()                 #current position of the scotch
scotch_pos = int(scotch_pos)         #current position of the scotch

first_bids = [int(i) for i in raw_input().split()]
second_bids = [int(i) for i in raw_input().split()]
bid = calculate_bid(player, scotch_pos, first_bids, second_bids)
print bid
