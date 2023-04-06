import numpy as np

# astronomical unit, gravitational constant
AU = 1.496e+11
G = 6.67408e-11

def step(bodies, timestep):
    for b1 in bodies:
        total_fx = 0
        total_fy = 0
        for b2 in bodies:
            if b1 != b2:
                # calculate distance
                dx = b2.position[0] - b1.position[0]
                dy = b2.position[1] - b1.position[1]
                d = np.sqrt(dx**2 + dy**2)

                # calculate force
                f = G * b1.mass * b2.mass / d ** 2
                theta = np.arctan2(dy, dx)
                fx = np.cos(theta) * f
                fy = np.sin(theta) * f

                # update velocity with force from each other body
                total_fx += fx
                total_fy += fy

        b1.velocity[0] += total_fx / b1.mass * timestep
        b1.velocity[1] += total_fy / b1.mass * timestep

        b1.position[0] += b1.velocity[0] * timestep
        b1.position[1] += b1.velocity[1] * timestep