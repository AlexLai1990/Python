__author__ = 'Alex_lai'

from Game.Shared import GameObject
from Game.Shared import GameConstants

class Pad(GameObject, object):

    def __init__(self, position, sprite):
        super(Pad, self).__init__(position, GameConstants.PAD_SIZE, sprite)
