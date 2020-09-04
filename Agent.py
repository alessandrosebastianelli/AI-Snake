from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import numpy as np
import pandas as pd
from operator import add
import collections

class Agent(object):
    def __init__(self, params):
        self.reward = 0
        self.gamma = 0.9
        self.memory = collections.deque(maxlen=params['memory_size'])

        # Old code start
        #
        #
        #
        # Old code end

        # Load network settings 
        self.lr = params['lr']   
        self.firstLayer_dim = params['firstLayer_dim']
        self.secondLayer_dim = params['secondLayer_dim']
        self.thirdLayer_dim = params['thirdLayer_dim']
        self.weights_save_path = params['weights_save_path']
        self.load_weights = params['load_weights']
        self.dropout = params['dropout']
        self.dropoutVal = params['dropoutValue']

        self.network = self.build_network()

    # Create the network
    def build_network(self):
        # Build a sequential model
        model = Sequential()
        model.add(Dense(output_dim=self.firstLayer_dim, activation='relu', input_dim=11))
        if self.dropout:
            model.add(Dropout(self.dropoutVal))
        model.add(Dense(output_dim=self.secondLayer_dim, activation='relu'))
        if self.dropout:
            model.add(Dropout(self.dropoutVal))
        model.add(Dense(output_dim=self.thirdLayer_dim, activation='relu'))
        if self.dropout:
            model.add(Dropout(self.dropoutVal))
        model.add(Dense(output_dim=3, activation='softmax'))
        model.compile(loss='mse', optimizer = Adam(self.lr))
        # If true load pre-trained weights
        if self.load_weights:
            model.load_weights(self.weights_save_path)
        return model
    
    def get_state(self, game, player, food):
        state = [
            (player.x_change == 20 and player.y_change == 0 and ((list(map(add, player.position[-1], [20, 0])) in player.position) or
            player.position[-1][0] + 20 >= (game.width - 20))) or (player.x_change == -20 and player.y_change == 0 and ((list(map(add, player.position[-1], [-20, 0])) in player.position) or
            player.position[-1][0] - 20 < 20)) or (player.x_change == 0 and player.y_change == -20 and ((list(map(add, player.position[-1], [0, -20])) in player.position) or
            player.position[-1][-1] - 20 < 20)) or (player.x_change == 0 and player.y_change == 20 and ((list(map(add, player.position[-1], [0, 20])) in player.position) or
            player.position[-1][-1] + 20 >= (game.height-20))),  # danger straight

            (player.x_change == 0 and player.y_change == -20 and ((list(map(add,player.position[-1],[20, 0])) in player.position) or
            player.position[ -1][0] + 20 > (game.width-20))) or (player.x_change == 0 and player.y_change == 20 and ((list(map(add,player.position[-1],
            [-20,0])) in player.position) or player.position[-1][0] - 20 < 20)) or (player.x_change == -20 and player.y_change == 0 and ((list(map(
            add,player.position[-1],[0,-20])) in player.position) or player.position[-1][-1] - 20 < 20)) or (player.x_change == 20 and player.y_change == 0 and (
            (list(map(add,player.position[-1],[0,20])) in player.position) or player.position[-1][
             -1] + 20 >= (game.height-20))),  # danger right

            (player.x_change == 0 and player.y_change == 20 and ((list(map(add,player.position[-1],[20,0])) in player.position) or
            player.position[-1][0] + 20 > (game.width-20))) or (player.x_change == 0 and player.y_change == -20 and ((list(map(
            add, player.position[-1],[-20,0])) in player.position) or player.position[-1][0] - 20 < 20)) or (player.x_change == 20 and player.y_change == 0 and (
            (list(map(add,player.position[-1],[0,-20])) in player.position) or player.position[-1][-1] - 20 < 20)) or (
            player.x_change == -20 and player.y_change == 0 and ((list(map(add,player.position[-1],[0,20])) in player.position) or
            player.position[-1][-1] + 20 >= (game.height-20))), # danger left

            player.x_change == -20,         # moving left
            player.x_change == 20,          # moving right
            player.y_change == -20,         # moving up
            player.y_change == 20,          # moving down
            food.x < player.x,              # is food left
            food.x > player.x,              # is food right
            food.y < player.y,              # is food up
            food.y > player.y               # is food down
            ]

        # From boolean to 0-1
        for i in range(len(state)):
            if state[i]:
                state[i]=1
            else:
                state[i]=0
        return np.asarray(state)

    # Assign a reward: if Snake hits himself or a wall (game crash) the reward is set to -10
    # is Snake eats a fruit the reward is set to +10
    def set_reward(self, player, crash):
        self.reward = 0
        if crash:
            self.reward = -10
            return self.reward
        if player.eaten:
            self.reward = 10
        return self.reward

    # New update - memory

    # Add actions, states etc. to the memory
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay_new(self, memory, batch_size):
        # If the lenght of the memory is greater then the batch_size
        # then extrapolate a batch of batch size randomly from the memory
        if len(memory) > batch_size:
            minibatch = random.sample(memory, batch_size)
        else:
            minibatch = memory

        # Train the network using the input in memory
        for state, action, reward, next_state, done in minibatch:
            pred = reward
            if not done:
                pred = reward + self.gamma * np.amax(self.network.predict(np.array([next_state]))[0])
            final_pred = self.network.predict(np.array([state]))
            final_pred[0][np.argmax(action)] = pred
            self.network.fit(np.array([state]), final_pred, epochs=1, verbose=0)

    def train_short_memory(self, state, action, reward, next_state, done):
        pred = reward
        if not done:
            pred = reward + self.gamma * np.amax(self.network.predict(next_state.reshape((1, 11)))[0])
        final_pred = self.network.predict(state.reshape((1, 11)))
        final_pred[0][np.argmax(action)] = pred
        self.network.fit(state.reshape((1, 11)), final_pred, epochs=1, verbose=0)
