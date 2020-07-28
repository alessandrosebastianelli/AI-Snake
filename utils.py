import pygame

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
