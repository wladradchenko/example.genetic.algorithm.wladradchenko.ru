from constants import settings
from food import Food
from organism import Organism
from functions import simulate, evolve, crossover
from plotting import plot_frame
from random import choice


# Main function
def run():
    # Initialize environment with food particles and organisms
    foods = []
    organisms = []
    for _ in range(settings['food_num']):
        foods.append(Food())

    for _ in range(settings['pop_size']):
        organisms.append(Organism(settings))

    # Cycle through each generation of evolution and simulation
    for gen in range(settings['gens']):

        for org in organisms:
            org.reset()

        for time in range(settings['gen_time']):
            simulate(settings, organisms, foods)

            if settings['plot'] and gen == settings['gens'] - 1:

                # Update strong organisms
                strong_organism = []
                for org in organisms:
                    if org.fitness > 1:
                        strong_organism += [org]
                else:
                    # Update child organisms
                    if len(strong_organism) >= 2 and len(foods) > len(organisms):
                        num_children = len(strong_organism) // 2
                        for _ in range(num_children):
                            parent1 = choice(strong_organism)
                            parent2 = choice(strong_organism)
                            child = crossover(parent1, parent2)  # Perform crossover to create a new organism
                            organisms.append(child)

                plot_frame(settings, organisms, foods, gen, time)

        evolve(settings, organisms)


if __name__ == "__main__":
    run()
