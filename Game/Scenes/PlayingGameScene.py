__author__ = 'Alex_lai'
import pygame

from Game.Scenes.Scene import Scene

# if we want the derive class to use the base class function.
class PlayingGameScene(Scene, object):
    def __int__(self, game):
        super(PlayingGameScene, self).__init__(game)

    def handleEvents(self, events):
        super(PlayingGameScene, self).handleEvents(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()

    def render(self):
        super(PlayingGameScene, self).render()
        game = self.getGame()

        balls = game.getBalls()
        for ball in balls:
            # check all brick
            for ball2 in balls:
                if ball != ball2 and ball.intersects(ball2):
                    ball.changeDircetion(ball2)

            for brick in game.getLevel().getBricks():
                if not brick.isDestory() and ball.intersects(brick):
                    brick.hit()
                    ball.changeDircetion(brick)
                    print("intersect!")
                    break # can only hit one brick each time

            ball.updatePosition()
            game.screen.blit(ball.getSprite(), ball.getPosition())

        for brick in game.getLevel().getBricks():
            if not brick.isDestory():
                game.screen.blit(brick.getSprite(),brick.getPosition())

