import pygame
from random import randint
from utils import update_screen

class Food(object):
    
    # Initialize an object of the Food class
    def __init__(self):
        # Default values for x and y
        self.x = 240
        self.y = 200
        # Load the image for a food
        self.tile = pygame.image.load('img/food.png')

    # Display a food
    def render(self, x, y, game):
        game.gameDisplay.blit(self.tile, (x, y))
        update_screen()

    # Update a food
    def update(self, game, snake):
        # Set the food coordinates with random values
        rand_x = randint(20, game.width - 40)
        self.x = rand_x - rand_x % 20
        
        rand_y = randint(20, game.height - 40)
        self.y = rand_y - rand_y % 20

        # If snake reaches the fruit position, the function returns the fruit
        # coordinates
        if [self.x, self.y] not in snake.position:
            return self.x, self.y
        # Otherwise call recursively the update function
        else:
            self.update(game, snake)
