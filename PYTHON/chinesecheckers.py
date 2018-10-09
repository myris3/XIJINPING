
board_size = 9



class Node():
    def __init__(self):
        self.neighbours = []
        self.color = 0
        self.r=0
        self.c=0
        self.visited = 0

def createBoardTree(): # New plan: create tree of nodes to represent game board
    matrix = []
    for i in range(0, board_size): # create node layers increasing in size
        row=[]
        #TODO: Fix issue with an empty list being the first element of matrix, this messes up indexing, due to z starting on 0
        for z in range(0, i): #Create row of nodes
            node = Node()
            node.r=i
            node.c=z
            row.append(node)
        if len(row) != 1: # Create adjacency to neighbours within row
            for x in range(0, len(row)):
                if x+1 < len(row):
                    row[x].neighbours.append(row[x+1])
                if x-1 >= 0:
                    row[x].neighbours.append(row[x-1])
        matrix.append(row)
        if i > 0:
            previousRow = matrix[i-1]
            for y in range(0, len(previousRow)): # add adjacency between layers
                previousRow[y].neighbours.append(row[y])
                previousRow[y].neighbours.append(row[y+1])
                row[y].neighbours.append(previousRow[y])
                row[y+1].neighbours.append(previousRow[y])
    for n in range(0, board_size-2): # Decreasing row sizes to match shape of board. Size of board should probably be supplied as an arg
        i = board_size-2-n

        row = []

        for z in range(0,i):
            node = Node()
            node.r = i
            node.c = z
            row.append(node)
        if len(row) != 1: # Possibly put this in a function, to increase readability
            for x in range(0, len(row)):
                if x+1 < len(row):
                    row[x].neighbours.append(row[x+1])
                if x-1 >= 0:
                    row[x].neighbours.append(row[x-1])
        matrix.append(row)
        previousRow = matrix[len(matrix)-2]
        #print("Length of row: "+ str(len(row)))
        #print("Length of pprevRow: " + str(len(previousRow)))
        for y in range(0, len(row)):
            #print("Y is: "+ str(y))
            row[y].neighbours.append(previousRow[y])
            row[y].neighbours.append(previousRow[y+1])
            previousRow[y].neighbours.append(row[y])
            previousRow[y+1].neighbours.append(row[y])
             

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




def possibleMoves(row, column):
    moves = []

    if (matrix[row][column].color=="0"):
        return moves
    node =  matrix[row][column]
    node.visited = 1
    for i in node.neighbours:
        if i.color == "0":
            moves.append((node.r, node.c))
        else:
            for j in i.neighbours:
                if (j != node):
                    auxPossibleMoves(j, moves)
                    


def auxPossibleMoves(node, possibleMoves): #Called on an occupied node
    for i in node.neigbours:
        if (i.visited == 0):
            i.visited = 1
            if (i.color == "0"):
                candidate = (i.r, i.c)
                if (candidate not in possibleMoves):
                    possibleMoves.append(candidate)
                for j in i.neigbours:
                    if (j.color != "0"):
                        auxPossibleMoves(j, possibleMoves)

            



    


def run():
    print("Starting print")
    matrix = createBoardTree()
    #print(matrix)
    placeToken(1,0,matrix,"1")
    placeToken(len(matrix)-1, 0, matrix, "2")
    printCheckerBoard(matrix)
    print("End print")




#oldplan: use adjacency matrix to set constraints on game board, each piece has its own adjacency matrix, charting where it can move
#plan 20.08 Use node tree to set constraints, changing the color of nodes depending on what occupies it
#[
#["x"]
#["x","x"]
#["x","x","x"]
#["x","x","x","x"]
#["x","x","x"]
#["x","x"]
#["x"]
#]



if __name__=="__main__":
    run()
