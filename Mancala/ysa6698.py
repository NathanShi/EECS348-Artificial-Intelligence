# File: Player.py
# Author(s) names AND netid's: Yibing Shi, ysa6698
# Date: 10/15/2017
# Group work statement: I'm contributing to all work on this project.
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.

"""If 'Netid.Netid(1, Netid.Player.CUSTOM)' is not able to be called,
   Please use 'Netid(1, Player.CUSTOM)' to call, this is how I test my
   CUSTOM player"""

from random import *
from decimal import *
from copy import *
from MancalaBoard import *
# from sys import *
# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4

    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)

    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score

    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """

        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        # print "Alpha Beta Move not yet implemented"
        # returns the score adn the associated moved
        # return (-1,1)
        move = -1
        score = -INFINITY
        turn = self
        alpha = -INFINITY # lower bound of Alpha Beta Move
        beta = INFINITY # upper bound of Alpha Beta Move

        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.alphaBetaMin(nb, ply-1, turn, alpha, beta)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    # lower bound
    def alphaBetaMin(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.alphaBetaMax(nextBoard, ply-1, turn, alpha, beta)
            #print "s in minValue is: " + str(s)
            # if s is less than score, then score = s since it's smaller.
            if s < score:
                score = s
            # if score is smaller
            if score <= alpha:
                return score # prune rest of the node
            # update beta. beta represents min node.
            beta = min(beta, score)

        return score

    def alphaBetaMax(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.alphaBetaMin(nextBoard, ply-1, turn, alpha, beta)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
            # if score larger than beta
            if score >= beta:
                return score # prune rest of the node
            # update alpha, represents the max node
            alpha = max(score, alpha)
        return score



    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            val, move = self.alphaBetaMove(board, 7) # 8 ply will take too long
            print "chose move", move, " with value", val
            return move
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class ysa6698(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        # print "Calling score in MancalaPlayer"
        if board.hasWon(self.num):
            return 1000000.0 # Win the game, return a max value
        elif board.hasWon(self.opp):
            return -1000000.0 # Lose the game, return a min value

        """Use different amount of stones in Mancala(Mancala[user] - Mancala[oppo]),
               different amount of stones in all pit(sum(cups[user]) - sum(cups[oppo])),
               different amount of empty pit(empty[user] - empty[oppo]),
               different amount of pit that can end to Mancala for another chance(potential[user] - potential[oppo]).
           to evaluate the score of current stage."""

        # different amount of stones in Mancala(Mancala[user] - Mancala[oppo])
        if self.num == 1:
            diff_mancala = board.scoreCups[0] - board.scoreCups[1]
            total_stones_Self = sum(board.P1Cups)
            total_stones_Oppo = sum(board.P2Cups)
        else:
            diff_mancala = board.scoreCups[1] - board.scoreCups[0]
            total_stones_Self = sum(board.P2Cups)
            total_stones_Oppo = sum(board.P1Cups)

        empty = 0 # Empty pit
        potential = 0 # Potential Pit that can give another move

        for pit in range(0, 6):
            if self.num == 1:
                # If self pit has 0, add to empty
                if board.P1Cups[pit] == 0:
                    empty += 1
                # If oppo pit has 0, minus to empty
                if board.P2Cups[pit] == 0:
                    empty -= 1
                # If self pit can end in Mancala, add to potential
                if board.P1Cups[pit] + pit == 6:
                    potential += 1
                # If oppo pit can end in Mancala, minus to potential
                if board.P2Cups[pit] + pit == 6:
                    potential -= 1
            else:
                # If oppo pit has 0, minus to empty
                if board.P1Cups[pit] == 0:
                    empty -= 1
                # If self pit has 0, add to empty
                if board.P2Cups[pit] == 0:
                    empty += 1
                # If oppo pit can end in Mancala, minus to potential
                if board.P1Cups[pit] + pit == 6:
                    potential -= 1
                # If self pit can end in Mancala, add to potential
                if board.P2Cups[pit] + pit == 6:
                    potential += 1

        diff_stones = total_stones_Self - total_stones_Oppo

        """Since the stones in Mancala are not movable, thus it should have most weight.
           The potential pit and empty pit that can win another move are useful to player,
           they should have second weight. The diff stones are less important since it changes
           so frequently"""
        return 5 * diff_mancala + 3 * potential + 2 * empty + diff_stones
        #return Player.score(self, board)
