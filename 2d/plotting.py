from math import sin, cos, radians
import matplotlib.pyplot as plt

def plot_organism(x1, y1, theta, ax):
    circle = plt.Circle((x1, y1), 0.05, edgecolor='g', facecolor='lightgreen', zorder=8)
    ax.add_artist(circle)

    tail_len = 0.075
    x2 = x1 + cos(radians(theta)) * tail_len
    y2 = y1 + sin(radians(theta)) * tail_len

    ax.plot([x1, x2], [y1, y2], color='darkgreen', linewidth=1, zorder=10)

def plot_food(x1, y1, ax):
    circle = plt.Circle((x1, y1), 0.03, edgecolor='darkslateblue', facecolor='mediumslateblue', zorder=5)
    ax.add_artist(circle)
