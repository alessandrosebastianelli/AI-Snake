import pygame
import numpy as np

from utils import eat
from utils import update_screen

class Snake(object):
    def __init__(self, game):
        x = 0.45 * game.width
        y = 0.5  * game.height

        self.x = x - x % 20
        self.y = y - y % 20

        self.position = []
        self.position.append([self.x, self.y])

        self.tail_lenght = 1
        self.eaten = False
        self.tile = pygame.image.load('img/snake.png')

        self.x_change = 20
        self.y_change = 0

    def render(self, x, y, tail_lenght, game):
        self.position[-1][0] = x
        self.position[-1][1] = y

        if game.crash == False:
            for i in range(tail_lenght):
                x_temp, y_temp = self.position[len(self.position)-1-i]
                game.gameDisplay.blit(self.tile, (x_temp, y_temp))

            update_screen()
        else:
            pygame.time.wait(300)
    
    def update(self, x, y):
        if self.position[-1][0] != x or self.position[-1][1] != y:
            if self.tail_lenght > 1:
                for i in range(0, self.tail_lenght - 1):
                    self.position[i][0], self.position[i][1] = self.position[i + 1]
            self.position[-1][0] = x
            self.position[-1][1] = y
   
    def move(self, move, x, y, game, food, agent):
        move_array = [self.x_change, self.y_change]

        if self.eaten:
            self.position.append([self.x, self.y])
            self.eaten = False
            self.tail_lenght = self.tail_lenght + 1

        if np.array_equal(move, [1, 0, 0]):
            move_array = self.x_change, self.y_change
        elif np.array_equal(move, [0, 1, 0]) and self.y_change == 0:  # right - going horizontal
            move_array = [0, self.x_change]
        elif np.array_equal(move, [0, 1, 0]) and self.x_change == 0:  # right - going vertical
            move_array = [-self.y_change, 0]
        elif np.array_equal(move, [0, 0, 1]) and self.y_change == 0:  # left - going horizontal
            move_array = [0, -self.x_change]
        elif np.array_equal(move, [0, 0, 1]) and self.x_change == 0:  # left - going vertical
            move_array = [self.y_change, 0]
        
        self.x_change, self.y_change = move_array
        self.x = x + self.x_change
        self.y = y + self.y_change

        if self.x < 20 or self.x > game.width - 40 \
                or self.y < 20 \
                or self.y > game.height - 40 \
                or [self.x, self.y] in self.position:
            game.crash = True
        eat(self, food, game)

        self.update(self.x, self.y)
