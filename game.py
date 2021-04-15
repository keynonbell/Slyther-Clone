import random

class game:
    def __init__(self):
        self.snakes = []
        self.pellets = []
        self.numSnakes = 0
        self.numPellets = 0
        self.gridLength = 1000
        self.step = 5
        self.gameOver = False
        self.directions = ["up", "right", "down", "left"]
        self.colors = ["blue", "red", "yellow", "green", "purple", "pink", "orange", "cyan"]
        self.snakeSize = 50
        self.pelletSize = 10



    def startGame(self):
        self.createSnake(1)
        self.createPellet(50)
        while self.gameOver == False:
            for x in range(self.numSnakes):
                self.snakes[x].move(random.choice(self.directions))
            for x in range(self.numSnakes):
                for i in range(self.numSnakes):
                    if x != i:
                        if self.snakes[x].checkOverlap(self.snakes[i]) == True:
                            if x == 0:
                                self.gameOver = True
                            else:
                                del self.snakes[x]
                                self.numSnakes -= 1



    def createSnake(self, numSnakes):
        self.snakes.append(snakeHead(self.snakeSize, random.choice(self.colors), [self.gridLength/2, self.gridLength/2], self.step))
        self.numSnakes += 1
        for x in range(2, numSnakes):
            newCoordinates = [random.choice(range(self.snakeSize, self.gridLength - self.snakeSize)), random.choice(range(self.snakeSize, self.gridLength - self.snakeSize))]
            self.snakes.append(snakeHead(self.snakeSize, random.choice(self.colors), newCoordinates, self.step, random.choice(self.directions))
            self.numSnakes += 1

    def createPellet(self, numPellets):

        for x in range(numPellets):
            newCoordinates = [random.choice(range(self.pelletSize, self.gridLength - self.pelletSize)),
                              random.choice(range(self.pelletSize, self.gridLength - self.pelletSize))]
            self.pellets.append(pellet(self.pelletSize, random.choice(self.colors), newCoordinates))
            self.numPellets += 1