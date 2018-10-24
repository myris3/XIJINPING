
board_size = 13

max_depth = 100

aligned = True

max_turns = 100


class Node():
    def __init__(self):
        self.neighbours = []
        self.color = "0" #What shows when I print the board
        self.r=0 #row placement
        self.c=0 #column placement
        self.visited = 0
        
#Make a deep copy of the board state
def copyBoardTree(matrix):
    new = newCreateBoardTree()
    for i_row in range(0, len(matrix)):
        for i_col in range(0, len(matrix[i_row])):
            node = matrix[i_row][i_col]
            new_node = new[i_row][i_col]
            new_node.r = node.r
            new_node.c = node.c
            new_node.color = node.color
    return new

#Go down from 2d list of Nodes, from 2d list of strings
def simplifyBoardRep(matrix):
    new = newCreateBoardTree()
    for i_row in range(0, len(matrix)):
        for i_col in range(0, len(matrix[i_row])):
            node = matrix[i_row][i_col]
            new[i_row][i_col] = node.color
    return new 

#Primary way of creating the board representation
def newCreateBoardTree():

    #stage 1, create the onion, layerslayerslayers

    matrix = []
    global board_size

    if(board_size%2 ==0):
        print("Board size must be odd, fixing the issue")
        board_size += 1

    
    for i in range(0, board_size):
        row = []

        if (i<board_size//2 +1):
            for j in range(0, i+1):
                node = Node()
                node.r = i
                node.c = j
                row.append(node)
            matrix.append(row)
        else:
            lengthOfLastRow = len(matrix[i-1])
            lengthOfThisRow = lengthOfLastRow-1
            for j in range(0, lengthOfThisRow):
                node = Node()
                node.r = i
                node.c = j
                row.append(node)
            matrix.append(row)

    #stage 2, connect the layers and nodes in the same layer
    
    for j in range(0, len(matrix)):
        row = matrix[j]

        if len(row) != 1: #Connect internally on a layer
            for i in range(1, len(row)):
                row[i].neighbours.append(row[i-1])
                row[i-1].neighbours.append(row[i])
        
        if j+1 < len(matrix): # Connect nodes between layers

            nextRow = matrix[j+1]
            

            if (len(row)<len(nextRow)): #When connecting layers in increasing order
                for x in range(0, len(row)):
                    row[x].neighbours.append(nextRow[x])
                    row[x].neighbours.append(nextRow[x+1])
                    nextRow[x].neighbours.append(row[x])
                    nextRow[x+1].neighbours.append(row[x])

            else: #When connecting layers in decreasing order

                for z in range(0, len(nextRow)):
                    nextRow[z].neighbours.append(row[z])
                    nextRow[z].neighbours.append(row[z+1])
                    row[z].neighbours.append(nextRow[z])
                    row[z+1].neighbours.append(nextRow[z])

    return matrix

#Function to print the board in a nice way
def printCheckerBoard(matrix, aligned):
    #board_size determines amount of rows
    #TODO: does not print just right for all sizes, some scaling issue 
    half_point = (board_size//2)
    half_size = len(matrix[half_point])
    padding = half_size//2+3
    i=0
    if aligned:
        axis = "    "
        for x in range(0, half_size):
            axis+=str(x)+ " "
        print(axis)

    for row in matrix:
        if not aligned:
            if (i>9):
                 stringprint =str(i)+ "" + " "*(padding)
            else:

                stringprint =str(i)+ " " + " "*(padding)
        else:
            if i>9:
                stringprint = str(i)+" "
            else:

                stringprint=str(i)+"  "

        if (i<half_point):
            padding-=1
        else:
            padding+=1

        #print("Padding is ", padding) 
        i+=1 
        for item in row:
            stringprint += " "+str(item.color)
        print(stringprint)





def placeToken(row, column, matrix, token):
    matrix[row][column].color = token
    return matrix

def removeToken(row, column, matrix):
    saveToken = matrix[row][column].color 
    matrix[row][column].color = "0"
    return matrix, saveToken
#Call this if pieces on board needs moved, returns moved = False if no change was made
def moveToken(startRow, startColumn, endRow, endColumn, matrix):
    moved = False
    if (matrix[endRow][endColumn].color == "0"):
        matrix, savedToken = removeToken(startRow, startColumn, matrix)
        matrix = placeToken(endRow, endColumn, matrix, savedToken)
        #print("Placement happened")
        moved = True

    return matrix, moved

#Determine the relative fitness of each board state, sum of the row values for any single player. TODO: This could be more advanced
def calculateScore(matrix, token, startingRow):    
    score = 0
    for r in range(0, len(matrix)):
        for c in range(0, len(matrix[r])):
            node = matrix[r][c]
            #print(node)
            if node.color == token:
                toAdd = 0
                if startingRow == board_size-1:
                    toAdd = - r + board_size - 1
                else:
                    toAdd = r
                score += toAdd
                #print("Node at ", (r, c), " evaluated at ", toAdd)

    return score

            
            




#Used during debugging
def printNeighbours(node):
    neighbours = []
    for i in node.neighbours:
        neighbours.append((i.r, i.c))
    print(neighbours)

#Debugging tool
def possibleMovesVisual(row, column, matrix):
    #moves = possibleMoves(row, column, matrix)
    moves = {}
    fullRecursivePossibleMoves(max_depth, row, column, matrix, moves, matrix[row][column])
    for t in moves.keys():
        placeToken(t[0], t[1], matrix,  "x")

#after looking for possible moves, clear all visited flags in each node
#used in fullRecursivePossibleMoves
def clearVisited(matrix):
    for row in matrix:
        for node in row:
            node.visited = 0
    return matrix

#Primary function to find all moves any piece can do on the board
def fullRecursivePossibleMoves(depth, row, column, matrix, moves, origin):
    # This seems to actually work, i dub the the delta rule

    if depth==0:
        return

    node = matrix[row][column]

    node.visited = 1
    
    for n in node.neighbours:
        if n.visited == 1:
            continue

        if n.color == "0" and depth == max_depth:
            n.visited = 1
            moves[(n.r, n.c)] = [origin, 0]

        if n.color != "0":
            for item in n.neighbours:
                if item.color == "0":
                    row_delta = abs(item.r-node.r)
                    col_delta = abs(item.c-node.c)
                    #delta rule
                    if (row_delta == 2 or row_delta ==0) and (col_delta ==2 or col_delta ==0):
                        item.visited = 1
                        n.visited = 1
                        moves[(item.r, item.c)] = [origin, 0]
                        fullRecursivePossibleMoves(depth-1, item.r, item.c, matrix, moves, origin)

            


#Create default starting positions for player 1 and player 2   
def createStartingPositions(token1, token2):
    matrix = newCreateBoardTree()
    #Assuming board size is reasonable

    #global board_size
    #board_size = 13

    for i in range(0,4):
        for col in matrix[i]:
            placeToken(col.r,col.c, matrix, token1)

    for j in range(len(matrix)-4, len(matrix)):
        for col in matrix[j]:
            placeToken(col.r, col.c,matrix, token2)

    return matrix

#Test to see the starting position of any default game
def run():
    matrix = createStartingPositions()
    printCheckerBoard(matrix, False)
    print("scores\tplayer1: ",calculateScore(matrix, "1", 0),"\n\tplayer2: ",calculateScore(matrix,"2",len(matrix)-1))




if __name__=="__main__":
    run()
