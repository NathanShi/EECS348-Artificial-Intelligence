import copy
import sys

myGameBoard = [] # Start State Game Board, Global
finalGameBoard = [] # End State Game Board, Global

# Define the tree node
class treeNode:
    def __init__(self, data):
        self.children = [] # List of children
        self.parent = None # parent node
        self.state = data # game board state
        self.level = None # node level, for dfs
        self.distance = None # distance, for best first search

    # Add children
    def appendChildren(self, childNode):
        self.children.append(childNode)

    # define parent
    def giveParent(self, parentNode):
        self.parent = parentNode
        self.level = parentNode.level + 1

########
# Best First Search
#
#
########
# Calculate the distance to final state, compare differences between two state,
# and add the disk reprenstative number
def calculateDistance(currentNode):
    dis = 0
    for i in range(0,3):
        for j in range (0, len(currentNode.state[i])):
            if currentNode.state[i][j] not in finalGameBoard[i]:
                dis += currentNode.state[i][j]
    return dis

# Give a node list, return the index of the smallest distance node
def findSmallestDistanceNode(nodeList):
    compare = sys.maxint
    index = 0
    for i in range(0, len(nodeList)):
        if compare > nodeList[i].distance:
            index = i
            compare = nodeList[i].distance
    return index

# Best first search
def hanoi_BestFS():
    root = treeNode(myGameBoard)
    root.level = 0
    root.distance = calculateDistance(root) # Node the root
    targetNode = root # targetNode for tracking the path by parent

    checkedDistanceList = []
    visitedState = []
    checkedDistanceList.append(root) # add root to list
    path = []

    while len(checkedDistanceList) > 0:

        # Find smallest distance node index in the list, then pop
        currentNode = checkedDistanceList.pop(findSmallestDistanceNode(checkedDistanceList))

        # If not visited add to list
        if (currentNode.state) not in visitedState:
            visitedState.append(currentNode.state)
        # If matches final state, set node and break the loop
        if compareWithFinalBoard(currentNode.state):
            targetNode = currentNode
            break

        # For every possible move, if not visited then create Node
        for possibleMoves in possibleMovesList(currentNode.state):
            if possibleMoves not in visitedState:
                tempNode = treeNode(possibleMoves)
                # Build Connect with parent
                currentNode.appendChildren(tempNode)
                tempNode.giveParent(currentNode)
                # Calculate the distance to final state
                tempNode.distance = calculateDistance(root)
                # Add to list
                if tempNode not in checkedDistanceList:
                    checkedDistanceList.append(tempNode)

    # Trace back to start state, add path to path list
    while targetNode.state is not myGameBoard:
        path.insert(0, targetNode.state)
        targetNode = targetNode.parent
    path.insert(0, myGameBoard)

    #Print the path
    for i in range(0, len(path)):
        if i == 0:
            print "Initial Step 0"
        else:
            print "Step " + str(i)
        printGameBoard(path[i])
        print "---"

# Helper Function
# Print Game Board Vertically
# Use 0 to fit empty
def printGameBoard(board):
    max_disk = max(map(len, board))  # finding max length
    output = zip(*map(lambda x: [0] * (max_disk - len(x)) + x , board)) #convert to print vertically
    for i in output:
        print i # printing the result

# Helper Function
# Get user input
# Split by ','
# Small number indicates small disks goes in front of large ones.
# Assume ALL input is VALID
def getUserInput():
    for i in range(0,3):
        print "Please input initial disks on Peg %c:" % (i + 65)
        user_input = raw_input()
        if not user_input:
            myGameBoard.append([])
        else:
            input_list = map(int,user_input.split(',')) #split by ,
            myGameBoard.append(input_list)
    print "============"
    for i in range(0,3):
        print "Please input final disks on Peg %c:" % (i + 65)
        user_input = raw_input()
        if not user_input:
            finalGameBoard.append([])
        else:
            input_list = map(int,user_input.split(',')) #split by ,
            finalGameBoard.append(input_list)

    if not checkIfValid():
        print "Invalid Input, the number of disks doesn't match"
        print "------------------------------------------------\n"
        getUserInput()

# Helper Function
# Check if input start state and end state is valid on numbers
def checkIfValid():
    sum_start = 0
    sum_end = 0

    for peg in myGameBoard:
        for number in peg:
            sum_start += number

    for peg in finalGameBoard:
        for number in peg:
            sum_end += number

    if sum_start == sum_end:
        return True
    else:
        return False



# Compare with target game board
def compareWithFinalBoard(board):
    for i in range(0,3):
        if (set(board[i]) != set(finalGameBoard[i])):
            return False
    return True

########
# DFS
#
#
########

def hanoi_DFS():
    root = treeNode(myGameBoard)
    root.level = 0 # Node the root
    targetNode = root # targetNode for tracking the path by parent
    visitedState = []
    nextState = []
    nextState.append(root) # Add root to list

    while len(nextState) > 0:
        currentNode = nextState.pop(0) # Serve as Stack

        if currentNode.state not in visitedState:
            visitedState.append(currentNode.state)

        if compareWithFinalBoard(currentNode.state):
            # If it matches final state, check if it is the shortest path by level
            if targetNode.level == 0 or targetNode.level > currentNode.level:
                targetNode = currentNode

        for possibleMoves in possibleMovesList(currentNode.state):
            # Create node for possible moves
            tempNode = treeNode(possibleMoves)
            # if not visited, add to tree
            if tempNode.state not in visitedState:
                # Build connection with parent
                currentNode.appendChildren(tempNode)
                tempNode.giveParent(currentNode)
                # Push to Stack
                if tempNode not in nextState:
                    nextState.append(tempNode)
            else:
                # If already visited, compare currentNode level with tempNode parent level
                if tempNode.parent is not None:
                    # If currentNode is more close to root, change the connection
                    if currentNode.level < tempNode.parent.level:
                        tempNode.parent = currentNode
                        tempNode.level = currentNode.level+1
                        if tempNode not in currentNode.children:
                            currentNode.children.append(tempNode)
                else:
                    tempNode.parent = currentNode

    # Trace back to start state by parent pointer.
    path = []
    while targetNode.state is not myGameBoard:
        path.insert(0, targetNode.state)
        targetNode = targetNode.parent
    path.insert(0, myGameBoard)

    # Print the pass
    for i in range(0, len(path)):
        if i == 0:
            print "Initial Step 0"
        else:
            print "Step " + str(i)
        printGameBoard(path[i])
        print "---"

########
# BFS
#
#
########
# Hanoi BFS Main Function
# Use Queue for BFS, also a dictionary 'index' to mimic a tree structure.
# See details via inline comments
def hanoi_BFS():
    visitedState = [] # List of visited state
    nextState = [] # List of next state, act as queue
    index = {} # Dictionary to store index of state, 'children:parent'
    nextState.append(myGameBoard) # Add initial state to list
    final_index = -1 # Index of final state matches with user input in visitedState
    shortest_path = [] # Queue & Dictionary to act as a tree, this stores shortest path

    while len(nextState) != 0: # nextState not empty
        currentState = nextState.pop(0) # Act as Queue, get first element of the list, FIFO

        # If matches end state from user input
        if compareWithFinalBoard(currentState):
            # Set final_index
            final_index = visitedState.index(currentState)
            break

        # Make Queue unique, don't allow cycle
        if currentState not in visitedState:
            # Store parent index
            parent_index = len(visitedState)
            visitedState.append(currentState)
        else:
            # If already in list, find index
            parent_index = visitedState.index(currentState)

        # Get all possible moves of current state
        for possibleState in possibleMovesList(currentState):
            if possibleState not in visitedState:
                # If this possible state not visited, add to list. BFS
                nextState.append(possibleState)
                # Set dictionary (key:value) as (children:parent)
                index[len(visitedState)] = parent_index
                # Add possibleState to visitedState
                visitedState.append(possibleState)

    # There should always a path between start state and end state.
    if (final_index == -1):
        print "NO PATH!"
    else:
        #Loop until the final_index goes to 0, this is tracing back the tree to top
        while final_index != 0:
            # Add to shortest_path use index
            shortest_path.insert(0, visitedState[final_index])
            final_index = index[final_index]
        # Add start state to shortest_path
        shortest_path.insert(0, myGameBoard)

        # Print the shortest_path
        for i in range(0, len(shortest_path)):
            if i == 0:
                print "Initial Step 0"
            else:
                print "Step " + str(i)
            printGameBoard(shortest_path[i])
            print "---"

# Search all possible moves for current State
# Increase Tree breadth
# compareToMove() is to compare two pegs and return a possible move
# moveDisk() is to actually move the disk.
def possibleMovesList(current):
    list_moves = [] # Return possible moves in list

    # Compare 3 pegs with each other
    compareResult_0_1 = compareToMove(current[0], current[1])
    compareResult_0_2 = compareToMove(current[0], current[2])
    compareResult_1_2 = compareToMove(current[1], current[2])

    # Compare result for peg0 and peg1
    if (compareResult_0_1 == 1):
        attempt_move = copy.deepcopy(current)
        moveDisk(attempt_move, 0, 1)
        list_moves.append(attempt_move)

    elif (compareResult_0_1 == 2):
        attempt_move = copy.deepcopy(current)
        moveDisk(attempt_move, 1, 0)
        list_moves.append(attempt_move)

    # Compare result for peg0 and peg2
    if (compareResult_0_2 == 1):
        attempt_move = copy.deepcopy(current)
        moveDisk(attempt_move, 0, 2)
        list_moves.append(attempt_move)

    elif (compareResult_0_2 == 2):
        attempt_move = copy.deepcopy(current)
        moveDisk(attempt_move, 2, 0)
        list_moves.append(attempt_move)

    # Compare result for peg1 and peg2
    if (compareResult_1_2 == 1):
        attempt_move = copy.deepcopy(current)
        moveDisk(attempt_move, 1, 2)
        list_moves.append(attempt_move)

    elif (compareResult_1_2 == 2):
        attempt_move = copy.deepcopy(current)
        moveDisk(attempt_move, 2, 1)
        list_moves.append(attempt_move)

    return list_moves

# Compare two pegs to see if which one can move
# return 0 means no move, other wise return former or latter peg can move
def compareToMove(peg1, peg2): #Compare two pegs
    if (not peg1 and not peg2): #If both empty, don't move
        return 0
    elif (not peg1 and peg2): #If one empty, move another
        return 2
    elif (peg1 and not peg2): #If one empty, move another
        return 1
    else:
        if (peg1[0] < peg2[0]): #Move smaller disk
            return 1
        else:
            return 2

# Move the disk from peg to peg by index
def moveDisk(current, from_peg, to_peg):
    moved = current[from_peg].pop(0)
    current[to_peg].insert(0, moved)

# Call input function
getUserInput()

# Show user input for start state and final state
print "======Your Start State======"
printGameBoard(myGameBoard)
print "=======Your End State======="
printGameBoard(finalGameBoard)

print '\n'
print '\n'
print "==============================="

# Excecute the game with BFS
print "======Start Game with BFS======"
hanoi_BFS()
print "=======End Game with BFS======="

print '\n'
print '\n'
# Excecute the game with DFS
print "======Start Game with DFS======"
hanoi_DFS()
print "=======End Game with DFS======="

print '\n'
print '\n'
# Excecute the game with Best FS
print "====Start Game with Best FS===="
hanoi_BestFS()
print "=====End Game with Best FS====="


# UNIT TEST CODE:
# print compareWithFinalBoard(myGameBoard)
# print compareToMove(myGameBoard[0], myGameBoard[1])
# print compareToMove(myGameBoard[1], myGameBoard[2])
# list_temp = possibleMovesList(myGameBoard)
# for moves in list_temp:
#     printGameBoard(moves)
#     print "==="
