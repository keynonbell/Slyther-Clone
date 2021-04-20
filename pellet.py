class pellet:
    def __init__(self, size, color, coordinates):
        self.size = size
        self.color = color
        self.coordinates = coordinates

    def getSize(self):
        return self.size

    def getColor(self):
        return self.color

    def getCoordinates(self):
        return self.coordinates

    def checkOverlap(self, minX, minY, maxX, maxY):
        if self.coordinates[0] >= minX and self.coordinates[0] <= maxX:
            if self.coordinates[1] >= minY and self.coordinates[1] <= maxY:
                return True
        return False




