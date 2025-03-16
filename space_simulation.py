import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

class CelestialBody:
    def __init__(self, name, mass, position, velocity, color):
        self.name = name
        self.mass = mass
        self.position = np.array(position, dtype='float64')
        self.velocity = np.array(velocity, dtype='float64')
        self.color = color

    def update_position(self, dt):
        self.position += self.velocity * dt
    
    def apply_gravity(self, other):
        G = 6.67430e-11  # universal gravitational constant
        r = np.linalg.norm(other.position - self.position)
        force_magnitude = G * self.mass * other.mass / r**2
        force_direction = (other.position - self.position) / r
        return force_magnitude * force_direction

class Universe:
    def __init__(self):
        self.bodies = []
    
    def add_body(self, body):
        self.bodies.append(body)
    
    def update(self, dt):
        forces = {body: np.zeros(2) for body in self.bodies}
        
        for i, body in enumerate(self.bodies):
            for j in range(i+1, len(self.bodies)):
                other = self.bodies[j]
                force = body.apply_gravity(other)
                forces[body] += force
                forces[other] -= force
        
        for body in self.bodies:
            # update velocity based on net force
            body.velocity += forces[body] / body.mass * dt
            body.update_position(dt)

def init_plot(universe):
    fig, ax = plt.subplots()
    ax.set_xlim(-1e11, 1e11)
    ax.set_ylim(-1e11, 1e11)
    ax.set_aspect('equal', adjustable='box')
    return fig, ax

def animate(i, universe, scat):
    universe.update(1e3)  # time step
    positions = np.array([body.position for body in universe.bodies])
    scat.set_offsets(positions)
    return scat,

def main():
    universe = Universe()

    sun = CelestialBody("Sun", 1.989e30, [0, 0], [0, 0], 'yellow')
    earth = CelestialBody("Earth", 5.972e24, [1.496e11, 0], [0, 29780], 'blue')
    mars = CelestialBody("Mars", 6.4171e23, [2.279e11, 0], [0, 24077], 'red')

    universe.add_body(sun)
    universe.add_body(earth)
    universe.add_body(mars)

    fig, ax = init_plot(universe)
    scat = ax.scatter([], [])
    
    anim = FuncAnimation(fig, animate, fargs=(universe, scat), frames=200, interval=100, blit=True)
    plt.title("Space Simulation")
    plt.show()

if __name__ == "__main__":
    main()