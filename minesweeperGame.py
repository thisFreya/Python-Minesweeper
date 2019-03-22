#################################
#       MinesweeperGame         #
#################################
"""
    Abstraction function:
        int a * int b * int c * window w -> A game of minesweeper in window w
                                            set on an a x b board with c mines.
"""
import board
import curses
import time
from curses import wrapper

class MinesweeperGame():
    """
    Representation Invariants:

        board is a boardLength x boardWidth board with mines mines.

        boardLength, boardWidth, and mines are all positive integers

        boardLength >= 1, boardWidth >= 3

        window is contained within screen

        window is a curses.window instance that displays the game board.

        scr is a curses.window instance that contains window and
            displays the instructions.
    """
    mines = 0
    boardLength = 0
    boardWidth = 0
    board = None
    scr = None
    window = None

    """
    Gets input from the user.

    :returns: A string representing the first key the user enters
                after this is called.
    """
    def getInput(self):
        return self.window.getkey()

    """
    Handles display and function of the game of minesweeper.
    Will not terminate until the game is won or lost.

    :returns: whether the game was won.
    """
    def beginGame(self):
        minesRemaining = self.mines

        cursorX = 0
        cursorY = 0

        for y in range(self.boardLength):
            self.window.addstr(y+1, 1, self.board.printRow(y))
        self.window.addstr(cursorY+1, 2*(cursorX+1)-1, "[")
        self.window.addstr(cursorY+1, 2*(cursorX+1)+1, "]")
        self.scr.refresh()
        self.window.refresh()
        stop = False
        while(not stop):
            ch = 'l'
            while(ch != 's' and
                    ch != 'w' and
                    ch != 'a' and
                    ch != 'd' and
                    ch != 'f' and
                    ch != ' '):
                ch = self.getInput().lower()
            if(ch == 's'):
                cursorY += 1
                if(cursorY >= self.boardLength):
                    cursorY = 0
            elif(ch == 'w'):
                cursorY -= 1
                if(cursorY < 0):
                    cursorY = self.boardLength - 1
            elif(ch == 'a'):
                cursorX -= 1
                if(cursorX < 0):
                    cursorX = self.boardWidth - 1
            elif(ch == 'd'):
                cursorX += 1
                if(cursorX >= self.boardWidth):
                    cursorX = 0
            elif(ch == 'f'):
                minesRemaining += self.board.flagSquare(cursorX, cursorY)
                if(minesRemaining == 0):
                    stop = True
            elif(ch == ' '):
                square = self.board.discoverSquare(cursorX, cursorY)
                if(square == -1):
                    stop = True

            for y in range(self.boardLength):
                self.window.addstr(y+1, 1, self.board.printRow(y))
            self.window.addstr(cursorY+1, 2*(cursorX+1)-1, "[")
            self.window.addstr(cursorY+1, 2*(cursorX+1)+1, "]")
            self.window.refresh()
            self.scr.refresh()
        return minesRemaining == 0

    """
    Displays the win and lose states of the game.
    More accurately, displays "YOU WIN!" or
    "YOU LOSE" in the top bar of the game board
    based on the state of win

    :param win: Whether the game was won or lost,
                    True iff the game should be displayed
                    as a victory.
    """
    def winState(self, win):
        try:
            str = ""
            xPos = int((self.boardWidth*2 + 3) / 2) - 4
            yPos = 0
            if(win):
                str = "YOU WIN!"
            else:
                str = "YOU LOSE"
            self.window.addstr(yPos, xPos, str)
        except TypeError:
            pass

    """
    Initializes the game of minesweeper and handles its
    completion. Waits for user input after the game before
    terminating.

    :param length: A positive integer, at least 1. The length
                    of the minesweeper board.
    :param width: A positive integer, at least 3. The width
                    of the minesweeper board.
    :param mines: A positive integer, the number of mines
                    on the minesweeper board.
    :param mainscr: A curses.window instance, the window
                    in which the game will be displayed.
                    Must be at least length + 5 tall and
                    width*2 + 3 wide.
    """
    def __init__(self, length, width, mines, mainscr):
        try:
            self.scr = mainscr
            #curses.noecho()
            #curses.cbreak()
            curses.curs_set(0)
            self.boardLength = length
            self.boardWidth = width
            self.mines = mines
            self.board = board.Board(length, width, mines)
            self.window = curses.newwin(length+2, width*2+3)
            self.window.box()
            self.scr.addstr(length+2,0,"[W][A][S][D] to move")
            self.scr.addstr(length+3,0,"[SPACE]      to uncover")
            self.scr.addstr(length+4,0,"[F]          to flag")

            self.winState(self.beginGame())

            self.window.getch()
            #curses.nocbreak()
            #curses.echo()
            #curses.endwin()
        except TypeError:
            pass

def main(mainscr):
    MinesweeperGame(20, 20, 60, mainscr)
wrapper(main)
