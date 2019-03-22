###################################
#           Board                 #
###################################
"""
    Abstraction function:
        int a * int b * int c -> An a x b minesweeper board with c mines.
"""
import random

class Board():
    """
    Representation Invariants:

       self.boardVals contains only lists of equal length

       self.boardVals[n] are lists of integers (-1 <= int <= 8),
           for all n = [0, len(self.boardVals))

       Each integer in boardVals[n] (n = [0, len(self.boardVals)])
           represents a square on the board, with the following
           definition:
               -1  -> A mine
               0-8 -> 0-8 adjacent mines, respectively. Not a mine.

       self.boardDiscovered matches the size of self.boardVals exactly.

       self.boardDiscovered[n] contains integers (similarly to self.boardVals)
           representing the state of a square on the board, defined:
               -2 -> A flagged, undiscovered square.
               -1 -> A flagged, previously discovered square.
                0 -> An undiscovered square
                1 -> A discovered square
    """

    boardVals = []
    boardDiscovered = []

    """
    Constructs a randomized minesweeper board. Matches the dimensions of board.
    It is recommended that board consists only of lists of zeroes, if
    this is not the case then this function will simply add mines on top
    of any existing mines.

    :param board: the board on which this construction will be overlaid.
                    must be a list of lists of integers, with all sublists
                    being the same length.
    :param mines: A positive integer, the number of mines to be put on the
                    board.
    :returns: a list of lists of integers representing an updated board
                with mines mines aded. Returns a shallow copy of the
                original board if wrong types are provided.
    """
    @staticmethod
    def constructBoard(board, mines):
        try:
            newBoard = board.copy()
            for i in range(mines):
                x = random.randint(0,len(board)-1)
                y = random.randint(0,len(board[0])-1)
                while(newBoard[x][y] == -1):
                    x = random.randint(0,len(board)-1)
                    y = random.randint(0,len(board[0])-1)
                newBoard[x][y] = -1
                for addX in range(x-1,x+2):
                    for addY in range(y-1, y+2):
                        if(addX >= 0 and
                                addY >= 0 and
                                addX < len(board) and
                                addY < len(board[0])):
                            if(newBoard[addX][addY] != -1):
                                newBoard[addX][addY] = newBoard[addX][addY] + 1
            return newBoard
        except TypeError:
            return board.copy()

    """
    Constructor for board. If wrong types are given, constructs a
    board with no mines of length 1 and width 3.

    :param length: A positive integer, the vertical length of the board.
                    Minimum 1.
    :param width: A positive integer, the horizontal width of the board.
                    Minimum 3.
    :param mines: A positive integer, the number of mines to be placed
                    on the board.
    """
    def __init__(self, length, width, mines):
        board = []
        assert(length >= 1), ""
        assert(width >= 3), ""
        try:
            for i in range(width):
                col = []
                for ii in range(length):
                    col.append(0)
                board.append(col.copy())
                self.boardDiscovered.append(col.copy())
            self.boardVals = self.constructBoard(board, mines)
        except assertionError:
            for i in range(3):
                col = []
                for ii in range(1):
                    col.append(0)
                board.append(col.copy())
                self.boardDiscovered.append(col.copy())
            self.boardVals = board
        except TypeError:
            for i in range(3):
                col = []
                for ii in range(1):
                    col.append(0)
                board.append(col.copy())
                self.boardDiscovered.append(col.copy())
            self.boardVals = board

    """
    Gets a character representation of a minesweeper square.

    :param square: An integer in the range -1 <= square <= 8.
                    The square to be conerted.
    :return: A character conversion of square conforming to
                the minesweeper display conventions used here.
                Returns None iff an invalid parameter was given.
    """
    @staticmethod
    def printSquare(square):
        try:
            if(square == -1):
                return 'M'
            elif(square == 0):
                return ' '
            else:
                return str(square)[0]
        except TypeError:
            return None

    """
    Prepares a row of the board for printout.

    :param rowY: 0 <= rowY < len(self.boardVals[0]), the
                    y-value of the row to prepare.
    :returns: A formatted string of the rowY row to print.
    """
    def printRow(self, rowY):
        try:
            assert(0 <= rowY and rowY < len(self.boardVals[0])), ""
            returnStr = ""
            for x in range(len(self.boardVals)):
                returnStr += " "
                if(self.boardDiscovered[x][rowY] == 0):
                    returnStr += "`"
                elif(self.boardDiscovered[x][rowY] < 0):
                    returnStr += "F"
                else:
                    returnStr += str(Board.printSquare(self.boardVals[x][rowY]))
            returnStr += " "
            return returnStr
        except TypeError:
            return ""
        except AssertionError:
            return ""

    """
    Marks the given square at (x,y) as discovered.
    If (x,y) has no adjacent mines then other adjacent
    squares are discovered, this is performed repeatedly
    until all nearby squares are discovered. In regular
    games of minesweeper, this is likely to be all
    relevant squares, however in large, empty boards,
    some squares will be missed to prevent stack overflows.

    :param x: 0 <= x < len(self.boardVals)
    :param y: 0 <= y < len(self.boardVals)
    :returns: The value of the square (x,y) that was
                discovered, None if the spec was broken.
    """
    def discoverSquare(self, x, y):
        try:
            depth = 0
            if(x >= 0 and x < len(self.boardVals) and
                    y >= 0 and y < len(self.boardVals[0])):
                if(self.boardDiscovered[x][y] < 0):
                    return 0
                if(self.boardDiscovered[x][y] == 1):
                    return self.boardVals[x][y]
                self.boardDiscovered[x][y] = 1
                if(self.boardVals[x][y] == 0):
                    for newX in range(x-1,x+2):
                        for newY in range(y-1, y+2):
                            if(newX >= 0 and newY >= 0 and
                                    newX < len(self.boardDiscovered) and
                                    newY < len(self.boardDiscovered[0])):
                                if(self.boardDiscovered[newX][newY] == 0):
                                    try:
                                        if(self.discoverSquareRec(newX,newY, depth + 1) is None):
                                            self.boardDiscovered[newX][newY] = 1
                                    except RecursionError:
                                        return self.boardVals[x][y]
                return self.boardVals[x][y]
            else:
                return None
        except TypeError:
            return None

    """
    Identical to Board.discoverSquare, with the once exception
    that this includes an additional parameter to help with recursive
    calls.

    :param x: 0 <= x < len(self.boardVals)
    :param y: 0 <= y < len(self.boardVals)
    :param depth: The depth of this call in the recursion chain.
    :returns: The value of the square (x,y) that was
                discovered, None if the spec was broken.
    """
    def discoverSquareRec(self, x, y, depth):
        try:
            if(x >= 0 and x < len(self.boardVals) and
                    y >= 0 and y < len(self.boardVals[0])):
                if(self.boardDiscovered[x][y] < 0):
                    return 0
                if(self.boardDiscovered[x][y] == 1):
                    return self.boardVals[x][y]
                self.boardDiscovered[x][y] = 1
                if(self.boardVals[x][y] == 0):
                    for newX in range(x-1,x+2):
                        for newY in range(y-1, y+2):
                            if(newX >= 0 and newY >= 0 and
                                    newX < len(self.boardDiscovered) and
                                    newY < len(self.boardDiscovered[0])):
                                if(self.boardDiscovered[newX][newY] == 0):
                                    if(self.discoverSquareRec(newX,newY, depth+1) is None):
                                        self.boardDiscovered[newX][newY] = 1
                return self.boardVals[x][y]
            else:
                return None
        except TypeError:
            return None
        except RecursionError:
            if(depth < 800):
                return self.boardVals[x][y]
            else:
                raise RecursionError

    """
    Either flags the given square at (x,y), or
    if a flag is already present, returns it to
    the unflagged discovery state it was at before
    being flagged.

    :param x: 0 <= x < len(self.boardVals)
    :param y: 0 <= y < len(self.boardVals)
    :returns: 0 if a mine was not present, 1,
                if a mine was just unflagged,
                -1 if a mine was just flagged,
                None if the spec was broken.
    """
    def flagSquare(self, x, y):
        try:
            if(x >= 0 and x < len(self.boardVals) and
                    y >= 0 and y < len(self.boardVals[0])):
                if(self.boardDiscovered[x][y] < 0):
                    self.boardDiscovered[x][y] += 2
                    if(self.boardVals[x][y] == -1):
                        return 1
                else:
                    self.boardDiscovered[x][y] -= 2
                    if(self.boardVals[x][y] == -1):
                        return -1
                return 0
            return None
        except TypeError:
            return None
