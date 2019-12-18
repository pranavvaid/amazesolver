import numpy as np
import math
import time
import bisect

def main():
    startTime = time.clock()
    gamefield = np.array([[[0,0,0,0,0,0,0,0,2,2,0,0,0,0], # matrix representing the maze; 0 = empty space, 1 = filled space, 2 = ball current location, 3 = obstacle
                           [0,2,2,0,2,2,0,0,2,0,0,2,2,0],
                           [0,0,0,0,0,2,0,0,2,0,0,2,0,0],
                           [0,0,2,0,0,2,0,2,2,0,0,2,0,0],
                           [0,0,2,0,0,2,0,2,0,0,0,2,0,0],
                           [0,0,2,0,0,2,0,2,0,0,2,2,0,0],
                           [0,0,2,2,2,2,0,0,0,0,2,2,0,0],
                           [0,0,2,2,2,2,2,2,2,2,2,2,0,0],
                           [0,0,0,0,0,0,2,2,2,2,2,2,0,0],
                           [0,0,2,0,0,0,0,0,0,2,0,0,0,2],
                           [0,0,2,0,0,2,2,0,0,0,0,0,0,2],
                           [3,0,2,0,0,2,2,0,0,2,0,2,2,2],
                           [2,2,2,0,0,2,2,2,0,0,0,2,2,2],
                           [2,2,2,0,0,2,2,2,2,2,2,2,2,2]]])
    '''gamefield = np.array([[[0,0,0,2],
                           [0,0,0,0],
                           [3,0,2,0]]])'''
                           
    
    activeFields = gamefield # currently active gamefields
    activeMoves = np.array([[]]) # moves made by the ball to fill the gamefield. 0 = RIGHT, 1 = LEFT, 2 = UP, 3 = DOWN
    obstacles = findObstacles(gamefield[0])
    currentBall = findBall(gamefield)

    
    m = 0
    maxMoves = 100
    cullingFrequency = 3
    cullingAmount = float(2)/3
    solutionFound = False
    print(" ")
    squaresFilledByFields = []
    threshholdValue = -1
    while m < maxMoves and (not solutionFound) and activeFields.shape[0]>0:
        
        newActiveFields = [] # will store all the new gamefields after moves have been made on them
        newMoves = [] # an updated list of moves taken to reach the current gamefields
        for i in range(0, activeFields.shape[0]): # For each currently active field
            
            if m % cullingFrequency == 1 and m > 1:
                if np.count_nonzero(activeFields[i]==1) < threshholdValue:
                    continue
            
            nextMoves = determineNextMove(activeMoves, i, activeFields)
            for move in nextMoves:
                
                # Move the ball according to the next move on the current field
                ballPosition = moveBall(activeFields[i], move, obstacles)
                currentBallPosition = findBall(activeFields[i])
                squaresTraveled = abs(currentBallPosition[0]-ballPosition[0]) + abs(currentBallPosition[1]-ballPosition[1])
                fieldAfterMove = updateBallMovement(findBall(activeFields[i]), ballPosition, move, activeFields[i])
                
                
                # Update the list of moves made by the ball
                if len(activeMoves[0]) > 0:
                    newMove = np.append(activeMoves[i], move)
                else:
                    newMove = np.append(activeMoves[0], move)
            
                # Check if the ball is stuck in a recurring loop
                if squaresTraveled == 0 or checkIfInLoop(newMove, gamefield[0], fieldAfterMove, 5, obstacles):
                    pass
                else:
                    #Update the overall moves and field tracker
                    newMoves.append(newMove)
                    newActiveFields.append(fieldAfterMove)
                
                # If the gamefield is full, then break out of all the loops
                if checkIfFieldComplete(fieldAfterMove):
                    printMovesInReadableWay(newMove, m)
                    solutionFound = True
                    break # break out of move for loop
                
            if m % cullingFrequency == 0 and m>0:
                bisect.insort(squaresFilledByFields, np.count_nonzero(activeFields[i]==1))
            #squaresFilledByFields.append(np.count_nonzero(activeFields[i]==0))
            
            
            if solutionFound: # break out of activeField for loop
                break
    
        if m % cullingFrequency == 0 and m>0:
            median = int(len(squaresFilledByFields) * cullingAmount)
            threshholdValue = squaresFilledByFields[median]
        
        if m % cullingFrequency == 1 and m>1:
            squaresFilledByFields = []
            threshholdValue = -1
        if solutionFound: # break out of while loop
            break

        activeFields = np.copy(newActiveFields)
        activeMoves = np.copy(newMoves)
        m = m + 1
    if m >= maxMoves:
        print("Whomp whomp - no solutions found within " + str(maxMoves) + " moves :(")
    print(" ")
    print("TOTAL RUN TIME: " + str(time.clock() - startTime))








def findBall(field, ballValue = 3):
    #print("-------------")
    #print(field)
    #print("=============")
    a = np.where(field == ballValue)
    return [a[0][0], a[1][0]]

def moveBall(field, direction, obstacleList):
    ballLocation = findBall(field)
    limitingObstacle = None
    if direction == 0:
        limitingObstacle = [ballLocation[0], field.shape[1]]
        for obstacle in obstacleList:
            if obstacle[0] == ballLocation[0]:
                if obstacle[1] < limitingObstacle[1] and obstacle[1] > ballLocation[1]:
                    limitingObstacle = obstacle
        return([limitingObstacle[0], limitingObstacle[1]-1])
    if direction == 1:
        limitingObstacle = [ballLocation[0], -1]
        for obstacle in obstacleList:
            if obstacle[0] == ballLocation[0]:
                if obstacle[1] > limitingObstacle[1] and obstacle[1] < ballLocation[1]:
                    limitingObstacle = obstacle
        return([limitingObstacle[0], limitingObstacle[1]+1])
    if direction == 2:
        limitingObstacle = [-1, ballLocation[1]]
        for obstacle in obstacleList:
            if obstacle[1] == ballLocation[1]:
                if obstacle[0] > limitingObstacle[0] and obstacle[0] < ballLocation[0]:
                    limitingObstacle = obstacle
        return([limitingObstacle[0]+1, limitingObstacle[1]])
    if direction == 3:
        limitingObstacle = [field.shape[0], ballLocation[1]]
        for obstacle in obstacleList:
            if obstacle[1] == ballLocation[1]:
                if obstacle[0] < limitingObstacle[0] and obstacle[0] > ballLocation[0]:
                    limitingObstacle = obstacle
        return([limitingObstacle[0]-1, limitingObstacle[1]])

def updateBallMovement(originalBallPos, finalBallPos, direction, field, fillWith = 1):
    newField = np.copy(field)
    squaresAlreadyFilled = 0
    if direction == 0:
        for i in range(originalBallPos[1], finalBallPos[1]+1):
            newField[originalBallPos[0]][i] = fillWith
    if direction == 1:
        for i in range(finalBallPos[1], originalBallPos[1]+1):
            newField[originalBallPos[0]][i] = fillWith
    if direction == 2:
        for i in range(finalBallPos[0], originalBallPos[0]+1):
            newField[i][originalBallPos[1]] = fillWith
    if direction == 3:
        for i in range(originalBallPos[0], finalBallPos[0]+1):
            newField[i][originalBallPos[1]] = fillWith
    newField[finalBallPos[0]][finalBallPos[1]] = 3
    return newField

def findObstacles(field, obstacleValue = 2):
    a = np.where(field == obstacleValue)
    return(np.rot90(a))

def checkIfFieldComplete(field, emptyValue = 0):
    if emptyValue in field:
        return False
    return True


def determineNextMove(allMoves, currentGameFieldIndex, allGameFields):
    if len(allMoves[0]) > 0: # If it isn't the first move, only move perpendicular to the last move
        previousMove = allMoves[currentGameFieldIndex][-1]
        a = int((math.ceil(float((previousMove + 1))/2) * 2 + 1) % 4) # map 0 and 1 to 2 and 3
        nextMove = [a-1, a]
    else: # if its the first move, test all possible directions of movement
        nextMove = [0,1,2,3]
    return nextMove

def printMovesInReadableWay(movesToPrint, a):
    print("Solution found requiring " + str(a + 1) + " moves!")
    readableWords = []
    for move in movesToPrint:
        if move == 0:
            readableWords.append("right")
        if move == 1:
            readableWords.append("left")
        if move == 2:
            readableWords.append("up")
        if move == 3:
            readableWords.append("down")
    print(readableWords)

def checkIfInLoop(pastMoves, originalField, field, maxLoopSize, obs):
    a = 2
    while ((a*2) <= len(pastMoves)) and (a <= maxLoopSize):
        past1 = pastMoves[-a:]
        past2 = pastMoves[-2*a:-a]
        if np.array_equal(past1, past2):
            currentField = np.copy(originalField)
            for move in pastMoves[:-2*a]:
                
                bp = moveBall(currentField, move, obs)
                currentField = updateBallMovement(findBall(currentField), bp, move, currentField)
            #print(currentField)
            #print(" ")
            
            #print(field)
            if np.array_equal(currentField, field):
                return True
        a = a + 1
    return False

if __name__ == '__main__':
    main()

#IF SURROUNDED ON ALL SIDES, ONLY 1 MOVE
