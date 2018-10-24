import chinesecheckers as helper
import time



#Agent class, a way to contain useful data and methods pertaining any player
class Greedy_Agent():
    def __init__(self, token, startingRow):
        self.startingRow = startingRow
        self.token = token
    #Helper method, used in determining the score of a board position relative to the agent 
    def calculateNodeScore(self, node):
        score = 0
        if self.token == "1":
            score = node.r
        else:
            score = helper.board_size-1 - node.r
        return score
    #Primary method, does a lot of things, in summary, returns two tuples, represents origin game piece and destination position on the gameboard.
    #Finally, it returns a score, the score being the value of the current  board state after the move has been performed
    def suggestedMove(self, matrix):
        
        #plan: 1.enumerate all moves
        #      2. analyse all moves
        #      3. choose one with highest value
        #      4. do some default cases, return some special value if no change is made to board state
        
        
    
        listOfMoveDicts = []

        for row in matrix:
            for node in row:
                if node.color == self.token:
                    #TODO: logic isnt working properly, doesnt properly evaluate game state 
                    moves = {}
                    matrix = helper.clearVisited(matrix)
                    helper.fullRecursivePossibleMoves(
                            helper.max_depth,
                            node.r,
                            node.c,
                            matrix,
                            moves,
                            node)
                    if len(moves.keys()) == 0:
                        continue
                    #print("Printing contents of moves: ", moves.keys())
                    listOfMoveDicts.append(moves)
        
        highest_delta = 0
        suggestedMove = (0, 0)
        suggested_origin = (0, 0)
        highest_score = 0        
        for moves in listOfMoveDicts:
            for move in moves.keys():

                #moves is a dict, keys are tuples with the move to be considered, the data with the key is a list, with the origin node at element 0
                temp = helper.copyBoardTree(matrix) 

                #renaming for readability
                destination = (move[0], move[1])
                origin = (moves[move][0].r, moves[move][0].c)

                scoreBefore = helper.calculateScore(temp, self.token, self.startingRow)
                #print(move)
                temp, dump = helper.moveToken(origin[0], origin[1], destination[0], destination[1], temp)
                
                scoreAfter = helper.calculateScore(temp, self.token, self.startingRow)
                
                delta = scoreAfter - scoreBefore
                #print("delta is", delta)

                #moves[move][1] = delta
                 
                if delta > highest_delta:
                    #print("Score before is ",scoreBefore, ". Score after is ", scoreAfter, "move ",origin, destination, " is considered")
                    highest_delta = delta
                    suggestedMove = destination
                    suggested_origin = origin
                    highest_score = scoreAfter

        # trigger this if there seems to be no good greedy option, find the lowest score node, and determine direction to highest score increase
        if highest_delta == 0: # find the piece with lowest score, plot a path for it to closest increase in score
            
            candidate = (0, 0)
            scores = {}
            #Iterate over each node, getting the scores for each, put them in a dict, with similar scores on same key in dict
            for row in matrix:
                for node in row:
                    if self.token == node.color:
                        score = self.calculateNodeScore(node)
                        if score in scores:
                            scores[score].append(node)
                        else:
                            scores[score] = [node]
                            
            #Go from lowest score to "infinity", stopping at the lowest score it finds, and evaluates
            for i in range(0, 1000):
                if i in scores:
                    spaces_and_nodes = {}

                    for node in scores[i]:
                        #evaluate free space on previous and next row
                        #pick the node with closest distance to the free space wich will increase its score
                        rowToExamine = -1

                        #See if score gradient points up a row, or down a row
                        if self.calculateNodeScore(matrix[node.r-1][0]) > i:
                            rowToExamine = node.r-1
                            #print("Considering up, i is  ",i)
                        else:
                            rowToExamine = node.r+1
                            #print("Considering down, i is ", i)
                        free_spaces = []
                        
                        #Consider each free space on the row in question, and calculate the distance to it
                        for n in matrix[rowToExamine]:
                            if n.color == "0":
                                #append a list with the node, and the distance, if distance is negative, space is to the right of node, else to the left
                                free_spaces.append([n, node.c - n.c])

                        spaces_and_nodes[node] = free_spaces
                    
                    signed_distance = 0
                    shortest_distance = 10000
                    destination = (0, 0)
                    origin = (0, 0)
                    #Try to find a node with shortest distance to score increase
                    for node in spaces_and_nodes.keys():
                        for item in spaces_and_nodes[node]:
                           # print("At ", node.color, item)
                            if abs(item[1]) <shortest_distance:
                                shortest_distance = abs(item[1])
                                signed_distance = item[1]
                                destination = (item[0].r, item[0].c)
                                origin = (node.r, node.c)
                                #print("considering ", origin, destination)
                    #Heres a rule to determine to go left or right on the row (the idea is to break out of the local optimum)
                    if signed_distance<0: 
                        suggestedMove = (origin[0], origin[1]+1)
                    else:
                        suggestedMove = (origin[0], origin[1]-1)
                    
                    suggested_origin = origin

                    break
                    



        return suggestedMove, suggested_origin, highest_score

    
            
class Game():
    def __init__(self, agent1, agent2, board):
        self.player1 = agent1
        self.player2 = agent2
        self.gameBoard = board
        self.gameNotOver = True
        self.turn = 1
        self.current = "3"
        self.maxTurns = helper.max_turns

    #main loop to drive a game between two agents 
    def play(self):
        print("|___________________________________|")
        print("|___________Initial Board___________|")
        print("|___________________________________|")
        helper.printCheckerBoard(self.gameBoard, helper.aligned)
        print("")


        winner = ""
        loser = ""
        score1 = 0
        score2 = 0
        turns = 0
        #shape of this sould be a copy of the board, turn count, scores of each player
        turnStack = []

        while self.gameNotOver:
            move = (0, 0)
            toMove = (0, 0)
            #score = 0
            player = self.player1
            moved = True
            
            #Alternate between player1 and 2
            if self.turn%2 != 0:
                move, toMove, tempscore1 = self.player1.suggestedMove(self.gameBoard)
                self.current = self.player1.token
                winner = self.player1.token
                loser = self.player2.token
                if tempscore1>score1:
                    score1=tempscore1
            else:
                move, toMove, tempscore2 = self.player2.suggestedMove(self.gameBoard)
                self.current= self.player2.token
                winner = self.player2.token
                loser = self.player1.token
                if tempscore2>score2:
                    score2=tempscore2

                    
            #boardCopy = helper.copyBoardTree(self.gameBoard)
            self.gameBoard, moved = helper.moveToken(
                    toMove[0],
                    toMove[1],
                    move[0],
                    move[1],
                    self.gameBoard)
            #maybe checking move==toMove is redundant 
            if self.turn>=self.maxTurns or not moved:
                print("Game ended on turn "+str(self.turn-2))
                turns = self.turn-2
                self.gameNotOver = False
                    
                turnStack.pop(len(turnStack)-1)
                
                break

            #else:
                #print("Turn ", self.turn,". Player ", self.current, " moved ", toMove, move)
            #time.sleep(5)
            #helper.printCheckerBoard(self.gameBoard, helper.aligned)
           # print("scores\tplayer1: ",helper.calculateScore(self.gameBoard, self.player1.token, 0), "\n\tplayer2: ",helper.calculateScore(self.gameBoard, self.player2.token, len(self.gameBoard)-1))

            #print("")
            if self.gameNotOver: #This goes into ml algorithm, bookkeeping
                boardCopy = helper.simplifyBoardRep(self.gameBoard)
                #self.turn
                player1_score = helper.calculateScore(self.gameBoard, self.player1.token, self.player1.startingRow)
                player2_score = helper.calculateScore(self.gameBoard, self.player2.token, self.player2.startingRow)
                turnStack.append([boardCopy, self.turn, player1_score, player2_score])
            
            self.turn +=1
        helper.printCheckerBoard(self.gameBoard, helper.aligned) 
        print("Game has ended")

        return winner, score1, turns, loser, score2, turnStack




def run():
    token1 = "1"
    token2 = "2"

    board = helper.createStartingPositions(token1, token2)
    agent1 = Greedy_Agent(token1, 0)
    agent2 = Greedy_Agent(token2, len(board)-1)
    game = Game(agent1, agent2, board)
    results = game.play()

    print("Winner is player " + str(results[0]) + " with " + str(results[1]) + " points on turn " + str(results[2]) + ".\nLoser is player "+ str(results[3])+ " with "+str(results[4])+" points." )
    #print(results[5])
if __name__ == "__main__":
    run()
