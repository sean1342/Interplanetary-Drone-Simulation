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
        self.bodies.append(Body([0 * physics.AU, 0 * physics.AU], [0, 0], 8e+30, 4.65247264e-3))
        self.bodies.append(Body([-5 * physics.AU, 0 * physics.AU], [0, 29.783 * 1000], 5e+24, 4.25875e-5))
    
    def draw(self):
        self.WIN.fill((0,0,0))

        for i, body in enumerate(self.bodies):
            font = pygame.font.SysFont('sansserrif', 16)

            # change pygames weird coordinate system to standard
            x = body.position[0] * self.scale + self.SIZE[0] * 0.5 + self.offset[0]
            y = -body.position[1] * self.scale + self.SIZE[1] * 0.5 + self.offset[1]

            # massive scaling factor so everything is visible
            pygame.draw.circle(self.WIN, (230,230,230), (x, y), body.radius * self.scale * 10_000_000_000_000)
            if i == 0:
                text = font.render("Sun", True, (255,255,255))
            else:
                text = font.render(f"Planet {i}", True, (255,255,255))

            x = body.position[0] * self.scale + self.SIZE[0] * 0.5 + self.offset[0]
            y = -body.position[1] * self.scale + self.SIZE[1] * 0.5 + self.offset[1]
            self.WIN.blit(text, (x, y - body.radius * self.scale - text.get_height()))

        pygame.display.update()

    def step(self):
        self.clock.tick(60)

        # divide by seconds in a day to get days past
        self.time += self.timestep / 86400

        physics.step(self.bodies, self.timestep)

sim = Sim((600,400))

mouse_start_pos = [0,0]
clicking = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                sim.timestep *= 1.2
            if event.key == pygame.K_s:
                sim.timestep *= 0.8

            if event.key == pygame.K_q:
                sim.scale *= 2
            if event.key == pygame.K_a:
                sim.scale *= 0.5

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = True
                mouse_start_pos[0] = pygame.mouse.get_pos()[0] - sim.offset[0]
                mouse_start_pos[1] = pygame.mouse.get_pos()[1] - sim.offset[1]
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False
                mouse_start_pos = [0, 0]

    if clicking:
        x_off = mouse_start_pos[0] - pygame.mouse.get_pos()[0]
        y_off = mouse_start_pos[1] - pygame.mouse.get_pos()[1]
        sim.offset[0] = -x_off
        sim.offset[1] = -y_off
        # for body in sim.bodies:
        #     body.position += (x_off,y_off)

    if np.round(sim.time, 0) % 50 == 0:
        print(f"{np.round(sim.time, 0)} Days")
    sim.step()
    sim.draw()

pygame.quit()