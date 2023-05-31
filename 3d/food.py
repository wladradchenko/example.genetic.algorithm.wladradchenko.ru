from constants import settings
from random import uniform


# Class representing the food particles
class Food(object):
    def __init__(self):
        self.respawn()

    def respawn(self):
        self.color = 'green'
        self.x = uniform(settings['x_min'], settings['x_max'])
        self.y = uniform(settings['y_min'], settings['y_max'])
        self.z = uniform(settings['z_min'], settings['z_max'])
        self.energy = 1
