import tkinter as tk
from game import *
from PIL import ImageTk, Image

class UI:

    def __init__(self):
        '''
        This init initializes the UI for playing the game and everything required to do so. It makes the play area window,
        the stats collumn and all the stats, as well as the start game and game over functions.
        '''
        self.windowSize = 1000
        self.window = tk.Tk()
        self.window.title("snakes on a plane")
        self.frame1 = tk.Frame(master=self.window, width=100, bg="grey")
        self.frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.frame2 = tk.Frame(master=self.window, width=1000, height=1000, bg="white")
        self.frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.size = tk.StringVar()
        self.kills = tk.StringVar()
        self.snack = tk.StringVar()
        self.count = tk.StringVar()
        self.lengthLabel = tk.Label(master=self.frame1, textvariable=self.size)
        self.lengthLabel.pack()
        self.pelletsLabel = tk.Label(master=self.frame1, textvariable=self.snack)
        self.pelletsLabel.pack()
        self.killsLabel = tk.Label(master=self.frame1, textvariable=self.kills)
        self.killsLabel.pack()
        self.countLabel = tk.Label(master=self.frame1, textvariable=self.count)
        self.countLabel.pack()
        self.canvas = tk.Canvas(master=self.frame2, height=1000, width=1000)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.gameOver = False
        self.window.bind("<Key>", self.keyPressed)
        self.game = game(self.windowSize)
        self.startGame()
        self.window.mainloop()

    def startGame(self):
        #game will continue playing until you lose, in which case the game will restart when the "Game Over" screen is closed
        if self.gameOver == False:
            self.drawMap()
            self.gameOver = self.game.playGame()
            self.size.set("Snake Length: " + str(self.game.getSnakes()[0].getLength()))
            self.kills.set("Snakes Killed: " + str(self.game.getSnakesKilled()))
            self.snack.set("Pellets Eaten: " + str(self.game.getPelletsEaten()))
            self.count.set("Enemy Snakes: " + str(self.game.getNumSnakes()))

        else:
            popUpWindow = tk.Toplevel(self.window)
            img = ImageTk.PhotoImage(Image.open('gameover.jpg'))
            newCanvas = tk.Canvas(master=popUpWindow, width=626, height=626)
            newCanvas.create_image(313,313, image=img)
            newCanvas.pack()
            self.window.wait_window(popUpWindow)
            self.gameOver = False
            self.game.restartGame()

        self.window.after(1, self.startGame)

    def keyPressed(self, event):
        #Converts arrow key presses into movement directions the snake head can understand
        if event.keysym_num == 65364:  #up
            self.game.getSnakes()[0].setDirection("up")
        elif event.keysym_num == 65363: #right
            self.game.getSnakes()[0].setDirection("right")
        elif event.keysym_num == 65362: #down
            self.game.getSnakes()[0].setDirection("down")
        elif event.keysym_num == 65361: #left
            self.game.getSnakes()[0].setDirection("left")



    def drawMap(self):
        '''
        This function essentially makes the entire playable area which is populated by snakes and pellets. It also creates a
        window which will only show a fraction of the total map inside the pop-window. Other pellets and snakes
        not currently shown on the screen are still on the map, but the snakes are not moving.
        '''
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

        #The color here is arbitary, but this sets your snake as the center of the window and draws snakes that are within that window
        windowSnake = snakeHead(self.windowSize, "blue", [playerX, playerY])
        for s in self.game.getSnakes():
            if s.checkOverlap(windowSnake):
                relativeX = s.getCoordinates()[0] - originX - s.getSize()/2
                relativeY = s.getCoordinates()[1] - originY - s.getSize()/2
                self.canvas.create_rectangle(relativeX, relativeY, relativeX + s.getSize(), relativeY + s.getSize(),
                                             fill=s.getColor())
                p = s.getParts()
                for part in p:
                    relativeX = part.getCoordinates()[0] - originX - part.getSize() / 2
                    relativeY = part.getCoordinates()[1] - originY - part.getSize() / 2
                    self.canvas.create_rectangle(relativeX, relativeY, relativeX + part.getSize(), relativeY + part.getSize(),
                                                 fill=part.getColor())
        self.canvas.pack()
