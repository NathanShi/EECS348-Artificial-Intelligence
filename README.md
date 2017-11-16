# EECS348-Artificial-Intelligence
Course project of Northwestern EECS 348 - Artificial Intelligence, this repo is mainly for tracking my solutions of different AI problems. If you are taking the same class, please do not directly copy the code here.

---

### 1. Hanoi

**The Game**
> The Tower of Hanoi is a puzzle that provides us with the opportunity to look at some of the basic issues in problem solving. The game consists of three pegs and an arbitrary number of disks of descending size. In the initial state, the disks are stacked from largest to smallest on the leftmost peg. The goal is to get all of the disks on the rightmost peg.
It is a classic exponential problem in that the minimum number of moves to solve the problem is 2^n - 1, where n is the number of disks.

In order to play this game, you have to obey the following simple rules:
1. Only one disk can be moved at a time.
2. Each move consists of taking the upper disk from one of the stacks and placing it on top
of another stack i.e. a disk can only be moved if it is the uppermost disk on a stack.
3. No disk may be placed on top of a smaller disk.

**The Assignment**

The assignment is to build a system that takes an initial board position (the disks on each peg) and an end state (the disks on each peg) and searches for the solution using various approaches.
 
You can work in teams of two people. You are going to hand in the homework in the form of two documents:
- The code itself
- A trace of the code running that shows its progress and path and when it is finished,
displays the solution it developed.

**Search**

This is a classic search problem. You should make use of each of these three methods:
- Depth first search in which you commit to a path and continue down it until you reach conclusion or a dead end.
- Breadth first search in which you expand the space of possible solutions by adding a step to each of the initial possibilities that you have taken. This means that you maintain and expand upon all possible solutions to length N until you find the right one.
- Best first search, given a set of states, expand on the one that seems to be closest to the solution. This requires an incremental evaluation function as well as a function to test against end states.

---

### 2. Mancala

**Introduction to Mancala**
> Mancala is a two-player game from Africa in which players moves stones around a board (shown above), trying to capture as many as possible. In the board above, player 1 owns the bottom row of stones and player 2 owns the top row. There are also two special pits on the board, called Mancalas, in which each player accumulates his or her captured stones (player 1's Mancala is on the right and player 2's Mancala is on the left).

> On a player's turn, he or she chooses one of the pits on his or her side of the board (not the Mancala) and removes all of the stones from that pit. The player then places one stone in each pit, moving counterclockwise around the board, starting with the pit immediately next to the chosen pit, including his or her Mancala but NOT his or her opponents Mancala, until he or she has run out of stones. If the player's last stone ends in his or her own Mancala, the player gets another turn. If the player's last stone ends in an empty pit on his or her own side, the player captures all of the stones in the pit directly across the board from where the last stone was placed (the opponents stones are removed from the pit and placed in the player's Mancala) as well as the last stone placed (the one placed in the empty pit) – even if there aren’t any stones on the opponents side to collect (note – this interpretation of the rules differs from how they are implemented on play-mancala.com). The game ends when one player cannot move on his or her turn, at which time the other player captures all of the stones remaining on his or her side of the board.

> You can practice playing the game here: [Mancala Game](http://play-mancala.com/).

**Part 1: A Better Board Score Function**

The board score function in the basic player is too simple to be useful in Mancala--the agent will never be able to look ahead to see the end of the game until it's way too late to do anything about it. Your first task is to write an improved board score in the MancalaPlayer class, a subclass of Player. You may wish to consider the number of pieces your player currently has in its Mancala, the number of blank spaces on its side of the board, the total number of pieces on its side of the board, specific board configurations that often lead to large gains, or anything else you can think of.

You should experiment with a number of different heuristics, and you should systematically test these heuristics to determine which work best. Note that you can test these heuristics with the MINIMAX player, or you can wait until you've completed part 2 below (alpha-beta pruning).

**Part 2: Alpha-Beta Pruning search**

The next part of the assignment is to implement the alpha-beta prune search algorithm described in your textbook and in class. Look in the code to see where to implement this function. You may refer to the pseudocode in the book, but make sure you understand what you are writing.

In your alpha-beta pruning algorithm, you do NOT have to take into account that players get extra turns when they land in their own Mancalas with their last stones. You can assume that a player simply gets one move per turn and ignore the fact that this is not always true. Notice that my provided version of minimax also makes this simplifying assumption. This makes the scoring function slightly inaccurate.

You probably wish to test your alpha-beta pruning algorithm on something simpler than Mancala, which is why I have provided the Tic Tac Toe class. Using alpha-beta pruning, it's possible for an agent to play a perfect game of Tic Tac Toe (by setting ply=9) in a reasonable amount of time. The first move will take the agent awhile (20 seconds or so), but after that the agent will choose its moves quickly. Contrast this to minimax, where a ply greater than 5 takes an unreasonable amount of time.

Test your algorithm carefully by working through the utility values for various board configurations and making sure your algorithm is not only choosing the correct move, but pruning the tree appropriately.

**Part 3: Creating your best custom player**

Create a custom player (using any technique you wish) that plays the best game of Mancala possible. This will be the player that you enter into the class tournament (unless you choose to opt out).

Past years of resourceful students have led me to be more specific about my specification and restrictions for your players:
- Your player must compile without errors.
- Your player must make its moves in 10 seconds or less (you don't need to get fancy with timers or anything, but if it runs significantly longer than that, it will be disqualified from the tournament).
- The name of your player should be your netid (the netid of the student submitting the assignment for your group). Rename both the MancalaPlayer subclass and the Player.py file to exactly match your player's name.(This is so they can be easily identified in the tournament). For example, I would name my player “sho533.” So, my file (which would be called “sho533.py”) would contain a class called “Player” and a class called “sho533”.
- I will not specify a ply for your tournament player. It is your (your player’s) responsibility to use the ply that makes it return a move within 10 seconds. What I mean by this is, I'll instantiate your player in this way for the tournament sho533.sho533(1,sho533.Player.CUSTOM)

In other words, I will not initialize it with a ply - you should either have a default ply, or have the player determine on its own what ply it can get to in each move.
- Your player may NOT use a database.
- Your player may NOT connect remotely to another machine.
- Your code must compile in 5 seconds or less.
- Your player may NOT spawn any other processes or threads. The player must use a
single thread.
- Any pre-computed moves can be hard coded, but not written to or loaded from a file
or database.
- Let me know if you have any further questions!

**What to submit: (please read all bullets below before submitting)**
- netid.py: (i.e. the renamed "Player.py" file) The file containing all the code you have written, including your score function, your alpha beta pruning algorithm and your custom player.
- Be sure to include all of your team member’s names and netid’s in comments at the beginning of the file.
- If you worked in a group, in a comment at the beginning of the file, please write this exact statement. “All group members were present and contributing during all work on this project.”
- Additionally, your code should be readable, commented and clear. There are many possible ways to approach this problem, which makes code style and comments very important here so that the grader and I can understand what you did. For this reason, you will lose points for poorly commented or poorly organized code.

---

### 3 & 4 Logic and Inference
**Finished with teammate Courtney Bankston**

Description please check 
- *Assignment 4_ A Knowledge Base for Block.pdf*, 
- *Function Details.pdf*, 
- *Test File Description.pdf*
