import pygame
import physics
import numpy as np

class Rocket:
    def __init__(self, position, velocity):
        self.position = [position[0] * physics.AU, position[1] * physics.AU]
        self.velocity = velocity
        # in radians
        self.angle = 1.571
        self.mass = 4989516.07
        self.height = 3.3423e-10
        self.width = 6.0161e-11

class Body:
    def __init__(self, position, velocity, mass, radius, sun):
        self.sun = sun
        self.position = [position[0] * physics.AU, position[1] * physics.AU]
        self.velocity = velocity
        # in kg
        self.mass = mass
        self.radius = radius

class Sim:
    def __init__(self, SIZE):
        pygame.init()

        self.SIZE = SIZE
        # approx 1 AU per 0.4 pixels to start
        self.scale = 1 / physics.AU * 8
        # 1 day per frame to start
        self.timestep = 3600 * 24

        self.render_constant = 1e12

        self.WIN = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Simulation")

        # time stored in days
        self.time = 0

        # offset to allow movement of view
        self.offset = [0, 0]

        self.clock = pygame.time.Clock()

        self.stepping = True

        self.bodies = []
        self.bodies.append(Body([0, 0], [0, 0], 5e+24, 5e-5, False))
        rocket = Rocket([-2, 0], [0, 0])
        self.bodies.append(rocket)
    
    def draw(self):
        self.WIN.fill((0,0,0))

        for i, body in enumerate(self.bodies):
            font = pygame.font.SysFont('sansserrif', 16)

            # change pygames weird coordinate system to standard
            x = body.position[0] * self.scale + self.SIZE[0] * 0.5
            y = -body.position[1] * self.scale + self.SIZE[1] * 0.5

            if isinstance(body, Body):
                pygame.draw.circle(self.WIN, (230,230,230), (x, y), body.radius * self.scale * self.render_constant)

                if body.sun:
                    text = font.render("Sun", True, (255,255,255))
                else:
                    text = font.render(f"Planet {i}", True, (255,255,255))
                self.WIN.blit(text, (x - text.get_width() * 0.5, y - body.radius * self.scale * self.render_constant - text.get_height()))

            if isinstance(body, Rocket):
                half_width = body.width * self.scale * self.render_constant
                half_height = body.height * self.scale * self.render_constant
                points = [(x - half_width, y + half_height),
                          (x - half_width, y - half_height),
                          (x + half_width, y - half_height),
                          (x + half_width, y + half_height)]
                rot_points = []
                for point in points:
                    s = np.sin(-body.angle + 1.571)
                    c = np.cos(-body.angle + 1.571)

                    px = point[0] - x
                    py = point[1] - y

                    rotx = px * c - py * s
                    roty = px * s + py * c

                    px = rotx + x
                    py = roty + y

                    rot_points.append((px, py))

                pygame.draw.polygon(self.WIN, (255,255,255), rot_points)

                text = font.render("Rocket", True, (255,255,255))
                self.WIN.blit(text, (x - text.get_width() * 0.5, y - body.height * self.scale * self.render_constant - text.get_height()))

        pygame.display.update()

    def step(self):
        self.clock.tick(60)

        # divide by seconds in a day to get days past
        self.time += self.timestep / 86400

        if self.stepping:
            physics.step(self.bodies, self.timestep)

sim = Sim((600,400))

mouse_start_pos = [0,0]
clicking = False
x_off, y_off = 0,0

tracking = False

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
            
            if event.key == pygame.K_SPACE:
                if sim.stepping:
                    sim.stepping = False
                else:
                    sim.stepping = True

            if event.key == pygame.K_w:
                sim.timestep *= 1.2
            if event.key == pygame.K_s:
                sim.timestep *= 0.8

            if event.key == pygame.K_q:
                sim.scale *= 2
            if event.key == pygame.K_a:
                sim.scale *= 0.5
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicking = True
            mouse_start_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            clicking = False

    if (pygame.key.get_pressed()[pygame.K_UP]):
        sim.bodies[1].velocity[1] += 0.00000001 * sim.timestep * np.cos(-sim.bodies[1].angle + 1.571)
        sim.bodies[1].velocity[0] += 0.00000001 * sim.timestep * np.sin(-sim.bodies[1].angle + 1.571)
    if (pygame.key.get_pressed()[pygame.K_RIGHT]):
        sim.bodies[1].angle -= 0.00004 * sim.timestep
    if (pygame.key.get_pressed()[pygame.K_LEFT]):
        sim.bodies[1].angle += 0.00004 * sim.timestep

    if clicking:
        x_off = (mouse_start_pos[0] - pygame.mouse.get_pos()[0]) / sim.scale
        y_off = (mouse_start_pos[1] - pygame.mouse.get_pos()[1]) / sim.scale

        for body in sim.bodies:
            body.position[0] -= x_off
            body.position[1] += y_off
        
        mouse_start_pos = pygame.mouse.get_pos()

    sim.step()
    sim.draw()

pygame.quit()