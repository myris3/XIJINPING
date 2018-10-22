
board_size = 9



class Node():
    def __init__(self):
        self.neighbours = []
        self.color = "0" #What shows when I print the board
        self.r=0 #row placement
        self.c=0 #column placement
        self.visited = 0


def newCreateBoardTree():
    #plan: separate the creating of the board, and the connecting, previous solution was way to cluttered

    #stage 1, create the onion, layerslayerslayers

    matrix = []
    if(board_size%2 ==0):
        print("Board size must be odd, returning empty matrix")
        return matrix
    
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



def printCheckerBoard(matrix):
    for row in matrix:
        stringprint = ""
        for item in row:
            stringprint += " "+str(item.color) + " "
        print(stringprint)

def placeToken(row,column, matrix, token):
    matrix[row][column].color = token

def removeToken(row, column, matrix):
    saveToken = matrix[row][column].color 
    matrix[row][column].color = "0"
    return saveToken

def moveToken(startRow, startColumn, endRow, endColumn, matrix):
    savedToken = removeToken(startRow, startColumns, matrix)
    placeToken(endRow, endColumn, matrix, savedToken)

def printNeighbours(node):
    neighbours = []
    for i in node.neighbours:
        neighbours.append((i.r, i.c))
    print(neighbours)


def possibleMovesVisual(row, column, matrix):
    #moves = possibleMoves(row, column, matrix)
    moves = []
    fullRecursivePossibleMoves(row, column, matrix, moves, matrix[row][column])
    for t in moves:
        placeToken(t[0], t[1],matrix,  "x")


def fullRecursivePossibleMoves(row, column, matrix, moves, origin):
    #Assuming initial node is occupied
    node = matrix[row][column]
    color = node.color
    node.visited = 1
    for n in node.neighbours:
        if n.color == "0" and n.visited == 0 and node.color != 0:
            moves.append((n.r, n.c))
            n.visited = 1
        else:
            if origin.color != "0" and n.visited != 0 and :
                 fullRecursivePossibleMoves(n.r, n.r, matrix, moves, node)
        



def possibleMoves(row, column, matrix):
    moves = [] #row, column tuples of each possible move

    if (matrix[row][column].color=="0"):
        print("You called possibleMoves on an empty slot")
        return moves

    node =  matrix[row][column]
    node.visited = 1
    for i in node.neighbours:
        i.visited=1

        if (i.color == "0"):
            moves.append((i.r, i.c))
            #print("Appended ", (i.r, i.c))
        else:
            #for j in i.neighbours:
                #if (j.visited ==0):
                    #auxPossibleMoves(j, moves, node)
            auxPossibleMoves(i, moves, node)
    return moves

def auxPossibleMoves(node, possibleMoves, origin):
    #Called on an occupied node
    
    for i in node.neighbours:
        if (i.visited == 0):
            if (i.color == "0"):

                i.visited = 1
                candidate = (i.r, i.c)
                delta = i.c-origin.c

                if (candidate not in possibleMoves and abs(delta)==2):        
                        possibleMoves.append(candidate)
                        #i.visited = 1
                        #print("Appended ", candidate)
                for j in i.neighbours:
                    if (j.color != "0" and j.visited==0):
                        auxPossibleMoves(j, possibleMoves, i)

            
    #print(possibleMoves)


    


def run():
    print("Starting print")
    matrix = newCreateBoardTree()

    #print("Rows: ", len(matrix), "Columns of row2: ", len(matrix[2]))
    #for row in matrix:
    #    print(len(row))
    placeToken(0,0, matrix,"1")
    placeToken(1,1, matrix, "1")
    placeToken(3,2,matrix,"1")
    #printNeighbours(matrix[6][1])

    #possibleMoves(0,0, matrix))
    possibleMovesVisual(0,0,matrix)

    #placeToken(len(matrix)-1, 0, matrix, "2")
    printCheckerBoard(matrix)
    print("End print")





if __name__=="__main__":
    run()
