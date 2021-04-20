import random
from snakePart import *

class game:
    def __init__(self):
        self.snakes = []
        self.pellets = []
        self.numSnakes = 0
        self.numPellets = 0
        self.gridLength = 10000
        self.step = 5
        self.gameOver = False
        self.directions = ["up", "right", "down", "left"]
        self.colors = ["blue", "red", "yellow", "lime green", "purple", "pink", "orange", "cyan"]
        self.snakeSize = 50
        self.pelletSize = 10
        self.minPellets = 5000
        self.createSnake(5)
        self.createPellet(2*self.minPellets)



    def playGame(self):


        for x in range(self.numSnakes):
            if x == 0:
                self.snakes[0].move(self.snakes[0].getDirection())
            else:
                self.snakes[x].move(random.choice(self.directions))
        for x in range(self.numSnakes):
            for i in range(self.numSnakes):
                if x != i and x < len(self.snakes) and i < len(self.snakes):
                    if self.snakes[x].checkOverlap(self.snakes[i]) == True:
                        if x == 0:
                            self.gameOver = True
                            return True
                        else:
                            del self.snakes[x]
                            self.numSnakes -= 1
        for snake in self.snakes:
            for pellet in self.pellets:
                if snake.eat(pellet) == True:
                    self.pellets.remove(pellet)
                    self.numPellets -= 1
        if self.numPellets <= self.minPellets:
            self.createPellet(self.minPellets - self.numPellets)
        return False

    def getSnakes(self):
        return self.snakes
    def getPellets(self):
        return self.pellets

    def createSnake(self, numSnakes):
        self.snakes.append(snakeHead(self.snakeSize, random.choice(self.colors), [self.gridLength/2, self.gridLength/2], self.step))
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