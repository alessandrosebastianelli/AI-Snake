import os
import pygame
import argparse
import numpy as np
from Agent import Agent
from random import randint
from keras.utils import to_categorical

from Game import Game
from Snake import Snake
from Food import Food
from utils import get_record, update_screen, plot_training_stats

#---------------------------------------
#                  GUI
#---------------------------------------

def display_ui(game, score, record, generation):
    # Define fonts
    myfont = pygame.font.SysFont('Segoe UI', 30)
    myfont_bold = pygame.font.SysFont('Segoe UI', 30, True)
    text_score = myfont.render('Current score: ', True, (0, 0, 0))
    text_score_number = myfont_bold.render(str(score), True, (0, 0, 0))
    text_highest = myfont.render('Best score: ', True, (0, 0, 0))
    text_highest_number = myfont_bold.render(str(record), True, (0, 0, 0))
    text_generation = myfont.render('Generation n: ', True, (0, 0, 0))
    text_generation_number = myfont_bold.render(str(generation), True, (0, 0, 0))
    # Render the text for the scores
    game.gameDisplay.blit(text_generation, (20, 440)) 
    game.gameDisplay.blit(text_generation_number, (180, 440)) 
    game.gameDisplay.blit(text_score, (240, 440)) # 20 470 
    game.gameDisplay.blit(text_score_number, (400, 440)) # 200 470
    game.gameDisplay.blit(text_highest, (240, 470))
    game.gameDisplay.blit(text_highest_number, (400, 470))

    # Render the background
    game.gameDisplay.blit(game.background, (10, 10))

def display(player, food, game, record, generation):
    game.gameDisplay.fill((255, 255, 255))
    display_ui(game, game.score, record, generation)
    player.render(player.position[-1][0], player.position[-1][1], player.tail_lenght, game)
    food.render(food.x, food.y, game)

#---------------------------------------
#            Model parameters
#---------------------------------------

def define_parameters():
    params = dict()
    params['epsilon_decay_linear'] = 1/75
    params['lr'] = 0.0005
    params['firstLayer_dim'] = 100  #150   
    params['secondLayer_dim'] = 100 #150  
    params['thirdLayer_dim'] = 100  #150   
    params['dropout'] = True
    params['dropoutValue'] = 0.3
    params['epochs'] = 150           
    params['memory_size'] = 2500 
    params['batch_size'] = 500 
    params['weights_save_path'] = 'weights/weights.hdf5'
    params['load_weights'] = False
    params['train'] = True
    return params

def initialize_game(player, game, food, agent, batch_size):
    state_init1 = agent.get_state(game, player, food)  # [0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0]
    action = [1, 0, 0]
    player.move(action, player.x, player.y, game, food, agent)
    state_init2 = agent.get_state(game, player, food)
    reward1 = agent.set_reward(player, game.crash)

    # New update - memory
    agent.remember(state_init1, action, reward1, state_init2, game.crash)
    agent.replay_new(agent.memory, batch_size)

#---------------------------------------
#            Game main loop
#---------------------------------------
def main_game_loop(display_option, speed, params):
    # Initialize the pygame library
    pygame.init()
    # Create the Agent with the parameters dictionary
    agent = Agent(params)
    # Load weights
    weights_filepath = params['weights_save_path']
    if params['load_weights']:
        agent.network.load_weights(weights_filepath)
        print("weights loaded")

    counter_games = 0
    score_plot = []
    counter_plot = []
    record = 0
    
    # While the games played are less then the epochs loop
    while counter_games < params['epochs']:
        # Manage the quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Initialize classes
        game = Game(440, 440)
        player1 = game.player
        food1 = game.food

        # Perform first move
        initialize_game(player1, game, food1, agent, params['batch_size'])

        if display_option:
            display(player1, food1, game, record, counter_games)

        while not game.crash:
            if not params['train']:
                agent.epsilon = 0
            else:
                # agent.epsilon is set to give randomness to actions
                agent.epsilon = 1 - (counter_games * params['epsilon_decay_linear'])

            # Get old state
            state_old = agent.get_state(game, player1, food1)

            # Perform random actions based on agent.epsilon, or choose the action
            if randint(0, 1) < agent.epsilon:
                final_move = to_categorical(randint(0, 2), num_classes=3)
            else:
                # Predict an action based on the old state (model prediction)
                prediction = agent.network.predict(state_old.reshape((1, 11)))
                final_move = to_categorical(np.argmax(prediction[0]), num_classes=3)

            # Perform new move and get the new state
            player1.move(final_move, player1.x, player1.y, game, food1, agent)
            state_new = agent.get_state(game, player1, food1)

            # Set a reward for the new state
            reward = agent.set_reward(player1, game.crash)

            if params['train']:
                # Train short memory base on the new action and state
                agent.train_short_memory(state_old, final_move, reward, state_new, game.crash)
                # Store the new data into a long term memory
                agent.remember(state_old, final_move, reward, state_new, game.crash)
            # Get the best score
            record = get_record(game.score, record)

            if display_option:
                display(player1, food1, game, record, counter_games)
                pygame.time.wait(speed)
        
        if params['train']:
            agent.replay_new(agent.memory, params['batch_size'])

        counter_games += 1

        print(f'Game {counter_games}      Score: {game.score}')

        score_plot.append(game.score)
        counter_plot.append(counter_games)

    # If 'train' parameter in the dict is set to true save the new weights
    if params['train']:
        agent.network.save_weights(params['weights_save_path'])
    
    # When counter_games > epochs plot the training trends
    plot_training_stats(counter_plot, score_plot, params['epochs'])


#---------------------------------------
if __name__ == '__main__':
    pygame.font.init()
    parser = argparse.ArgumentParser()
    params = define_parameters()
    # Activate or deactivate the game view and the
    parser.add_argument("--display", type=bool, default=True)
    parser.add_argument("--speed", type=int, default=10)

    args = parser.parse_args()
    main_game_loop(args.display, args.speed, params) 
