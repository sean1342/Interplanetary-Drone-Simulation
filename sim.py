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
        for i in range(n_planets):
            self.bodies.append(Body(np.random.uniform(0, avg_mass * 2), (0, 0), (200, 200)))
    
    def init(self):
        pygame.init()

        self.WIN = pygame.display.set_mode()
        pygame.display.set_caption("Simulation")

        self.clock = pygame.time.Clock()

    def step(self):
        self.WIN.fill((0,0,0))
        dt = self.clock.tick(60)

        physics.step(dt, self.bodies)

        for body in self.bodies:
            pygame.draw.circle(self.WIN, (255,255,255), body.position, np.sqrt(body.mass/np.pi))

        pygame.display.update()

sim = Sim(100, 2, 10)

running = True
while running:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    sim.step()