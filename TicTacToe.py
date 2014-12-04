"""
Created on November 19th, 2014

Python script that allows a computer to play Tic-Tac-Toe against a human.
The computer will either win or draw; it will never lose. Because computer.

This Tic Tac Toe class uses the Minimax algorithm with computer as Max and human as Min.

@author: Patricia Bailey

Usage:
    python TicTacToe.py
"""

import sys
from copy import deepcopy

'''
A class representing a Tic Tac Toe game that favors computers.
The computer will always win or draw. It will never lose.
'''
class TicTacToe:

    def __init__(self):

        # sets up the Tic Tac Toe board as a list of integers
        self.board = [1,2,3,4,5,6,7,8,9]

        # used to error check for invalid input from the human user
        self.possibleInput = ['1','2','3','4','5','6','7','8','9']

        # list of lists of the possible ways for a human or computer to win
        # 0-2: Horizontal 3-5: Vertical 6-7: Diagonal
        self.possibleWinStates = [[1, 2, 3],[4, 5, 6],[7, 8, 9],[1, 4, 7],
                                  [2, 5, 8],[3, 6, 9],[1, 5, 9],[3, 5, 7]]

        # human plays by placing an 'X' on the board
        self.human = 'X'

        # computer plays by placing an 'O' on the board
        self.computer = 'O'

    '''
    Prints out the rules of Tic Tac Toe and an initial board
    to show the human player the spaces it can choose from.
    '''
    def rules(self):

       print "\nYou are playing Noughts & Crosses. You will take turns marking the spaces in a 3x3 grid."
       print "The spaces are represented by numbers. You must type a number from 1 to 9 to decide where"
       print "to place your X. The player who succeeds in placing three respective marks in a horizontal,"
       print "vertical, or diagonal row wins the game."
       print "\nYou are playing against a computer. Don't be surprised if you fail miserably. A lot..."
       print "You will make the first move.\n"

       self.outputBoard()       # prints empty board for visual of spaces available

    '''
    Returns a visual representation of the Tic Tac Toe board.
    '''
    def outputBoard(self):

        for square in range(3):
            print self.board[square],

        print ""
        for square in range(3):
            print self.board[square+3],

        print ""
        for square in range(3):
            print self.board[square+6],

    '''
    Inserts an X into the square that the human chooses.
    '''
    def placeX(self, state, chosenSquare):

        if state.__contains__(chosenSquare):
            state.remove(chosenSquare)
            state.insert(chosenSquare - 1, self.human)
            return True
        else:
            print "Your X could not be placed. This space is already taken."
            print "Please choose a different space.\n"
            return False

    '''
    Inserts an O into the square that the computer chooses.
    '''
    def placeO(self, state, chosenSquare):

        if state.__contains__(chosenSquare):
            state.remove(chosenSquare)
            state.insert(chosenSquare - 1, self.computer)

    '''
    Returns True if the player has a winning position for the given state of the
    game and False if they do not.
    '''
    def checkWinningPosition(self, currentState, player):

        for state in self.possibleWinStates:
            r,s,t = state       # separates the win state into three pieces
            if (currentState[r-1] == player) and (currentState[s-1] == player) and (currentState[t-1] == player):
                return True

        return False

    '''
    Returns True if board is full and False if it is not full.
    '''
    def isBoardFull(self, currentState):

        for s in currentState:
            if (s != self.human) and (s != self.computer):
                return False

        return True

    '''
    Returns True if the game is over and False if it is not.
    '''
    def terminalTest(self, currentState):

        if self.checkWinningPosition(currentState, self.human):         # human wins
            return True
        elif self.checkWinningPosition(currentState, self.computer):    # computer wins
            return True
        elif self.isBoardFull(currentState):                            # it's a draw
            return True
        return False

    '''
    Returns -1 if the human wins, a 1 if the computer wins, and a 0 if it's a draw.
    '''
    def utility(self, currentState):

        if self.checkWinningPosition(currentState, self.human):         # human wins
            return -1
        elif self.checkWinningPosition(currentState, self.computer):    # computer wins
            return 1
        else:                                                           # it's a draw
            return 0

    '''
    Returns a list of spaces on the board that are not yet taken.
    '''
    def successors(self, currentState):

        state = []

        for s in currentState:
            if (s != self.human) and (s != self.computer):
                state.append(s)

        return state

    '''
    A depth-first adversarial search that determines the "best play" for computer.

    state - the state of the game being evaluated
    level - determines what level being evaluated where

        Max: level % 2 == 0
        Min: level % 2 != 0
    '''
    def minimax(self, state, level):

        move = -1

        # checks to see if the game is over
        if self.terminalTest(state):
            return (self.utility(state), 0)

        else:
            if level % 2 == 0:                      # max code
                max = float("-inf")
                for s in self.successors(state):
                    stateCopy = deepcopy(state)     # copy of the board for recursive minimax
                    self.placeO(stateCopy, s)       # places an O into the board copy
                    tempMax, tempMove = self.minimax(stateCopy, level+1)
                    if tempMax > max:
                        max = tempMax
                        move = s

                return (max, move)

            else:                                   # min code
                min = float("inf")
                for s in self.successors(state):
                    stateCopy = deepcopy(state)     # copy of the board for recursive minimax
                    self.placeX(stateCopy, s)       # places an X into the board copy
                    tempMin, tempMove = self.minimax(stateCopy, level+1)
                    if tempMin < min:
                        min = tempMin
                        move = s

                return (min, move)


    '''
    Plays an entire game of Tic Tac Toe.
    '''
    def playTicTacToe(self):

        # prints the rules of Tic Tac Toe
        self.rules()

        # loops until the game is over
        while (True):

            # begin human's turn
            print "\n\nPlease type a number between 1 and 9.\n"

            # used to make sure the space is not already taken
            isValid = False

            # retrieves, error checks, and places human's input onto the Tic Tac Toe board
            while (isValid == False):

                # takes input from the user
                input = raw_input()

                # error checks the user's input before passing it to be placed on the board
                if(self.possibleInput.__contains__(input)):         # if string input is in list of possible valid input
                    chosenSquare = int(input)                       # type cast to an int
                    isValid = self.placeX(self.board, chosenSquare) # attempts to place the X on board
                else:
                    print "You've entered an invalid number. Please enter a whole number between 1 and 9.\n"

            # prints Tic Tac Toe board after an X is placed
            self.outputBoard()

            # checks to see if the game has ended after the human has gone
            if self.terminalTest(self.board):
                result = self.utility(self.board)
                if result == -1:
                    print "\n\nHuman wins!"
                    break
                elif result == 0:
                    print "\n\nIt's a draw!"
                    break

            # begin computer's turn
            print "\n\nThe computer places an O.\n"

            # copy of the board for minimax
            currentStateCopy = deepcopy(self.board)
            value, move = self.minimax(currentStateCopy, 0)

            # places an O with the move that minimax returned
            self.placeO(self.board, move)

            # prints Tic Tac Toe board after an O is placed
            self.outputBoard()

            # checks to see if the game has ended after the computer has gone
            if self.terminalTest(self.board):
                result = self.utility(self.board)
                if result == 1:
                    print "\n\nComputer wins!"
                    break
                elif result == 0:
                    print "\n\nIt's a draw!"
                    break

def main():

    playAgain = True

    while playAgain == True:

        game = TicTacToe()
        game.playTicTacToe()

        print "\nWould you like to play again?\n"

        input = raw_input()
        input = input.lower()
        if input == 'y' or input == 'yes' or input == '':
            playAgain = True
        else:
            print "\nThanks for being a good sport! Bye!\n"
            playAgain = False


if __name__ == "__main__":

    # some preliminary error checking

    if len(sys.argv) != 1:
        print 'Usage: python TicTacToe.py'
    else:
        main()