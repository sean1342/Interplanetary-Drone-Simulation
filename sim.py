import pygame
import physics
import numpy as np

class Body:
    def __init__(self, position, velocity, mass, radius):
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.radius = radius

class Sim:
    def __init__(self, SIZE):
        pygame.init()

        self.SIZE = SIZE
        self.scale = 5 / physics.AU # approx 1 AU per 2 pixels to start
        self.timestep = 3600 * 24 * 10 # 10 days per frame to start

        self.WIN = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Simulation")

        # time stored in days
        self.time = 0

        # offset to allow movement of view
        self.offset = [0, 0]

        self.clock = pygame.time.Clock()

        self.bodies = []
        self.bodies.append(Body([0 * physics.AU, 0 * physics.AU], [0, 0], 5e+30, 200000000000))
        self.bodies.append(Body([10 * physics.AU, 0 * physics.AU], [0, 16000], 5e+24, 100000000000))
        self.bodies.append(Body([-10 * physics.AU, 0 * physics.AU], [0, -10000], 5e+24, 100000000000))
    
    def draw(self):
        self.WIN.fill((0,0,0))

        for body in self.bodies:
            # change pygames weird coordinate system to standard
            x = body.position[0] * self.scale + self.SIZE[0] * 0.5 + self.offset[0]
            y = -body.position[1] * self.scale + self.SIZE[1] * 0.5 + self.offset[1]
            pygame.draw.circle(self.WIN, (230,230,230), (x, y), body.radius * self.scale) # * self.scale)
            
        pygame.display.update()

    def step(self):
        self.clock.tick(60)

        # divide by seconds in a day to get days past
        self.time += self.timestep / 86400

        physics.step(self.bodies, self.timestep)

sim = Sim((600,400))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                sim.timestep += 50000
            if event.key == pygame.K_s:
                sim.timestep -= 50000
            if event.key == pygame.K_UP:
                sim.scale += 1 / physics.AU
            if event.key == pygame.K_DOWN:
                sim.scale -= 1 / physics.AU
    if np.round(sim.time, 0) % 10 == 0:
        print(f"{np.round(sim.time, 0)} Days")
    sim.step()
    sim.draw()