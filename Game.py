import pygame
from Snake import Snake
from Food import Food

class Game:

    def __init__(self, width, height):
        # Set the name of the game
        pygame.display.set_caption('Snake Game')
        
        # Define width and height for the game window
        self.width = width
        self.height = height

        # Create a window for the game with width and height. In this case the 
        # height is increased by 60 pixels to add extra components
        self.gameDisplay = pygame.display.set_mode((width, height + 60))
        
        # Load the background image
        self.background = pygame.image.load('img/background.png')

        # Initilizied the flag crash. It will be used to check the status of
        # the game
        self.crash = False

        # Initilize a player
        self.player = Snake(self)
        
        # Spawn a food
        self.food = Food()

        # Initialize the score to zero
        self.score = 0
