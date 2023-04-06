import pygame
import physics
import numpy as np

class Body:
    def __init__(self, mass, velocity, position):
        self.mass = mass
        self.velocity = velocity
        self.position = position

class Sim:
    def __init__(self, sun_mass, n_planets, avg_mass):
        self.SIZE = (600, 400)

        self.sun_mass = sun_mass

        self.bodies = []
        # self.bodies.append(Body(1000, [0, 0], [100, 100]))
        # self.bodies.append(Body(1000, [0, 0], [200, 230]))

        for i in range(n_planets):
            self.bodies.append(Body(np.random.uniform(0, avg_mass * 2), [0, 0], [np.random.random() * self.SIZE[0], np.random.random() * self.SIZE[0]]))
    
    def init(self):
        pygame.init()

        self.WIN = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Simulation")

        self.clock = pygame.time.Clock()

    def step(self):
        self.WIN.fill((0,0,0))
        dt = self.clock.tick(60)

        physics.step(dt, self.bodies)

        for body in self.bodies:
            pygame.draw.circle(self.WIN, (255,255,255), body.position, np.sqrt(body.mass/np.pi))
            # print(body.position[0], body.position[1])

        pygame.display.update()

sim = Sim(1000, 2, 100)
sim.init()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    sim.step()