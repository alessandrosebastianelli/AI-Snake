import pygame
import numpy as np
from utils import eat
from utils import update_screen

class Snake(object):
    def __init__(self, game):
        # Spawn the Snake in a fixed position
        x = 0.45 * game.width
        y = 0.5  * game.height

        self.x = x - x % 20
        self.y = y - y % 20

        self.position = []
        self.position.append([self.x, self.y])

        # Set the tail lenght to 1 (Head)
        self.tail_lenght = 1
        self.eaten = False

        # Load the tiles
        self.tile = pygame.image.load('img/snakeBody.png')
        self.tile_headN = pygame.image.load('img/snakeHeadN.png')
        self.tile_headS = pygame.image.load('img/snakeHeadS.png')
        self.tile_headE = pygame.image.load('img/snakeHeadE.png')
        self.tile_headW = pygame.image.load('img/snakeHeadW.png')

        # Set the initial x velocity to 20 (or y velocity to 20)
        self.x_change = 20
        self.y_change = 0

    # Display or Render the Snake
    def render(self, x, y, tail_lenght, game):
        self.position[-1][0] = x
        self.position[-1][1] = y

        # If the game is not crashed, render Snake and the tail
        if game.crash == False:
            
            # Display the head with different rotation
            x_temp, y_temp = self.position[len(self.position)-1]

            if self.x_change == 20:
                game.gameDisplay.blit(self.tile_headE, (x_temp, y_temp))
            elif self.x_change == -20: 
                game.gameDisplay.blit(self.tile_headW, (x_temp, y_temp))
            elif self.y_change == -20:
                game.gameDisplay.blit(self.tile_headN, (x_temp, y_temp))
            elif self.y_change == 20:
                game.gameDisplay.blit(self.tile_headS, (x_temp, y_temp))

            # Display the tail
            for i in range(1, tail_lenght):
                x_temp, y_temp = self.position[len(self.position)-1-i]
                game.gameDisplay.blit(self.tile, (x_temp, y_temp))

            update_screen()
        else:
            pygame.time.wait(300)
    
    # Update the Snake position
    def update(self, x, y):
        if self.position[-1][0] != x or self.position[-1][1] != y:
            # Update the tail
            if self.tail_lenght > 1:
                for i in range(0, self.tail_lenght - 1):
                    self.position[i][0], self.position[i][1] = self.position[i + 1]
                    
            self.position[-1][0] = x
            self.position[-1][1] = y
   
    # Update the Snake position
    def move(self, move, x, y, game, food, agent):
        move_array = [self.x_change, self.y_change]
        
        # Increment the tail if Snake eats a fruit
        if self.eaten:
            self.position.append([self.x, self.y])
            self.eaten = False
            self.tail_lenght = self.tail_lenght + 1

        # Set the x and y velocity based on the input <move>
        if np.array_equal(move, [1, 0, 0]):
            move_array = self.x_change, self.y_change                 # Same
        elif np.array_equal(move, [0, 1, 0]) and self.y_change == 0:  # Right
            move_array = [0, self.x_change]
        elif np.array_equal(move, [0, 1, 0]) and self.x_change == 0:  # Down
            move_array = [-self.y_change, 0]
        elif np.array_equal(move, [0, 0, 1]) and self.y_change == 0:  # Left
            move_array = [0, -self.x_change]
        elif np.array_equal(move, [0, 0, 1]) and self.x_change == 0:  # Up
            move_array = [self.y_change, 0]
        
        self.x_change, self.y_change = move_array
        self.x = x + self.x_change
        self.y = y + self.y_change

        # Borders collision
        if self.x < 20 or self.x > game.width - 40 \
                or self.y < 20 \
                or self.y > game.height - 40 \
                or [self.x, self.y] in self.position:
            game.crash = True


        eat(self, food, game)
        self.update(self.x, self.y)
