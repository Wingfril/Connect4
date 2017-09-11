# Name: Ziyan Mo
# CMS cluster login name: Zmo

'''
final_board.py

This module contains classes that implement the Connect-4 board object.
'''

# Imports go here...
import copy

class MoveError(Exception):
    '''
    Instances of this class are exceptions which are raised when
    an invalid move is made.
    '''
    pass

class BoardError(Exception):
    '''
    Instances of this class are exceptions which are raised when
    some erroneous condition relating to a Connect-Four board occurs.
    '''
    pass

class Connect4Board:
    '''
    Instance of this class manage a Connect-Four board, but do not
    manage the play of the game itself.
    '''

    def __init__(self):
        '''
        Initialize the board.
        '''
        self.board =  [[0 for x in range(7)] for y in range(6)] 
        self.rowlisting = [0, 0, 0, 0, 0, 0, 0]
        self.row = 6
        self.col = 7

    def getRows(self):
        '''
        Return the number of rows.
        '''

        return self.row

    def getCols(self):
        '''
        Return the number of columns.
        '''
        return self.col

    def get(self, row, col):
        '''
        Arguments:
          row -- a valid row index
          col -- a valid column index

        Return value: the board value at (row, col).

        Raise a BoardError exception if the 'row' or 'col' value is invalid.
        '''
        
        if row < 0 or row > 5:
            raise BoardError('The row you requested is invalid')
        elif col < 0 or col > 6:
            raise BoardError('The column you requested is invalid')
        return self.board[row][col]
 

    def clone(self):
        '''
        Return a clone of this board i.e. a new instance of this class
        such that changing the fields of the new instance will not
        affect the old instance.

        Return value: the new Connect4Board instance.
        '''
        return copy.deepcopy(self)
        

    def possibleMoves(self):
        '''
        Compute the list of possible moves (i.e. a list of column numbers 
        corresponding to the columns which are not completely filled up).

        Return value: the list of possible moves
        '''
        moves = []
        for i in range(self.col):
            if self.rowlisting[i] < 6:
                moves.append(i)
        return moves      

    def makeMove(self, col, player):
        '''
        Make a move on the specified column for the specified player.

        Arguments:
          col    -- a valid column index
          player -- either 1 or 2

        Return value: none

        Raise a MoveError exception if a move cannot be made because the column
        is filled up, or if the column index or player number is invalid.
        '''
        if player != 1 and player != 2:
            raise MoveError('Invalid player')
        elif col < 0 or col > 6:
            raise MoveError('Invalid move: that column is unrecognized')
        elif col not in self.possibleMoves():
            raise MoveError('Invalid move: that column is full')
        else:
               
            temprow = self.rowlisting[col]
            self.board[temprow][col] = player           
            self.rowlisting[col] += 1


    def unmakeMove(self, col):
        '''
        Unmake the last move made on the specified column.

        Arguments:
          col -- a valid column index

        Return value: none

        Raise a MoveError exception if there is no move to unmake, or if the
        column index is invalid.
        '''
            
        if type(col) != int:
            raise MoveError('Unknown column; column must be an int')
        if col < 0 or col > 6:
            raise MoveError('Unknown column; column must be 0-6')
        elif self.rowlisting[col] == 0:
            raise MoveError('Cannot undo empty column')
        elif col < 7 and col >= 0:               
            self.board[self.rowlisting[col]-1][col] = 0     
            self.rowlisting[col] -= 1
                


    def isWin(self, col):
        '''
        Check to see if the last move played in column 'col' resulted in a win
        (four or more discs of the same color in a row in any direction).

        Argument: 
          col    -- a valid column index

        Return value: True if there is a win, else False

        Raise a BoardError exception if the column is empty (i.e. no move has
        ever been made in the column), or if the column index is invalid.
        '''
        if col < 0 or col > 6:
            raise BoardError('Unknown column; column must be 0-6')
        elif 0 == self.rowlisting[col]:
            raise BoardError('Empty column; no moves were made in that column ')
        
        player = self.board[self.rowlisting[col]-1][col]
        ls = [0] * 4
        ls[0] = self.chk(col, player, 1, 1) + self.chk(col, player, -1, -1) - 1
        ls[1] = self.chk(col, player, 1, 0) + self.chk(col, player, -1, 0) - 1
        ls[2] = self.chk(col, player, 0, -1)
        ls[3] = self.chk(col, player, 1, -1) + self.chk(col, player, -1, 1) - 1
        for i in ls:
            if i >= 4:
                return True
        return False

    def isDraw(self):
        '''
        Check to see if the board is a draw because there are no more
        columns to play in.

        Precondition: This assumes that there is no win on the board.

        Return value: True if there is a draw, else False
        '''
        for i in self.rowlisting:
            if i < 6:
                return False
        return True

    def isWinningMove(self, col, player):
        '''
        Check to see if making the move 'col' by the player 'player'
        would result in a win.  The board state does not change.

        Arguments:
          col    -- a valid column index
          player -- either 1 or 2

        Return value: True if the move would result in a win, else False.

        Precondition: This assumes that the move can be made.
        '''
        if col < 0 or col > 6:
            raise MoveError('Unknown column; column must be 0-6')
        elif player != 1 and player != 2:
            raise MoveError('Invalid player')
        elif self.rowlisting[col] > 6:
            raise MoveError('That column is full')
        
        nbd = self.clone()
        nbd.makeMove(col, player)
        
        if nbd.isWin(col):
            return True
        return False
    
    def chk(self, col, player, a, b):
        '''
        This function looks for any matches of 4 of 'player' given the 
        direction to traverse, a for col and b for row.
        (1, 1) and (-1, -1): Diagonal, right up and left down. 
        (0, -1): Down
        (1, 0) and (-1, 0): Side ways
        (-1, 1) and (1, -1): Diagonal, right down and left up.
        '''
        unswitched = False
        count = 0
        trw = self.rowlisting[col]
        while unswitched == False:
            unswitched = True
            if self.board[trw-1][col] == player:
                count += 1
                unswitched = False
            if trw + b <= 0 or col + a > 6 or trw + b > 6 or col + a < 0:               
                break
            col += a
            trw += b
        return count
    
    def isDrawingMove(self, col, player):
        '''
        Check to see if making the move 'col' by the player 'player'
        would result in a draw.  The board state does not change.

        Arguments:
          col    -- a valid column index
          player -- either 1 or 2

        Return value: True if the move would result in a win, else False.

        Precondition: This assumes that the move can be made, and that the
        move has been checked to see that it does not result in a win.
        '''
        if self.isWinningMove(col, player):
            return False
        else:
            return True



    def show(self):
        '''Print the board to the terminal, along with the player to move.'''

        print
        print '     top'
        print '-------------'
        for row in range(self.row-1, -1, -1):
            for col in range(0, self.col):
                val = self.get(row, col)
                if val == 0:
                    print '.',
                else:
                    print val,
            print
        print '-------------'
        print '0 1 2 3 4 5 6'
        print '   column'
        print
