import pygame

def eat(player, food, game):
    if player.x == food.x and player.y == food.y:
        food.update(game, player)
        player.eaten = True
        game.score = game.score + 1

def update_screen():
    pygame.display.update()
    pygame.event.get()
