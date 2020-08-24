import os
import pygame
import argparse
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from Agent import Agent
from random import randint
from keras.utils import to_categorical

from Game import Game
from Snake import Snake
from Food import Food

def define_parameters():
    params = dict()
    params['epsilon_decay_linear'] = 1/75
    params['learning_rate'] = 0.0005
    params['first_layer_size'] = 150   # neurons in the first layer
    params['second_layer_size'] = 150   # neurons in the second layer
    params['third_layer_size'] = 150    # neurons in the third layer
    params['episodes'] = 150            
    params['memory_size'] = 2500
    params['batch_size'] = 500
    params['weights_path'] = 'weights/weights.hdf5'
    params['load_weights'] = True
    params['train'] = False
    return params

def eat(player, food, game):
    if player.x == food.x and player.y == food.y:
        food.food_coord(game, player)
        player.eaten = True
        game.score = game.score + 1


def get_record(score, record):
    if score >= record:
        return score
    else:
        return record

def display_ui(game, score, record, generation):
    myfont = pygame.font.SysFont('Segoe UI', 30)
    myfont_bold = pygame.font.SysFont('Segoe UI', 30, True)

    text_score = myfont.render('Current score: ', True, (0, 0, 0))
    text_score_number = myfont_bold.render(str(score), True, (0, 0, 0))
    text_highest = myfont.render('Best score: ', True, (0, 0, 0))
    text_highest_number = myfont_bold.render(str(record), True, (0, 0, 0))
    text_generation = myfont.render('Generation n: ', True, (0, 0, 0))
    text_generation_number = myfont_bold.render(str(generation), True, (0, 0, 0))
    
    game.gameDisplay.blit(text_score, (20, 440))
    game.gameDisplay.blit(text_score_number, (200, 440))
    game.gameDisplay.blit(text_highest, (240, 440))
    game.gameDisplay.blit(text_highest_number, (400, 440))
    game.gameDisplay.blit(text_generation, (20, 470))
    game.gameDisplay.blit(text_generation_number, (200, 470))



    game.gameDisplay.blit(game.background, (10, 10))

def display(player, food, game, record, generation):
    game.gameDisplay.fill((255, 255, 255))
    display_ui(game, game.score, record, generation)
    player.render(player.position[-1][0], player.position[-1][1], player.tail_lenght, game)
    food.render(food.x, food.y, game)


def update_screen():
    pygame.display.update()
    pygame.event.get()


def initialize_game(player, game, food, agent, batch_size):
    state_init1 = agent.get_state(game, player, food)  # [0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0]
    action = [1, 0, 0]
    player.move(action, player.x, player.y, game, food, agent)
    state_init2 = agent.get_state(game, player, food)
    reward1 = agent.set_reward(player, game.crash)
    agent.remember(state_init1, action, reward1, state_init2, game.crash)
    agent.replay_new(agent.memory, batch_size)


def plot_seaborn(array_counter, array_score):
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


def run(display_option, speed, params):
    pygame.init()
    agent = Agent(params)
    weights_filepath = params['weights_path']
    if params['load_weights']:
        agent.model.load_weights(weights_filepath)
        print("weights loaded")

    counter_games = 0
    score_plot = []
    counter_plot = []
    record = 0
    while counter_games < params['episodes']:
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

            # get old state
            state_old = agent.get_state(game, player1, food1)

            # perform random actions based on agent.epsilon, or choose the action
            if randint(0, 1) < agent.epsilon:
                final_move = to_categorical(randint(0, 2), num_classes=3)
            else:
                # predict action based on the old state
                prediction = agent.model.predict(state_old.reshape((1, 11)))
                final_move = to_categorical(np.argmax(prediction[0]), num_classes=3)

            # perform new move and get new state
            player1.move(final_move, player1.x, player1.y, game, food1, agent)
            state_new = agent.get_state(game, player1, food1)

            # set reward for the new state
            reward = agent.set_reward(player1, game.crash)

            if params['train']:
                # train short memory base on the new action and state
                agent.train_short_memory(state_old, final_move, reward, state_new, game.crash)
                # store the new data into a long term memory
                agent.remember(state_old, final_move, reward, state_new, game.crash)

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
    if params['train']:
        agent.model.save_weights(params['weights_path'])
    plot_seaborn(counter_plot, score_plot)


if __name__ == '__main__':
    # Set options to activate or deactivate the game view, and its speed
    pygame.font.init()
    parser = argparse.ArgumentParser()
    params = define_parameters()
    parser.add_argument("--display", type=bool, default=True)
    parser.add_argument("--speed", type=int, default=50)
    args = parser.parse_args()
    params['bayesian_optimization'] = False    # Use bayesOpt.py for Bayesian Optimization
    run(args.display, args.speed, params) 
