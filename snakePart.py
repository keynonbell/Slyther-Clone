from pellet import *



class snakePart:
    def __init__(self, size, color, coordinates, step=1, direction="up"):
        self.size = size
        self.color = color
        self.coordinates = coordinates
        self.step = step
        self.direction = direction
        self.target = [0,0]
        self.target[0] = coordinates[0]
        self.target[1] = coordinates[1]

    def getCoordinates(self):
        return self.coordinates

    def getSize(self):
        return self.size

    def getColor(self):
        return self.color

    def getStep(self):
        return self.step

    def move(self, direction):
        if direction == "up":
            self.coordinates[1] += self.step
            self.direction = direction

        if direction == "right":
            self.coordinates[0] += self.step
            self.direction = direction

        if direction == "down":
            self.coordinates[1] -= self.step
            self.direction = direction

        if direction == "left":
            self.coordinates[0] -= self.step
            self.direction = direction

    def getDirection(self):
        return self.direction

    def setDirection(self, direction):
        self.direction = direction

    def getTarget(self):
        return self.target

    def setTarget(self, target):
        self.target[0] = target[0]
        self.target[1] = target[1]

    def setStep(self, step):
        self.step = step

    def setCoordinates(self, coordinates):
        self.coordinates[0] = coordinates[0]
        self.coordinates[1] = coordinates[1]

    def checkOverlap(self, minX, minY, maxX, maxY):
        myMinX = self.coordinates[0] - self.size / 2
        myMinY = self.coordinates[1] - self.size / 2
        myMaxX = self.coordinates[0] + self.size / 2
        myMaxY = self.coordinates[1] + self.size / 2

        # i'm above them
        if myMinY > maxY:
            return False
        # I'm below them
        if myMaxY < minY:
            return False
        # I'm to the right
        if myMinX > maxX:
            return False
        # I'm to the left
        if myMaxX < minX:
            return False
        # else intersect
        return True


class snakeHead:
    def __init__(self, size, color, coordinates, step=1, direction='up', length=0):
        self.size = size
        self.color = color
        self.coordinates = coordinates
        self.step = step
        self.direction = direction
        self.parts = []
        self.length = length
        self.points = 0
        if self.length != 0:
            self.grow(self.length)

    def getDimensions(self):
        myMinX = self.coordinates[0] - self.size / 2
        myMinY = self.coordinates[1] - self.size / 2
        myMaxX = self.coordinates[0] + self.size / 2
        myMaxY = self.coordinates[1] + self.size / 2
        return [myMinX, myMinY, myMaxX, myMaxY]


    def oppositeDirection(self, direction):
        if direction == 'up':
            return 'down'
        if direction == 'down':
            return 'up'
        if direction == 'left':
            return 'right'
        if direction == 'right':
            return 'left'

    def getCoordinates(self):
        return self.coordinates

    def getSize(self):
        return self.size

    def getLength(self):
        return self.length

    def getParts(self):
        return self.parts

    def getColor(self):
        return self.color

    def getDirection(self):
        return self.direction

    def setDirection(self, newDirection):
        if newDirection != self.oppositeDirection(self.direction):
            self.direction = newDirection


    def checkOverlap(self, enemyHead):
        enemyMinX = enemyHead.coordinates[0] - (enemyHead.length + 1) * enemyHead.size
        enemyMaxX = enemyHead.coordinates[0] + (enemyHead.length + 1) * enemyHead.size
        enemyMinY = enemyHead.coordinates[1] - (enemyHead.length + 1) * enemyHead.size
        enemyMaxY = enemyHead.coordinates[1] + (enemyHead.length + 1) * enemyHead.size
        if self.coordinates[0] > enemyMinX and self.coordinates[0] < enemyMaxX and self.coordinates[1] > enemyMinY and self.coordinates[1] < enemyMaxY:
            head = self.getDimensions()
            if enemyHead.length == 0:
                return True

            for x in enemyHead.parts:
                if x.checkOverlap(head[0], head[1], head[2], head[3]):
                    return True
        return False

    def move(self):

        if self.direction == "up":
            self.coordinates[1] += self.step
        elif self.direction == "right":
            self.coordinates[0] += self.step
        elif self.direction == "down":
            self.coordinates[1] -= self.step
        elif self.direction == "left":
            self.coordinates[0] -= self.step

        for x in range(self.length):
            C = self.parts[x].getCoordinates()
            T = self.parts[x].getTarget()

            if x == 0:
                L = self.coordinates
            else:
                L = self.parts[x-1].getCoordinates()

            if abs(C[0]-T[0]) < self.parts[x].getStep() and abs(C[1]-T[1]) < self.parts[x].getStep():
                self.parts[x].setCoordinates(T)
                C = self.parts[x].getCoordinates()
                if x == 0:
                    self.parts[x].setTarget(self.coordinates)
                else:
                    self.parts[x].setTarget([self.parts[x-1].getCoordinates()[0], self.parts[x-1].getCoordinates()[1]])
                T = self.parts[x].getTarget()

            #changes speed to remove gaps and overlaps
            if abs(C[0]-L[0]) < self.parts[x].getSize() and abs(C[1]-L[1]) < self.parts[x].getSize():
                self.parts[x].setStep(self.step / 2)
            elif abs(C[0]-L[0]) > self.parts[x].getSize() or abs(C[1]-L[1]) > self.parts[x].getSize():
                self.parts[x].setStep(self.step * 2)
            else:
                self.parts[x].setStep(self.step)

            #check for whether a part is within 1 step of an adjacent part
            if C[0] < T[0] and abs(C[0]-T[0]) >= self.parts[x].getStep():
                self.parts[x].move("right")
            elif C[0] > T[0] and abs(C[0]-T[0]) >= self.parts[x].getStep():
                self.parts[x].move("left")
            elif C[1] < T[1] and abs(C[1]-T[1]) >= self.parts[x].getStep():
                self.parts[x].move("up")
            else:
                self.parts[x].move("down")


    def eat(self, pellet):
        dims = self.getDimensions()
        if not pellet.checkOverlap(dims[0],dims[1],dims[2],dims[3]):
            return False
        if self.color == pellet.getColor():
            self.points += 5
        else:
            self.points += 1
        if self.points >= 6:
            self.grow(2)
            self.points -= 6
        elif self.points >= 3:
            self.grow()
            self.points -= 3
        return True

    def grow(self, parts=1):
        for x in range(parts):
            if self.length == 0:
                lastItem = self.coordinates
                lastDirection = self.direction
            else:
                lastItem = self.parts[-1].getCoordinates()
                lastDirection = self.parts[-1].getDirection()
            if lastDirection == "up":
                newCoordinates = [lastItem[0], lastItem[1] - 0.75*self.size]
            elif lastDirection == "right":
                newCoordinates = [lastItem[0] - 0.75*self.size, lastItem[1]]
            elif lastDirection == "down":
                newCoordinates = [lastItem[0], lastItem[1] + 0.75*self.size]
            else:
                newCoordinates = [lastItem[0] + 0.75*self.size, lastItem[1]]

            self.parts.append(snakePart(0.75*self.size, self.color, newCoordinates, self.step, lastDirection))
            self.length += 1
