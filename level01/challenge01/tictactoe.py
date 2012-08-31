#!/usr/bin/env python
import random
from collections import defaultdict


class GameBoard(object):

    def __init__(self, board_array, player):
        self._board = [r.upper() for r in board_array]
        self.rows = list()
        self.open_coordinates = list()
        self._translate_rows = defaultdict(list)
        self.player = player
        self.opponent = 'O' if player == 'X' else 'X'
        self._translate_board()

    def print_board(self):
        for i in range(len(self._board)):
            if i == 1:
                print '-----'
            print '%s|%s|%s' % tuple(self._board[i])
            if i == 1:
                print '-----'

    def block_win(self):
        """Return blocking move for an eminent win, if one exists.
        This doesn't account for being forked, but you if that happens
        you're forked already...
        """
        for (i, row) in enumerate(self.rows):
            if row.count(self.opponent) == 2:
                try:
                    bindex = row.index('_')
                    return self._translate_rows[i][bindex]
                except ValueError:
                    # We've already blocked this move
                    pass
        return None

    def victory(self):
        """Return a game winning move if there is one.  This doesn't account
        for forking your opponent, but sadly that feature is in the freezer.
        """
        for (i, row) in enumerate(self.rows):
            if row.count(self.player) == 2:
                try:
                    windex = row.index('_')
                    return self._translate_rows[i][windex]
                except ValueError:
                    # We've already blocked this move
                    pass
        return None

    def fork_you(self):
        """Try and find a forking move to make life difficult for the opponent.
        You! Yeah you! Fork You!!
        """
        # Identify the potential rows for a forking attack, and the open
        # coordinates which they hold.
        occupied_rows = list()
        for (i, row) in enumerate(self.rows):
            if self.player in row and not self.opponent in row:
                occupied_rows.append([p for p in self._translate_rows[i] if p in self.open_coordinates])

        # Find overlap in the possible fork rows
        for i in range(len(occupied_rows) - 1):
            for j in occupied_rows[i]:
                for k in occupied_rows[i+1:]:
                    if j in k:
                        return j

    def incremental_move(self):
        # This is a pretty simplistic move choice algorithm, will improve later

        # First, try to advance any existing positions that we may have which
        # hasn't been corrupted by our opponent.
        for (i, row) in enumerate(self.rows):
            if self.player in row and not self.opponent in row:
                return self._incremental_row_move(row, i)
        # We have no win advancing moves here, just choose a random open spot
        return random.choice(self.open_coordinates)

    def _incremental_row_move(self, row, row_index):
        cindex = row.index(self.player)
        if cindex in (0, 2):
            # Try and be tricky... we're on an edge so move to the opposite side
            return self._translate_rows[row_index][abs(cindex-2)]
        # We're in the middle, so cant be picky, move to either side randomly
        return self._translate_rows[row_index][random.choice([0,2])]

    def row_coordinates_at_index(self, index):
        return self._translate_rows[index]

    def _translate_board(self):
        # Horizontal
        for i in range(len(self._board)):
            self.rows.append(self._board[i])
            self._translate_rows[i] = [(i, j) for j in range(3)]

        # Vertical
        for i in range(len(self._board)):
            vert = list()
            tr_index = max(self._translate_rows)+1
            for j in range(len(self._board[i])):
                vert.append(self._board[j][i])
                self._translate_rows[tr_index].append((j, i))
            self.rows.append(vert)

        # Diagnonals
        self.rows.append([board[0][0], board[1][1], board[2][2]])
        self._translate_rows[max(self._translate_rows)+1] = [(i, i) for i in range(3)]
        self.rows.append([board[0][2], board[1][1], board[2][0]])
        self._translate_rows[max(self._translate_rows)+1] = [(0, 2), (1, 1), (2, 0)]

        # Map open coordinates
        for i in range(3):
            for j in range(3):
                if self._board[i][j] == '_':
                    self.open_coordinates.append((i, j))



# Complete the function below to print 2 integers separated by a single space which will be your next move
# Refer section <i>Output format</i> for more details
def nextMove(player, board):
    # Make sure we're dealing in caps so there's no funny business
    player = player.upper()
    gb = GameBoard(board, player)

    # The quick decision... are we about to win?
    move = None
    if gb.victory() is not None:
        #print "Returning winning move at coordinate: (%d, %d)" % gb.victory()
        move = gb.victory()

    # The next quickest decision... are we about to lose?
    if move is None and gb.block_win() is not None:
        #print "Returning blocking move at coordinate: (%d, %d)" % gb.block_win()
        move = gb.block_win()

    if move is None and gb.fork_you() is not None:
        #print "Returning a forking move at coordinate: (%d, %d)" % move
        move = gb.fork_you()

    # We're not about to win and we're not about to lose, so make a move...
    if move is None:
        move = gb.incremental_move()
    #print "Returning incremental move at coordinate: (%d, %d)" % move

    # Channenge requires returning the move as integers printed to screen
    print '%d %d' % move


#If player is X, I'm the first player.
#If player is O, I'm the second player.
player = raw_input()
#board = ['___', '___', '___']
# Read the board now. The board is a 3x3 array filled with X, O or _.
board = list()
for i in xrange(0, 3):
    board.append(raw_input())

nextMove(player,board);
