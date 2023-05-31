import os
import time


# Constants and settings
settings = dict()

# Evolution settings
settings['pop_size'] = 50
settings['food_num'] = 25
settings['gens'] = 100
settings['elitism'] = 0.20
settings['mutate'] = 0.10

# Simulation settings
settings['gen_time'] = 1000
settings['dt'] = 0.05
settings['dr_max'] = 720
settings['v_max'] = 0.5
settings['dv_max'] =  0.25

settings['x_min'] = -2.0
settings['x_max'] =  2.0
settings['y_min'] = -2.0
settings['y_max'] =  2.0
settings['z_min'] = -2.0
settings['z_max'] =  2.0

settings['plot'] = True
# Organism neural net settings
settings['inodes'] = 1
settings['hnodes'] = 5
settings['onodes'] = 2

# Distance before food
settings["distance"] = 0.3
settings["fine"] = -0.02  # fine on fitness

subfolder = str(int(time.time()))
os.mkdir(os.path.join("output", subfolder))