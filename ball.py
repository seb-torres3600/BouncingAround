import random


class Ball:
    
    def __init__(self, side, color):
        self.x_speed = random.randint(30,50)
        self.y_speed = random.choice(list(range(-50, -30)) + list(range(30, 50)))
        self.color = color
        self.side = side
        self.ball = None
        