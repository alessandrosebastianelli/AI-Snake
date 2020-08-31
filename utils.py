import pygame
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import interpolate

# Function that implements the eating action
def eat(player, food, game):
    # If the snake position is equal to a fruit position
    if player.x == food.x and player.y == food.y:
        # Generate a new fruit
        food.update(game, player)
        # Set the eaten flag to True
        player.eaten = True
        # Increment the score counter by 1
        game.score = game.score + 1

# Update the screen
def update_screen():
    pygame.display.update()
    # This is needed for Mac users
    pygame.event.get()

# Get the record
def get_record(score, record):
    if score >= record:
        return score
    else:
        return record

def plot_training_stats(array_counter, array_score, epochs):
    x = np.array([array_counter])[0]
    y = np.array([array_score])[0]

    xvals = np.arange(0, epochs-1, 0.1) # np.linspace(0, len(y), len(y))
    #yinterp = np.interp(xvals, x, y)
    f = interpolate.interp1d(x, y)
    yinterp = f(xvals)

    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (10, 10))    
    ax.plot(x, y, '*', color = 'r', label = 'Score values')
    ax.plot(xvals, yinterp, '-', color = 'b', label = 'Mean value')
    ax.set(xlabel='Games', ylabel='Score')
    ax.legend()
    plt.show()