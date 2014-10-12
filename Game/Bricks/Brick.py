__author__ = 'Alex_lai'

from Game.Shared import GameObject
from Game.Shared import GameConstants

class Brick(GameObject, object):

    def __init__(self, position, sprite, game):
        self.__game = game
        self.__hitPoints = 100
        self.__live = 1
        super(Brick,self).__init__(position, GameConstants.BRICK_SIZE, sprite)

    def getGame(self):
        return self.__game

    def isDestory(self):
        return self.__live <= 0

    def getHitPoints(self):
        return self.__hitPoints

    def hit(self):
        self.__live -= 1

    def getHitSound(self):
        pass

