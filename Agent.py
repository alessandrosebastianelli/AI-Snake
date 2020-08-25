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
        self.dataframe = pd.DataFrame()
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_predict = 0
        self.epsilon = 1
        self.actual = []
        self.memory = collections.deque(maxlen=params['memory_size'])

        # Load settings 
        self.lr = params['lr']   
        self.firstLayer_dim = params['firstLayer_dim']
        self.secondLayer_dim = params['secondLayer_dim']
        self.thirdLayer_dim = params['thirdLayer_dim']
        self.weights_save_path = params['weights_save_path']
        self.load_weights = params['load_weights']

        self.model = self.build_network()

    # Create the network
    def build_network(self):
        # Build a sequential model
        model = Sequential()
        model.add(Dense(output_dim=self.firstLayer_dim, activation='relu', input_dim=11))
        model.add(Dense(output_dim=self.secondLayer_dim, activation='relu'))
        model.add(Dense(output_dim=self.thirdLayer_dim, activation='relu'))
        model.add(Dense(output_dim=3, activation='softmax'))
        opt = Adam(self.lr)
        model.compile(loss='mse', optimizer=opt)
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

            player.x_change == -20,         # move left
            player.x_change == 20,          # move right
            player.y_change == -20,         # move up
            player.y_change == 20,          # move down
            food.x < player.x,              # food left
            food.x > player.x,              # food right
            food.y < player.y,              # food up
            food.y > player.y               # food down
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

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay_new(self, memory, batch_size):
        if len(memory) > batch_size:
            minibatch = random.sample(memory, batch_size)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, 11)))[0])
        target_f = self.model.predict(state.reshape((1, 11)))
        target_f[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1, 11)), target_f, epochs=1, verbose=0)
