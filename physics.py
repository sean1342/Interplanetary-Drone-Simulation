import numpy as np
import math

G = 6.67408e-11

def step(dt, bodies):
    for b1 in bodies:
        for b2 in bodies:
            if b1 != b2:
                dx = b2.position[0] - b1.position[0]
                dy = b2.position[1] - b1.position[1]
                distance = math.sqrt(dx * dx + dy * dy)

                # calculate force between bodies
                force = G * b1.mass * b2.mass / (distance**2)

                # calculate x and y components of force
                fx = force * dx / distance
                fy = force * dy / distance

                # apply forces to bodies
                b1.velocity[0] += fx
                b1.velocity[1] += fy
                b2.velocity[0] -= fx
                b2.velocity[1] -= fy

                b1.position[0] += b1.velocity[0] * dt
                b1.position[1] += b1.velocity[1] * dt
                b2.position[0] += b2.velocity[0] * dt
                b2.position[1] += b2.velocity[1] * dt