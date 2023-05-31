import numpy as np
from random import uniform
from math import radians, cos, sin, tan


# Class representing the organisms
class Organism(object):
    def __init__(self, settings):
        self.x = uniform(settings['x_min'], settings['x_max'])
        self.y = uniform(settings['y_min'], settings['y_max'])
        self.z = uniform(settings['z_min'], settings['z_max'])
        self.r = uniform(-180, 180)
        self.p = uniform(-90, 90)
        self.fitness = 1.0
        self.settings = settings
        self.wih = np.random.uniform(-1, 1, (settings['hnodes'], settings['inodes']))
        self.who = np.random.uniform(-1, 1, (settings['onodes'], settings['hnodes']))     # mlp weights (hidden -> output)
        self.d_food = 0
        self.r_food = 0

        self.v = uniform(0, settings['v_max'])  # velocity      [0, v_max]
        self.dv = uniform(-settings['dv_max'], settings['dv_max'])  # dv

    def reset(self):
        self.fitness = 1.0

    def eat_food(self, food):
        # Increase organism's fitness and respawn the food
        self.fitness += 1
        food.respawn(self.settings)

    def update_position(self, settings):
        dx = self.v * cos(radians(self.r)) * settings['dt']
        dy = self.v * sin(radians(self.r)) * settings['dt']
        dz = self.v * tan(radians(self.r)) * settings['dt']
        self.x += dx
        self.y += dy
        self.z += dz  # Add the update for the z-coordinate if necessary

    def update_velocity(self, settings):
        self.v += self.nn_dv * settings['dv_max'] * settings['dt']
        if self.v < 0:
            self.v = 0
        if self.v > settings['v_max']:
            self.v = settings['v_max']

    def update_heading(self, settings):
        self.r += self.nn_dr * settings['dr_max'] * settings['dt']
        self.r = self.r % 360

    def think(self):
        af = lambda x: np.tanh(x)  # activation function
        # Implement the neural network logic here
        # Example implementation:
        af = lambda x: np.tanh(x)  # activation function
        h1 = af(np.dot(self.wih, self.d_food))  # hidden layer
        h2 = af(np.dot(self.wih, self.r_food))  # hidden layer
        out = af(np.dot(self.who, h1 + h2))  # output layer

        # UPDATE dv AND dr WITH MLP RESPONSE
        self.nn_dv = float(out[0])  # [-1, 1]  (accelerate=1, deaccelerate=-1)
        self.nn_dr = float(out[1])  # [-1, 1]  (left=1, right=-1)