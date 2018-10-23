import chinesecheckers as helper
import time

class Greedy_Agent():
    def __init__(self, token, startingRow):
        self.startingRow = startingRow
        self.token = token
        

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
                    listOfMoveDicts.append(moves)
        
        highest_delta = 0
        suggestedMove = (-1, -1)
        origin = (-1, -1)
        for moves in listOfMoveDicts:
            for move in moves.keys():

                temp = matrix
                scoreBefore = helper.calculateScore(temp, self.token, self.startingRow)

                temp = helper.moveToken(move[0], move[1], moves[move][0].r, moves[move][0].c, temp)
                scoreAfter = helper.calculateScore(temp, self.token, self.startingRow)
                
                delta = scoreAfter #- scoreBefore
                print("delta is", delta)

                moves[move][1] = delta
            
                if delta > highest_delta:
                    highest_delta = delta
                    suggestedMove = move
                    origin = moves[move][0]

            if (suggestedMove == (-1, -1)):
                #print("No moves to make for player ", self.token)
                return (0,0), (0,0)
        return suggestedMove, (origin.r, origin.c)

    
            
class Game():
    def __init__(self, agent1, agent2, board):
        self.player1 = agent1
        self.player2 = agent2
        self.gameBoard = board
        self.gameNotOver = True
        self.turn = 1
        self.winner = "3"
        self.maxTurns = 5

    
    def play(self):
        print("Initial Board ")
        helper.printCheckerBoard(self.gameBoard, helper.aligned)
        print("")

        while self.gameNotOver:
            move = (0, 0)
            toMove = (0, 0)

            if self.turn%2 != 0:
                move, toMove = self.player1.suggestedMove(self.gameBoard)
                self.winner = self.player1.token

            else:
                move, toMove = self.player2.suggestedMove(self.gameBoard)
                self.winner= self.player2.token

            if move == toMove or self.turn>self.maxTurns:
                print("Gameover is set on turn "+str(self.turn))
                self.gameNotOver = False
                #break

            self.gameBoard = helper.moveToken(
                    toMove[0],
                    toMove[1],
                    move[0],
                    move[1],
                    self.gameBoard)

            helper.printCheckerBoard(self.gameBoard, helper.aligned)
            print(self.winner, " moved ", toMove, move)
            print("scores\tplayer1: ",helper.calculateScore(self.gameBoard, self.player1.token, 0), "\n\tplayer2: ",helper.calculateScore(self.gameBoard, self.player2.token, len(self.gameBoard)-1))

            print("")
            
            self.turn +=1

        print("Game has ended")




def run():
    token1 = "1"
    token2 = "2"

    board = helper.createStartingPositions(token1, token2)
    agent1 = Greedy_Agent(token1, 0)
    agent2 = Greedy_Agent(token2, len(board)-1)
    game = Game(agent1, agent2, board)
    game.play()

if __name__ == "__main__":
    run()
