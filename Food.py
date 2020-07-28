import pygame
from random import randint
from utils import update_screen

class Food(object):
    def __init__(self):
        self.x = 240
        self.y = 200
        self.tile = pygame.image.load('img/food.png')

    def render(self, x, y, game):
        game.gameDisplay.blit(self.tile, (x, y))
        update_screen()

    def update(self, game, snake):
        rand_x = randint(20, game.width - 40)
        self.x = rand_x - rand_x % 20

        rand_y = randint(20, game.height - 40)
        self.y = rand_y - rand_y % 20

        if [self.x, self.y] not in snake.position:
            return self.x, self.y
        else:
            self.update(game, snake)
