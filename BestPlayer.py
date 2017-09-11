import random
from Connect4Simulator import *

class BestPlayer:
    def __init__(self):
        '''
        Initialize the player using the best computer player.

       The best player (maybe...) using min-max.
       
        '''
        self.depth = 5
 
    def chooseMove(self, board, player):
        '''
        Choose a move given current board and player. 
        We will use the min-max strategy. 
        There are a few places where we will avoid at all cost.
        '''
        
        pmoves = board.possibleMoves()
        oplayer = 3 - player
        unmakable = [0]*7  
        best = -9999999
        bestMove = 0        
        
        # Tests for immediate wins
        for i in pmoves:         
            if board.isWinningMove(i, player):
                return i
            
        # Tests for what moves might cause the opponent's immediate win. 
        for i in pmoves:      
            if board.isWinningMove(i, oplayer):
                return i 
            
        # Tests for moves that leads to opponent's win
        for i in pmoves:
            stimu = board.clone()
            stimu.makeMove(i, player)
            stimulst = stimu.possibleMoves()
            for j in stimulst:              
                if stimu.isWinningMove(j, oplayer):
                    unmakable[i] = 1  
                    
        # Starts min-max search; heuristic-score is places in totalMoves
        totalMoves = [-999999]*7
        for i in pmoves:
            tempbd = board.clone()
            tempbd.makeMove(i, player)
            temp = self.dps(self.depth-1, tempbd, oplayer)
            temp *= -1
            totalMoves[i] = temp
            if unmakable[i] == 1:
                print i, unmakable[i]
                totalMoves[i] = -99999
        
        # Checks and returns highest score
        for i in range(7):
            if totalMoves[i] >= best: 
                bestMove = i
                best = totalMoves[i]
        
        if bestMove not in pmoves:
            return pmoves[0]
        return bestMove

    def dial(self, board, tCol, tRow):
        '''
        Method that evaluates the amount of streaks going diagonal left up.
        If that place has been traversed, skip that place.
        '''
        
        dial1 = [0,0,0,0,0,0,0]
        dial2 = [0,0,0,0,0,0,0]         
        grid =  [[0 for x in range(7)] for y in range(6)] 
        
        for col in range(3, tCol):
            row = 0
            while row<tRow :
                val = board.get(row, col)
                if val == 2 and grid[row][col] == 0:
                    score = self.streak(board, -1, 1, col, row, 2)
                    if score > 0:
                        score = self.correctsScore(score)
                        for i in range(score):
                            grid[row+i][col-i] = -1
                        dial2[score]+=1
                elif val == 1 and grid[row][col] == 0:
                    score = self.streak(board, -1, 1, col, row, 1)
                    if score > 0:
                        score = self.correctsScore(score)
                        for i in range(score):
                            grid[row+i][col-i] = -1                        
                        dial1[score]+=1  
                row += 1     
        return dial1, dial2
        
    def side(self, board ,tCol, tRow):
        '''
        Method that evaluates the amount of streaks going side right.
        If that place has been traversed, skip that place.
        '''        
        
        side1 = [0,0,0,0,0,0,0,0,0]
        side2 = [0,0,0,0,0,0,0,0,0]        
        for row in range(tRow):
            col = 0
            while col<tCol-3:
                jumpc = 1
                score = 1
                val = board.get(row, col)
                if val == 2:
                    score = self.streak(board, 1, 0, col, row, 2)
                    if score > 0:
                        score = self.correctsScore(score)
                        side2[score]+=1
                        jumpc = score
                elif val == 1:
                    score = self.streak(board, 1, 0, col, row, 1)
                    if score > 0:
                        score = self.correctsScore(score)
                        side1[score]+=1  
                        jumpc = score
                col += jumpc  
        return side1, side2

    def up(self, board, tCol, tRow):
        '''
        Method that evaluates the amount of streaks going up.
        If that place has been traversed, skip that place.
        '''
        
        up1 = [0,0,0,0,0,0,0]
        up2 = [0,0,0,0,0,0,0]        
        for col in range(tCol):
            row = 0
            while row<tRow :
                #print col, row
                jumpr = 1
                val = board.get(row, col)
                if val == 2:
                    score = self.streak(board, 0, 1, col, row, 2)
                    if score > 0:
                        score = self.correctsScore(score)
                        up2[score]+=1
                        jumpr = score
                elif val == 1:
                    score = self.streak(board, 0, 1, col, row, 1)
                    if score > 0:
                        score = self.correctsScore(score)
                        up1[score]+=1  
                        jumpr = score
                row += jumpr        
        return up1, up2
    
    def diar(self, board, tCol, tRow):
        '''
        Method that evaluates the amount of streaks going diagonal right up.
        If that place has been traversed, skip that place.
        '''        
        
        diar1 = [0,0,0,0,0,0,0]
        diar2 = [0,0,0,0,0,0,0]        
        grid =  [[0 for x in range(7)] for y in range(6)] 
        
        for col in range(0, tCol-2):
            row = 0
            while row<tRow :
                val = board.get(row, col)
                if val == 2 and grid[row][col] == 0:
                    score = self.streak(board, 1, 1, col, row, 2)
                    if score > 0:
                        score = self.correctsScore(score)
                        for i in range(score):
                            grid[row+1][col+1] = -1
                        diar2[score]+=1
                elif val == 1 and grid[row][col] == 0:
                    score = self.streak(board, 1, 1, col, row, 1)
                    if score > 0:
                        score = self.correctsScore(score)
                        for i in range(score):
                            grid[row+i][col+i] = -1                        
                        diar1[score]+=1
                row += 1 
        return diar1, diar2
    
    def correctsScore(self, score):
        '''
        To make sure no errors will be thrown. I hope.
        '''
        if score > 6 :
            return 6
        elif score < 0:
            return 0
        return score
    
    def score(self, board, player):
        '''
        Calculates a score for each board.
        '''
        tRow = board.getRows()
        tCol = board.getCols()
        score1 = 0
        score2 = 0
        finscore1 = 0
        finscore2 = 0
        
        dial1, dial2 = self.dial(board, tCol, tRow)
        diar1, diar2 = self.diar(board, tCol, tRow)
        side1, side2 = self.side(board, tCol, tRow)
        up1, up2     = self.up(board, tCol, tRow)
        
        for i in range(len(dial1)):
            finscore1 += dial1[i]*10**(i)
            finscore1 += diar1[i]*10**(i)
            finscore1 += side1[i]*10**(i)
            finscore1 += up1[i]*10**(i)
            finscore2 += dial2[i]*10**(i)
            finscore2 += diar2[i]*10**(i)
            finscore2 += side2[i]*10**(i)
            finscore2 += up2[i]*10**(i) 
            
        if player == 1:
            return finscore1
        else:
            return finscore2
        
    def streak(self, board, a, b, col, row, player):
        '''
        This function looks for any 'player', and determines how
        many of them pops up. A lot of if-statements look for
        patterns that CANNOT form 4 in a row.
        '''
        oplayer = 3 - player
        unswitched = False
        count = 0
        if col >= 6 or row >=5:
            return -1
        while unswitched == False:
            unswitched = True
            if board.get(row,col) == player:
                count += 1
                unswitched = False
            if row + b < 0 or col + a > 6 or row + b > 5 or col + a < 0:
                b = row > 0 and col > 0 and col < 6 and row < 5 
                if b and board.get(row-b, col-a) == oplayer and count <= 3:
                    return -1
                if count < 3:
                    return -1
                break
            if row > 2 and a == 1 and b == 1:
                return -1
            if board.get(row+b, col+a) == oplayer and count <=3:
                return -1
            col += a
            row += b
            
        return count
    

    def dps(self, depth, board, player):
        '''
        By creating a tree like state, recursively find the max state for AI, 
        and min state for human. 
        '''
        pmoves = board. possibleMoves()
        mapmoves = []
        oplayer  = 3 - player
        better = -999999
        
        for i in pmoves:
            tempbd = board.clone()
            tempbd.makeMove(i, player)
            mapmoves.append(tempbd)
            
        if  board.isDraw() or depth == 0 or len(pmoves) == 0:
            temp = self.score(board, player)
            if temp is None:
                temp = 0
            return temp

        for moves in mapmoves :
            if moves == None:
                pass
            temp = self.dps(depth-1, moves, oplayer)
            if temp is None:
                temp = 0            
            temp *= -1
            better = max(better, temp)
        return better
        
    