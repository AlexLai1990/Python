__author__ = 'Alex_lai'
import  os
import fileinput  #load file
import pygame

from Game.Bricks import  *
from Game.Shared import *

class Level:

    def __init__(self, game):
        self.__game = game
        self.__bricks = []
        self.__amountOfBrickLeft = 0
        self.__currentLevel = 0

    def getBricks(self):
        return self.__bricks

    def getAmountOfBrickLeft(self):
        return self.__amountOfBrickLeft

    def brickHit(self):
        self.__amountOfBrickLeft -= 1

    def loadNextLevel(self):
        pass

    def load(self, level):
        self.__currentLevel = level
        self.__bricks = []

        x, y = 0, 0
        for line in fileinput.input(os.path.join("Assets","Levels",
                                                 "level" + str(level) + ".dat")):
            for currentBrick in line:
                if currentBrick == "1":
                    brick = Brick([x,y], pygame.image.load(GameConstants.SPIRTE_BRICK), self.__game)
                    self.__bricks.append(brick)
                    self.__amountOfBrickLeft += 1
                elif currentBrick == "2":
                    brick = Brick([x,y], pygame.image.load(GameConstants.SPIRTE_SPEEDBRICK), self.__game)
                    self.__bricks.append(brick)
                    self.__amountOfBrickLeft += 1
                elif currentBrick == "3":
                    brick = Brick([x,y], pygame.image.load(GameConstants.SPIRTE_LIFEBRICK), self.__game)
                    self.__bricks.append(brick)
                    self.__amountOfBrickLeft += 1

                x += GameConstants.BRICK_SIZE[0]

            x = 0
            y += GameConstants.BRICK_SIZE[1]

