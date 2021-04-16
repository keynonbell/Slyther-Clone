import tkinter as tk
from game import *
import time

class UI:

    def __init__(self):
        self.windowSize = 1000
        self.window = tk.Tk()
        self.window.title("snake game")
        self.frame1 = tk.Frame(master=self.window, width=200, bg="grey")
        self.frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.frame2 = tk.Frame(master=self.window, width=1000, height=1000, bg="white")
        self.frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.canvas = tk.Canvas(master=self.frame2)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.gameOver = False
        self.game = game()
        self.startGame()
        self.window.mainloop()

    def startGame(self):
        if self.gameOver == False:
            self.drawMap()
            self.game.playGame()
            self.window.after(30, self.startGame)

    def drawMap(self):
        self.canvas.delete("all")
        playerX = self.game.getSnakes()[0].getCoordinates()[0]
        playerY = self.game.getSnakes()[0].getCoordinates()[1]
        originX = playerX - self.windowSize/2
        originY = playerY - self.windowSize/2
        originMaxX = playerX + self.windowSize/2
        originMaxY = playerY + self.windowSize / 2
        pellets = self.game.getPellets()
        for p in pellets:
            if p.checkOverlap(originX,originY,originMaxX,originMaxY):
                relativeX = p.getCoordinates()[0] - originX - p.getSize()/2
                relativeY = p.getCoordinates()[1] - originY - p.getSize()/2
                self.canvas.create_rectangle(relativeX, relativeY, relativeX + p.getSize(), relativeY + p.getSize(), fill=p.getColor())
        self.canvas.pack()
        print("map drawn")