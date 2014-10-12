__author__ = 'Alex_lai'
import pygame
from Game.Shared import GameObject
from Game.Shared import GameConstants

class Ball(GameObject, object):

    def __init__(self, position, sprite, game):
        self.__game = game
        self.__speed = 2
        self.__incrememt = [2, 2]
        self.__direction = [1, 1]
        self.__inMotion = 0

        super(Ball, self).__init__(position, GameConstants.BALL_SIZE, sprite)

    def setSpeed(self, newSpeed):
        self.__speed = newSpeed

    def resetSpeed(self):
        self.setSpeed(3)

    def getSpeed(self):
        return self.__speed

    def isInMotion(self):
        return self.__inMotion

    def setMotion(self, isMoving):
        self.__inMotion = isMoving
        self.resetSpeed()

    def changeDircetion(self, gameObject):
        position = self.getPosition()
        size = self.getSize()
        objectPosition = gameObject.getPosition()
        objectSize = gameObject.getSize()

        # hit bottom
        if position[1] > objectPosition[1] and \
            position[1] < objectPosition[1] + objectSize[1] and \
            position[0] > objectPosition[0] and \
            position[0] < objectPosition[0] + objectSize[0]:

            self.setPosition((position[0], objectPosition[1] + objectSize[1]))
            self.__direction[1] *= -1

        # hit top
        elif position[1] + size[1] > objectPosition[1] and \
                position[1] + size[1] < objectPosition[1] + objectSize[1] and\
             position[0] > objectPosition[0] and\
                position[0] < objectPosition[0] + objectSize[0] :

            self.setPosition((position[0], objectPosition[1] - objectSize[1]))
            self.__direction[1] *= -1

        # hit left
        elif position[0] + size[0] > objectPosition[0] and \
                position[0] + size[0] < objectPosition[0] + objectSize[0]:
            self.setPosition((objectPosition[0] - size[0], position[1]))
            self.__direction[0] *= -1

        # hit right
        else:
            self.setPosition((objectPosition[0] + objectSize[0], position[1]))
            self.__direction[0] *= -1
            #self.__direction[1] *= -1


    def updatePosition(self):
        #  self.setPosition(pygame.mouse.get_pos())
        position = self.getPosition()
        size = self.getSize()

        newPosition = [position[0] + (self.__incrememt[0] * self.__speed) * self.__direction[0],
                       position[1] + (self.__incrememt[1] * self.__speed) * self.__direction[1] ]

        if newPosition[0] <= 0:
            self.__direction[0] *= -1
            newPosition[0] = 0
        if newPosition[0] + size[0] >= GameConstants.SCREEN_SIZE[0] :
            self.__direction[0] *= -1
            newPosition[0] = GameConstants.SCREEN_SIZE[0] - size[0]
        if newPosition[1] <= 0:
            self.__direction[1] *= -1
            newPosition[1] = 0
        if newPosition[1] + size[1] >= GameConstants.SCREEN_SIZE[1] :
            self.__direction[1] *= -1
            newPosition[1] = GameConstants.SCREEN_SIZE[1] - size[1]

        self.setPosition(newPosition)

    def isBallDead(self):
        pass
