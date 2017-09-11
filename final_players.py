# Name: Ziyan Mo
# CMS cluster login name: Zmo

'''
final_players.py

This module contains code for various bots that play Connect4 at varying 
degrees of sophistication.
'''

import random
from Connect4Simulator import *

# Any other imports go here...

class RandomPlayer:
    '''
    This player makes one of the possible moves on the game board,
    chosen at random.
    '''

    def chooseMove(self, board, player):
        '''
        Given the current board and player number, choose and return a move.

        Arguments:
          board  -- a Connect4Board instance
          player -- either 1 or 2

        Precondition: There must be at least one legal move.
        Invariant: The board state does not change.
        '''

        assert player in [1, 2]
        possibles = board.possibleMoves()
        assert possibles != []
        return random.choice(possibles)


class SimplePlayer:
    '''
    This player will always play a move that gives it a win if there is one.
    Otherwise, it picks a random legal move.
    '''

    def chooseMove(self, board, player):
        '''
        Given the current board and player number, choose and return a move.

        Arguments:
          board  -- a Connect4Board instance
          player -- either 1 or 2

        Precondition: There must be at least one legal move.
        Invariant: The board state does not change.
        '''
        
        assert player in [1, 2]
        moves = board.possibleMoves()
        assert moves != []
        for i in moves:
            if board.isWinningMove(i, player):
                return i
        ranum = random.randint(0, len(moves)-1)
        return moves[ranum]


class BetterPlayer:
    '''
    This player will always play a move that gives it a win if there is one.
    Otherwise, it tries all moves, collects all the moves which don't allow
    the other player to win immediately, and picks one of those at random.
    If there is no such move, it picks a random move.
    '''

    def chooseMove(self, board, player):
        '''
        Given the current board and player number, choose and return a move.

        Arguments:
          board  -- a Connect4Board instance
          player -- either 1 or 2

        Precondition: There must be at least one legal move.
        Invariant: The board state does not change.
        '''
        oplayer = 3 - player
        moves = board.possibleMoves()
        unmakable = [] 
        assert player in [1, 2]
        assert moves != []        
        # Tests for immediate wins
        for i in moves:         
            if board.isWinningMove(i, player):
                return i
        # Tests for what moves might cause the opponent's immediate win. 
        for i in moves:      
            if board.isWinningMove(i, oplayer):
                return i 
        # If I make this move, will the opponent win?
        for i in moves:
            stimu = board.clone()
            stimu.makeMove(i, player)
            stimulst = stimu.possibleMoves()
            for j in stimulst:              
                if stimu.isWinningMove(j, oplayer):
                    unmakable.append(i)    
        # Get list of good moves
        trumov = [x for x in moves if x not in unmakable]  
        # If there are no good moves, return anything. 
        if trumov == [] or unmakable == []:    
            ranum = random.randint(0, len(moves)-1)  
            return moves[ranum]
        ranum = random.randint(0, len(trumov)-1)
        return trumov[ranum]


class Monty:
    '''
    This player will randomly simulate games for each possible move,
    picking the one that has the highest probability of success.
    '''

    def __init__(self, n, player):
        '''
        Initialize the player using a simpler computer player.

        Arguments: 
          n      -- number of games to simulate.
          player -- the computer player
        '''

        assert n > 0
        self.player = player
        #print self.player
        self.n = n

    def chooseMove(self, board, player):
        '''
        Given the current board and player number, choose and return a move.

        Arguments:
          board  -- a Connect4Board instance
          player -- either 1 or 2

        Precondition: There must be at least one legal move.
        Invariant: The board state does not change.
        '''
        moves = board.possibleMoves()
        result = [-1]* 7
        maxi = 0 
        maxx = 0
        check = True
        player1 = BetterPlayer()
        player2 = BetterPlayer()
        assert player in [1, 2]
        assert moves != []        
        if player == 1:
            player1 = self.player
            toMove = 2
        else:
            player2 = self.player
            toMove = 1           
        for i in moves:      
            maxi = i
            if board.isWinningMove(i, player):
                return i              
            result[i] = 0
            
            # Running simulations; if win matches player, add to a list
            # so we can compute total chances of winning
            for j in range(self.n):
                stimu = board.clone()
                stimu.makeMove(i, player)                 
                sim = Connect4Simulator(stimu, player1, player2, toMove) 
                tresult = sim.simulate()   
                if tresult == player:
                    result[i] += tresult
            if maxx < result[i]:
                maxx = result[i]
                maxi = i
                check == False
                
        print moves
        print'I\'m Monty!', maxi
        return maxi
    
