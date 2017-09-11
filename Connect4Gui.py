import tkMessageBox
import ttk
from Tkinter import *
import time

import sys
from final_board import *
from final_players import *
from BestPlayer import *
import random

class Connect4:
    '''Instances of this class simulate an interactive Connect-4 game.'''

    def __init__(self, opponent, toMove, canvas, root):
        '''
        Initializes the game.

        Arguments:
          opponent -- the computer opponent object
          toMove   -- the first player to move.  1 = human, 2 = computer.
        '''
        assert toMove in [1, 2]
        self.toMove = toMove
        self.opponent = opponent
        self.board = Connect4Board()
        self.nrows = self.board.getRows()
        self.ncols = self.board.getCols()
        
        # Initiating variables
        self.moves = []
        self.circle = []
        self.curcolhum = 0
        self.counter = 0
        self.newest = 0        
        self.newestChk = False
        self.end = False
        
        self.root = root
        self.canv = canvas
        self.canv.pack()
        
        if self.toMove == 1:
            self.canv.bind('<Button-1>', self.button_handler)        
        
        # Creating announcements at the top
        bgtxt = 'First player to move: %d'
        fclr = '#FFDBF1'
        self.txtbox = self.canv.create_rectangle(0,0, 800, 40, fill = fclr)
        self.txt = self.canv.create_text(400, 20, text = (bgtxt % self.toMove))

        # Creating the overall image
        self.p1 = PhotoImage(file = "IMG_5101.gif")
        self.p2 = PhotoImage(file = "IMG_5102.gif")
        self.images = [self.p1, self.p2]
        self.bdimg = PhotoImage(file = "Board.gif")
        self.bdimg_h = self.canv.create_image(400, 340, image = self.bdimg)    
            
        # Quiting and undo buttons
        quitb = Button(self.root, text = "Quit", command = self.quit)
        quitb_win = self.canv.create_window(10, 10, anchor=NW, window=quitb)
        undob = Button(self.root, text = "Undo", command = self.unmakeMove)
        undob_win = self.canv.create_window(730, 10, anchor=NW, window=undob)        
        
    def printBoard(self):
        '''
        This creates the gamem image. 
        Whenever a new step is made, there is a dropping animation 
        for the piece. 
        Otherwise, just print to where ever it should be.
        
        '''
        for row in range(self.nrows-1, -1, -1):
            for col in range(0, self.ncols):
                val = self.board.get(row, col)
                if ((val == 1 or val == 2) and self.end == False):
                    x = 60+100*col
                    y = 590-100*row                    
                    bl = (row + 1 < 6 and self.board.get(row+1, col) == 0 )
                    im = self.bdimg
                    t = self.images[val-1]
                    if bl and col == self.newest and self.newestChk:
                        self.newest = -1
                        t = self.images[val-1]
                        i = self.canv.create_image(x, 40, image = t, anchor='nw')
                        self.bdimg_h = self.canv.create_image(400, 340, image = im) 
                        totalY = 40
                        self.newestChk = False
                        while y != totalY and self.end == False:
                            self.canv.move(i, 0, 10)
                            totalY+=10
                            time.sleep(0.0000001)
                            self.root.update()
                        self.circle.append(i)
                    elif col == self.newest:
                        self.newest = -1
                        i = self.canv.create_image(x, y, image = t, anchor='nw')
                        self.bdimg_h = self.canv.create_image(400, 340, image = im)     
                        self.root.update()
                        self.circle.append(i)
                        
    def getendstate(self):
        '''
        Making sure the game is still going
        '''
        return self.end
        
    def quit(self):
        '''
        Stops the canvas from showing. 
        '''
        self.root.destroy()
        self.end = True
        
        
    def makeMove(self, col, player):
        '''
        Make a move on the board.

        Arguments:
          col    -- a valid column index
          player -- either 1 or 2
        '''

        if col < 0 or col >= self.ncols:
            raise MoveError('invalid move: %d' % col)
        self.board.makeMove(col, player)
        self.moves.append((player, col))

    def unmakeMove(self):
        '''
        Unmake a move on the board.  This means that the last move by
        both players is undone i.e. those locations on the board are cleared.

        Raise a MoveError exception if there are not enough moves to undo.
        '''

        if len(self.moves) > 1:
            self.board.unmakeMove(self.moves.pop()[1])
            self.canv.delete(self.circle[len(self.circle)-1])
            self.board.unmakeMove(self.moves.pop()[1])
            self.canv.delete(self.circle[len(self.circle)-2])

        else:
            raise MoveError('Not enough moves to undo!')
        
    def changePlayerToMove(self):
        '''Change the player to move.'''
        self.toMove = 3 - self.toMove   # changes 2 -> 1 and 1 -> 2

    def button_handler(self, event):
        '''
        When the mouse presses in canvas, this method
        is called. 
        If the mouse is within region of board, 
        it will allow the player to drop a piece there
        by calling self.choosecol().
        '''
        self.counter +=1
        if event.x<50 or event.x >750:
            self.counter -=1
        else:
            self.chooseCol(event.x, event.y)
        
    def chooseCol(self, x, y):
        '''
        Stop if either player wins or if the board is full.  Allow the user to
        undo moves.
        This detects where the mouse has clicked, and 
        at that place drops a piece. 
        It will also check for win and loss. 
        '''
        try:
            self.canv.unbind('<Button-1>')
            xlst = [50,150,151,250,251,350,351,450,451,550,551,650,651,750]
            for i in range(7):
                boolean = x > xlst[i*2] and x < xlst[i*2+1] 
                if boolean and self.counter == 1 and self.toMove == 1:
                    self.makeMove(i, 1)
                    self.canv.delete(self.txt)
                    txt = 'Player plays on column %d...'
                    self.txt = self.canv.create_text(400, 20, text = (txt % i))                     
                    self.newest = i
                    self.newestChk = True
                    self.printBoard()
                    self.curcolhum = i
            if self.end == True:  
                return   
            self.counter = 0
            time.sleep(1)
            
            # Checking for endgames
            boolean = self.board.isDraw() == False and self.end == False
            if boolean and self.board.isWin(self.curcolhum) == False :
                self.changePlayerToMove()
                self.playAI()
            elif self.board.isWin(self.curcolhum) == True:            
                self.win()
                return
            elif self.board.isDraw() == True:
                self.draw()  
                return
            
        except ValueError, e:
            print e
            print >> sys.stderr, 'Invalid command; try again...'

        except MoveError, e:
            print e
            print >> sys.stderr, 'Move error; try again...'

        except BoardError, e:
            print e
            print >> sys.stderr, 'Board error; try again...'
            
    def playAI(self):
        '''
        The computer opponent moves. 
        Checks for endgame after moving
        '''
        col = 0
        if self.toMove == 2 and self.end == False:  # player 2 = computer
            col = self.opponent.chooseMove(self.board.clone(), 2)
            self.makeMove(col, 2)
            self.canv.delete(self.txt)
            txt = 'Computer plays on column %d...'
            self.txt = self.canv.create_text(400, 20, text = (txt % col))
            self.newest = col
            self.newestChk = True
            self.printBoard()
            time.sleep(1)
            
            boolean = self.board.isDraw() == False and self.end == False
            if self.board.isWin(col) == False and self.toMove == 2 and boolean:
                self.changePlayerToMove()
                self.canv.bind('<Button-1>', self.button_handler)
            elif self.board.isWin(col) == True:
                self.win()
                return
            elif self.board.isDraw() == True:
                self.draw()
                return
            
    def win(self):
        '''
        What is displayed if someone wins;
        complier sleeps to allow user to see text
        '''
        self.delete()
        txt = "Game over: player %d wins!"
        self.txt = self.canv.create_text(400, 400, text = (txt % self.toMove))     
        time.sleep(3)
        return  

    def draw(self):
        '''
        What to display if it is a draw; 
        complier sleeps to allow user to see text
        '''
        self.delete()
        txt = "Game over: the game is a draw." 
        self.txt = self.canv.create_text(400, 400, text = (txt)) 
        time.sleep(3)
        return
    
    def delete(self):
        '''
        Clears the pieces away and creates end game window. 
        '''
        for cir in self.circle:
            self.canv.delete(cir)
        self.canv.delete(self.txt)
        self.canv.delete(self.bdimg_h)
        box = self.canv.create_rectangle(200,350, 600, 500, fill = '#FFFFFF') 
        okb = Button(self.root, text = "Ok", command = self.quit, anchor = W)
        okb_win = self.canv.create_window(380, 430, anchor=NW, window=okb)                     
                
    
def quit():
    '''
    Quiting for player choice root
    '''
    global root1
    root1.destroy()    
    
def stop():
    '''
    Quiting for monty root
    '''    
    global rootme
    rootme.destroy() 
    
def labels(root1):
    '''
    This is the instructions for the connect 4 game. 
    '''
    txt1 = 'This is a Connect4 game with four levels of difficulty!'
    lbl1 = Label(root1, text = txt1)
    lbl1.grid(row=0, column=0, columnspan=3) 
    
    txt2 = 'Your color will be blue while the computer will be red'
    lbl2 = Label(root1, text = txt2)
    lbl2.grid(row=2, column=0, columnspan=5)
    
    txt3 = 'You can quit or press undo during the game'
    lbl3 = Label(root1, text = txt3)
    lbl3.grid(row=4, column=0, columnspan=5)                 
    
    txt4 = 'For monty, a pop-up  will ask for number of simulations'
    lbl4 = Label(root1, text = txt4)
    lbl4.grid(row=6, column=0, columnspan=5)
    
    txt5 = 'A pop-up will ask for replay after the game ends'
    lbl5 = Label(root1, text = txt5)
    lbl5.grid(row=8, column=0, columnspan=5)   
    
    txt6 = 'Simply click on the desired column to make that move'
    lbl6 = Label(root1, text = txt6)
    lbl6.grid(row=10, column=0, columnspan=5)         

    
if __name__ == '__main__':
    replay = True
    # Need to check to see if user wants to replay
    while replay == True:
        
        # Block to determine difficulty
        root1 = Tk()
        labels(root1)
        choice_var = StringVar()
        dif_lbl = Label(root1, text='Select difficulty for connect four.')
        dif_lbl.grid(column=1)    
        playerList = ['Random', 'Simple', 'Better', 'Monty', 'Best']
        opt_menu = OptionMenu(root1, choice_var, *playerList) 
        opt_menu.grid(column=1)    
        btn = Button(root1, text='Play',command=quit)
        btn.grid(column=1)
        root1.mainloop()
        player =  choice_var.get()
        
        # Creates opponent given the difficulty
        if player == 'Random':
            opponent = RandomPlayer()
        elif player == 'Simple':
            opponent = SimplePlayer()
        elif player == 'Better':
            opponent = BetterPlayer()
        elif player == 'Best':
            opponent = BestPlayer()
        elif player == 'Monty':
            
            # Creates a pop-up asking for num of simulations
            rootme = Tk()
            gsim = StringVar()
            sim_lbl = Label(rootme, text='Enter number of simulations per move')
            sim_lbl.grid(row=0, column=0, columnspan=3)
            nsim_entry = Entry(rootme, textvariable=gsim)
            nsim_entry.grid(row=1, column=1)
            convert_btn = Button(rootme, text='Confirm', command=stop)
            convert_btn.grid(row=3, column=1)    
            rootme.mainloop()
            try:
                nsims = gsim.get()
                nsims = int(nsims)
                assert nsims > 0
                player = SimplePlayer()
                opponent = Monty(nsims, player)
            except ValueError:
                e = 'Invalid number of simulations.  Exiting.'
                tkMessageBox.showerror('Error', e)
                break
        else:
            tkMessageBox.showerror('Error','Invalid player name.  Exiting.')
            break

        # Creates mainroot and canvas; starts game; checks for replay?
        root = Tk()
        root.geometry('800x800')
        canvas = Canvas(root, width=800, height=680)           
        toMove = random.choice([1, 2])
        game = Connect4(opponent, toMove, canvas, root)
        game.printBoard()
        game.playAI()
        root.mainloop()
        Tk().withdraw()
        replay = tkMessageBox.askyesno('Replay','Replay?')  
