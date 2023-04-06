import numpy as np

G = 6.67408e-11

def step(dt, bodies):
    for i, b1 in enumerate(bodies):
        for j, b2 in enumerate(bodies):
            if i != j:
                dx = b2.position[0] - b1.position[0]
                dy = b2.position[1] - b1.position[1]

                r = np.sqrt(dx**2 + dy**2)

                F = G * bodies[j].mass * bodies[i].mass / r**2

                theta = np.arctan2(dy, dx)

                Fx += np.cos(theta)*F
                Fy += np.sin(theta)*F

                ax = Fx / b1.mass
                ay = Fy / b1.mass

                bodies[i].velocity[1] += ax * dt
                bodies[i].velocity[1] += ay * dt

                sx = b1.velocity[0] * dt - 0.5 * ax * dt ** 2
                sy = b1.velocity[1] * dt - 0.5 * ay * dt ** 2

                bodies[i].velocity[0] += sx
                bodies[i].velocity[1] += sy