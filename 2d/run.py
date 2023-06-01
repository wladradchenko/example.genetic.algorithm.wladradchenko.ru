from __future__ import division, print_function
import numpy as np

from constants import settings
from food import Food
from organism import Organism
from functions import simulate, evolve


def run(settings):

    # Populate the environment with food
    foods = [Food(settings) for _ in range(settings['food_num'])]

    # Populate the environment with organisms
    organisms = [Organism(settings,
                          np.random.uniform(-1, 1, (settings['hnodes'], settings['inodes'])),
                          np.random.uniform(-1, 1, (settings['onodes'], settings['hnodes'])),
                          name=f'gen[x]-org[{i}]')
                 for i in range(settings['pop_size'])]

    # Cycle through each generation
    for gen in range(settings['gens']):
        # Simulate
        organisms = simulate(settings, organisms, foods, gen)

        # Evolve
        organisms, stats = evolve(settings, organisms, gen)
        print(f'> GEN: {gen} BEST: {stats["BEST"]} AVG: {stats["AVG"]} WORST: {stats["WORST"]}')

    pass


if __name__ == '__main__':
    run(settings)
