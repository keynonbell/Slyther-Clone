import random
from snakePart import *

class game:
    def __init__(self, windowSize):
        self.windowSize = windowSize
        self.snakes = []
        self.pellets = []
        self.numSnakes = 0
        self.numPellets = 0
        self.snakesKilled = 0
        self.pelletsEaten = 0
        self.gridLength = 20000
        self.step = 5
        self.gameOver = False
        self.directions = ["up", "right", "down", "left"]
        self.colors = ["blue", "red", "yellow", "lime green", "purple", "pink", "orange", "cyan"]
        self.snakeSize = 50
        self.pelletSize = 10
        self.minPellets = 10000
        self.startingSnakes = 20
        self.restartGame()

    def getNumSnakes(self):
        return self.numSnakes

    def getSnakesKilled(self):
        return self.snakesKilled

    def getPelletsEaten(self):
        return self.pelletsEaten

    def restartGame(self):
        self.numSnakes = 0
        self.numPellets = 0
        self.pelletsEaten = 0
        self.snakesKilled = 0
        self.gameOver = False
        self.snakes.clear()
        self.pellets.clear()
        self.createSnake(self.startingSnakes)
        self.createPellet(2 * self.minPellets)

    def playGame(self):

        # check for out of map error
        playerS = self.snakes[0].getCoordinates()
        if playerS[0] <= 0 or playerS[0] >= self.gridLength or playerS[1] <= 0 or playerS[1] >= self.gridLength:
            self.gameOver = True
            return True

        for x in range(self.numSnakes):
            if x >= len(self.snakes):
                break

            playerX = self.snakes[0].getCoordinates()[0]
            playerY = self.snakes[0].getCoordinates()[1]
            windowSnake = snakeHead(self.windowSize / 2, "blue", [playerX, playerY])
            if self.snakes[x].checkOverlap(windowSnake) == False: # does not overlap with window, don't move this snake
                continue

            if x != 0:
                self.snakes[x].setDirection(random.choice(self.directions))
            self.snakes[x].move()

            for pellet in self.pellets:
                if self.snakes[x].eat(pellet) == True:
                    self.pellets.remove(pellet)
                    self.numPellets -= 1
                    if x == 0:
                        self.pelletsEaten += 1

            for i in range(self.numSnakes):
                if x != i and x < len(self.snakes) and i < len(self.snakes):
                    if self.snakes[i].checkOverlap(windowSnake) == False:
                        continue
                    if self.snakes[x].checkOverlap(self.snakes[i]) == True:
                        if x == 0:
                            self.gameOver = True
                            return True
                        else:
                            del self.snakes[x]
                            self.numSnakes -= 1
                            if i == 0:
                                self.snakesKilled += 1

        if self.numPellets <= self.minPellets:
            self.createPellet(self.minPellets - self.numPellets)
        return False

    def getSnakes(self):
        return self.snakes

    def getPellets(self):
        return self.pellets

    def createSnake(self, numSnakes):
        if self.numSnakes == 0:
            newLen = 0
        else:
            newLen = random.randint(30, 100)
        self.snakes.append(snakeHead(self.snakeSize, random.choice(self.colors), [self.gridLength/2, self.gridLength/2], self.step, length=newLen))
        self.numSnakes += 1
        for x in range(2, numSnakes):
            newCoordinates = [random.choice(range(self.snakeSize, self.gridLength - self.snakeSize)), random.choice(range(self.snakeSize, self.gridLength - self.snakeSize))]
            self.snakes.append(snakeHead(self.snakeSize, random.choice(self.colors), newCoordinates, self.step, random.choice(self.directions)))
            self.numSnakes += 1

    def createPellet(self, numPellets):
        for x in range(numPellets):
            newCoordinates = [random.choice(range(self.pelletSize, self.gridLength - self.pelletSize)),
                              random.choice(range(self.pelletSize, self.gridLength - self.pelletSize))]
            self.pellets.append(pellet(self.pelletSize, random.choice(self.colors), newCoordinates))
            self.numPellets += 1
