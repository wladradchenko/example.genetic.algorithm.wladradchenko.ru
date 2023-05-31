from organism import Organism
from random import random, choice, uniform
from math import atan2, degrees, sqrt, cos, sin


# Helper functions for distance calculation and heading calculation
def dist(x1, y1, z1, x2, y2, z2):
    return sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

def calc_heading(org, food):
    d_x = food.x - org.x
    d_y = food.y - org.y
    d_z = food.z - org.z
    theta_d = degrees(atan2(d_y, d_x)) - org.r
    phi_d = degrees(atan2(d_z, sqrt(d_x**2 + d_y**2))) - org.p
    if abs(theta_d) > 180: theta_d += 360
    if abs(phi_d) > 180: phi_d += 360
    return theta_d / 180, phi_d / 180

# Function for evolving the organisms based on their fitness and genetic operators
def evolve(settings, organisms):
    # Placeholder for evolution logic
    # Add your evolution implementation here
    # This function should update the organisms based on their fitness and genetic operators

    # Example implementation: Randomly select organisms for reproduction
    new_population = []

    # Perform elitism by keeping the best organisms without modification
    elitism_count = int(settings['elitism'] * settings['pop_size'])
    sorted_organisms = sorted(organisms, key=lambda org: org.fitness, reverse=True)
    new_population.extend(sorted_organisms[:elitism_count])

    # Generate offspring through crossover and mutation
    for _ in range(settings['pop_size'] - elitism_count):
        parent1 = choice(organisms)
        parent2 = choice(organisms)
        child = crossover(parent1, parent2)  # Perform crossover to create a new organism
        mutate(child, settings)  # Perform mutation on the child organism
        new_population.append(child)  # Add the child to the new population

    # Replace the old population with the new population
    organisms[:] = new_population


# Function for performing crossover between two parent organisms
def crossover(parent1, parent2):
    child = Organism(parent1.settings)  # Create a new organism with the same settings as the parents
    # Add your crossover implementation here
    # Example: Create a child organism by randomly selecting attributes from the parents
    child.x = choice([parent1.x, parent2.x])
    child.y = choice([parent1.y, parent2.y])
    child.z = choice([parent1.z, parent2.z])
    child.r = choice([parent1.r, parent2.r])
    child.p = choice([parent1.p, parent2.p])
    return child

# Function for mutating an organism's genes
def mutate(organism, settings):
    # Add your mutation implementation here
    # Example: Randomly modify some attributes of the organism
    if random() < settings['mutate']:
        organism.x = uniform(settings['x_min'], settings['x_max'])
    if random() < settings['mutate']:
        organism.y = uniform(settings['y_min'], settings['y_max'])
    if random() < settings['mutate']:
        organism.z = uniform(settings['z_min'], settings['z_max'])
    if random() < settings['mutate']:
        organism.r = uniform(-180, 180)
    if random() < settings['mutate']:
        organism.p = uniform(-90, 90)

# Function for simulating the organisms' behavior in the 3D environment
def simulate(settings, organisms, foods):
    # Placeholder for simulation logic
    # Add your simulation implementation here
    # This function should update the organisms' positions, headings, and fitness based on their behavior

    # Example implementation: Randomly update the organisms' positions
    for org in organisms:
        if org.fitness <= 0:
            continue

        dx = uniform(-settings['v_max'], settings['v_max'])
        dy = uniform(-settings['v_max'], settings['v_max'])
        dz = uniform(-settings['v_max'], settings['v_max'])

        # Update the organism's position, considering the boundaries
        org.x = max(settings['x_min'], min(org.x + dx, settings['x_max']))
        org.y = max(settings['y_min'], min(org.y + dy, settings['y_max']))
        org.z = max(settings['z_min'], min(org.z + dz, settings['z_max']))

        # Update the organism's fitness based on its position and proximity to food particles
        org.fitness += calculate_fitness(org, foods, settings)

        # Update the organism's perception data (d_food, r_food, and z_food)
        org.d_food, org.r_food, org.z_food = calculate_perception(org, foods)


    # GET ORGANISM RESPONSE
    for org in organisms:
        org.think()

    # UPDATE ORGANISMS POSITION AND VELOCITY
    for org in organisms:
        org.update_heading(settings)
        org.update_velocity(settings)
        org.update_position(settings)


# Function to calculate an organism's perception data (d_food, r_food, and z_food) based on its position and the food particles
def calculate_perception(organism, foods):
    # Calculate the distance, orientation, and vertical distance to the nearest food particle
    # Example implementation:
    d_food = float('inf')  # Initialize the distance to infinity
    r_food = 0.0  # Initialize the orientation to 0
    z_food = 0.0  # Initialize the vertical distance to 0

    for food in foods:
        dx = food.x - organism.x
        dy = food.y - organism.y
        dz = food.z - organism.z
        distance = sqrt(dx**2 + dy**2 + dz**2)

        if distance < d_food:
            d_food = distance
            r_food = atan2(dy, dx)  # Calculate the orientation towards the nearest food particle
            z_food = dz  # Calculate the vertical distance to the nearest food particle

    return d_food, r_food, z_food


# Function for calculating the organism's fitness based on its position and proximity to food particles
def calculate_fitness(organism, foods, settings):
    # Add your fitness calculation implementation here
    # Example: Calculate the distance between the organism and each food particle,
    # and assign fitness based on the proximity to food
    fitness = 0.0
    for food in foods:
        distance = calculate_distance(organism, food)

        if distance <= settings["distance"]:
            fitness += food.energy / (distance + 1.0)  # Assign higher fitness to organisms closer to food
            food.respawn()

    if fitness == 0.0:
        fitness = settings["fine"]

    return fitness

# Function for calculating the distance between two points in 3D space
def calculate_distance(point1, point2):
    # Add your distance calculation implementation here
    # Example: Euclidean distance between two points in 3D space
    distance = ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2) ** 0.5
    return distance