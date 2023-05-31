import os
from constants import subfolder
from matplotlib import pyplot as plt
from math import sin, cos, radians


# Function for plotting a frame of the simulation
def plot_frame(settings, organisms, foods, gen, t_step):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim3d([settings['x_min'], settings['x_max']])
    ax.set_ylim3d([settings['y_min'], settings['y_max']])
    ax.set_zlim3d([settings['z_min'], settings['z_max']])

    for food in foods:
        ax.scatter(food.x, food.y, food.z, c=food.color, marker='o')

    for org in organisms:
        if org.fitness <= 0:
            continue

        ax.scatter(org.x, org.y, org.z, c='b', marker='o')
        org_heading = org.r + 90
        org_radians = radians(org_heading)
        dx = cos(org_radians)
        dy = sin(org_radians)
        dz = 0.0
        ax.quiver(org.x, org.y, org.z, dx, dy, dz, length=0.2, color='b')

    plt.title('Generation: {}, Time: {}'.format(gen, t_step))
    plt.savefig(os.path.join("output", subfolder, f"{gen}-{t_step}.png"), dpi=100)
    plt.close()