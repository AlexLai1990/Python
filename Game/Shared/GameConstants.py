__author__ = 'Alex_lai'
import os

class GameConstants:
    SCREEN_SIZE = [800, 600]
    BRICK_SIZE = [100, 30]
    BALL_SIZE = [60, 60]
    PAD_SIZE = [130, 13]

    # load ball image
    SPIRTE_BALL = os.path.join("Assets", "ball.png")
    SPIRTE_BRICK = os.path.join("Assets", "standard.png")
    SPIRTE_SPEEDBRICK = os.path.join("Assets", "speed.png")
    SPIRTE_LIFEBRICK = os.path.join("Assets", "life.png")
