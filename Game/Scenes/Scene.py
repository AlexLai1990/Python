__author__ = 'Alex_lai'

class Scene():

    def __init__(self, game):
        self.__game = game
        self.__texts = []

    def render(self):
        pass

    def getGame(self):
        return self.__game

    def handleEvents(self, events):
        pass

    def clearText(self):
        self.__texts = []

    def addText(self, string, x = 0, y = 0, color = [255,255,255],
                background = [0,0,0], size = 17):
        pass




