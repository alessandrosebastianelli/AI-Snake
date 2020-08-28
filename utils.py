import pygame
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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

# Create a plot for the model training 
def plot_training_stats(array_counter, array_score):
    sns.set(color_codes=True)
    ax = sns.regplot(
        np.array([array_counter])[0],
        np.array([array_score])[0],
        color="b",
        x_jitter=.1,
        line_kws={'color': 'green'}
    )
    ax.set(xlabel='games', ylabel='score')
    plt.show()