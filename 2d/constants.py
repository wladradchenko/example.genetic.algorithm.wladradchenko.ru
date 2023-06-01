# CONSTANTS

settings = dict()

# EVOLUTION SETTINGS
settings['pop_size'] = 50       # number of organisms
settings['food_num'] = 25      # number of food particles
settings['gens'] = 100           # number of generations
settings['elitism'] = 0.20      # elitism (selection bias)
settings['mutate'] = 0.10       # mutation rate

# SIMULATION SETTINGS
settings['gen_time'] = 1000      # generation length         (seconds)
settings['dt'] = 0.04           # simulation time step      (dt)
settings['dr_max'] = 720        # max rotational speed      (degrees per second)
settings['v_max'] = 0.5         # max velocity              (units per second)
settings['dv_max'] = 0.25      # max acceleration (+/-)    (units per second^2)

settings['x_min'] = -2.0        # arena western border
settings['x_max'] = 2.0        # arena eastern border
settings['y_min'] = -2.0        # arena southern border
settings['y_max'] = 2.0        # arena northern border

settings['plot'] = True        # plot final generation?

# ORGANISM NEURAL NET SETTINGS
settings['inodes'] = 1          # number of input nodes
settings['hnodes'] = 5          # number of hidden nodes
settings['onodes'] = 2          # number of output nodes