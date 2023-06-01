# FUNCTIONS
import os
import operator
import time
from collections import defaultdict
from math import sqrt, degrees, atan2, floor
from random import randint, random, sample, uniform
from organism import Organism

from plotting import plot_food
from plotting import plot_organism
import matplotlib.pyplot as plt


subfolder = str(int(time.time()))
os.makedirs(os.path.join('output', subfolder))


def dist(x1,y1,x2,y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)


def calc_heading(org, food):
    d_x = food.x - org.x
    d_y = food.y - org.y
    theta_d = degrees(atan2(d_y, d_x)) - org.r
    if abs(theta_d) > 180: theta_d += 360
    return theta_d / 180


def plot_frame(settings, organisms, foods, gen, t_step):
    fig, ax = plt.subplots()
    fig.set_size_inches(9.6, 5.4)

    plt.xlim([settings['x_min'] + settings['x_min'] * 0.25, settings['x_max'] + settings['x_max'] * 0.25])
    plt.ylim([settings['y_min'] + settings['y_min'] * 0.25, settings['y_max'] + settings['y_max'] * 0.25])

    # PLOT ORGANISMS
    for organism in organisms:
        plot_organism(organism.x, organism.y, organism.r, ax)

    # PLOT FOOD PARTICLES
    for food in foods:
        plot_food(food.x, food.y, ax)

    # MISC PLOT SETTINGS
    ax.set_aspect('equal')
    frame = plt.gca()
    frame.axes.get_xaxis().set_ticks([])
    frame.axes.get_yaxis().set_ticks([])

    # plt.figtext(0.025, 0.95, r'Генерация: '+str(gen))
    # plt.figtext(0.025, 0.90, r'Шаг: '+str(t_step))
    plt.title('Generation: {}, Time: {}'.format(gen, t_step))

    plt.savefig(os.path.join('output', subfolder, f'{t_step}.png'), dpi=100)
    plt.close()

def evolve(settings, organisms_old, gen):

    elitism_num = int(floor(settings['elitism'] * settings['pop_size']))
    new_orgs = settings['pop_size'] - elitism_num

    #--- GET STATS FROM CURRENT GENERATION ----------------+
    stats = defaultdict(int)
    for org in organisms_old:
        if org.fitness > stats['BEST'] or stats['BEST'] == 0:
            stats['BEST'] = org.fitness

        if org.fitness < stats['WORST'] or stats['WORST'] == 0:
            stats['WORST'] = org.fitness

        stats['SUM'] += org.fitness
        stats['COUNT'] += 1

    stats['AVG'] = stats['SUM'] / stats['COUNT']


    #--- ELITISM (KEEP BEST PERFORMING ORGANISMS) ---------+
    orgs_sorted = sorted(organisms_old, key=operator.attrgetter('fitness'), reverse=True)
    organisms_new = []
    for i in range(0, elitism_num):
        organisms_new.append(Organism(settings, wih=orgs_sorted[i].wih, who=orgs_sorted[i].who, name=orgs_sorted[i].name))


    #--- GENERATE NEW ORGANISMS ---------------------------+
    for w in range(0, new_orgs):

        # SELECTION (TRUNCATION SELECTION)
        canidates = range(0, elitism_num)
        random_index = sample(canidates, 2)
        org_1 = orgs_sorted[random_index[0]]
        org_2 = orgs_sorted[random_index[1]]

        # CROSSOVER
        crossover_weight = random()
        wih_new = (crossover_weight * org_1.wih) + ((1 - crossover_weight) * org_2.wih)
        who_new = (crossover_weight * org_1.who) + ((1 - crossover_weight) * org_2.who)

        # MUTATION
        mutate = random()
        if mutate <= settings['mutate']:

            # PICK WHICH WEIGHT MATRIX TO MUTATE
            mat_pick = randint(0,1)

            # MUTATE: WIH WEIGHTS
            if mat_pick == 0:
                index_row = randint(0,settings['hnodes']-1)
                wih_new[index_row] = wih_new[index_row] * uniform(0.9, 1.1)
                if wih_new[index_row] >  1: wih_new[index_row] = 1
                if wih_new[index_row] < -1: wih_new[index_row] = -1

            # MUTATE: WHO WEIGHTS
            if mat_pick == 1:
                index_row = randint(0,settings['onodes']-1)
                index_col = randint(0,settings['hnodes']-1)
                who_new[index_row][index_col] = who_new[index_row][index_col] * uniform(0.9, 1.1)
                if who_new[index_row][index_col] >  1: who_new[index_row][index_col] = 1
                if who_new[index_row][index_col] < -1: who_new[index_row][index_col] = -1

        organisms_new.append(Organism(settings, wih=wih_new, who=who_new, name='gen['+str(gen)+']-org['+str(w)+']'))

    return organisms_new, stats


def simulate(settings, organisms, foods, gen):

    total_time_steps = int(settings['gen_time'] / settings['dt'])

    #--- CYCLE THROUGH EACH TIME STEP ---------------------+
    for t_step in range(0, total_time_steps, 1):

        # PLOT SIMULATION FRAME
        if settings['plot']==True and gen==settings['gens']-1:
            plot_frame(settings, organisms, foods, gen, t_step)

        # UPDATE FITNESS FUNCTION
        for food in foods:
            for org in organisms:
                food_org_dist = dist(org.x, org.y, food.x, food.y)

                # UPDATE FITNESS FUNCTION
                if food_org_dist <= 0.075:
                    org.fitness += food.energy
                    food.respawn(settings)

                # RESET DISTANCE AND HEADING TO NEAREST FOOD SOURCE
                org.d_food = 100
                org.r_food = 0

        # CALCULATE HEADING TO NEAREST FOOD SOURCE
        for food in foods:
            for org in organisms:

                # CALCULATE DISTANCE TO SELECTED FOOD PARTICLE
                food_org_dist = dist(org.x, org.y, food.x, food.y)

                # DETERMINE IF THIS IS THE CLOSEST FOOD PARTICLE
                if food_org_dist < org.d_food:
                    org.d_food = food_org_dist
                    org.r_food = calc_heading(org, food)

        # GET ORGANISM RESPONSE
        for org in organisms:
            org.think()

        # UPDATE ORGANISMS POSITION AND VELOCITY
        for org in organisms:
            org.update_r(settings)
            org.update_vel(settings)
            org.update_pos(settings)

    return organisms

