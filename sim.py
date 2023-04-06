import pygame
import physics

class Rocket:
    def __init__(self, position, velocity, rotation):
        self.position = position
        self.velocity = velocity
        self.rotation = rotation
        self.mass = 5e6
        self.height = 3.3423e+30
        self.width = 6.0161e+31

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
        self.scale = 1 / physics.AU * 8 # approx 1 AU per 0.4 pixels to start
        self.timestep = 3600 * 24 # 1 day per frame to start

        self.WIN = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Simulation")

        # time stored in days
        self.time = 0

        # offset to allow movement of view
        self.offset = [0, 0]

        self.clock = pygame.time.Clock()

        self.stepping = True

        # rocket = Rocket([0, 0], [0, 0], 0)

        self.bodies = []
        self.bodies.append(Body([0 * physics.AU, 0 * physics.AU], [0, 0], 8e+30, 4.65247264e-3))
        self.bodies.append(Body([-5 * physics.AU, 0 * physics.AU], [0, 29.783 * 1000], 5e+24, 4.25875e-5))
        # self.bodies.append(rocket)
    
    def draw(self):
        self.WIN.fill((0,0,0))

        for i, body in enumerate(self.bodies):
            font = pygame.font.SysFont('sansserrif', 16)

            # change pygames weird coordinate system to standard
            x = body.position[0] * self.scale + self.SIZE[0] * 0.5
            y = -body.position[1] * self.scale + self.SIZE[1] * 0.5

            # massive scaling factor so everything is visible
            if isinstance(body, Body):
                pygame.draw.circle(self.WIN, (230,230,230), (x, y), body.radius * self.scale * 1e12)
            elif isinstance(body, Rocket):
                rect = pygame.rect.Rect(body.position[0] - body.width / 2, body.position[1] - body.height / 2, body.width, body.height)
                pygame.draw.rect(self.WIN, (255,255,255), rect)

            if isinstance(body, Body):
                if i == 0:
                    text = font.render("Sun", True, (255,255,255))
                else:
                    text = font.render(f"Planet {i}", True, (255,255,255))
                self.WIN.blit(text, (x - text.get_width() / 2, y - body.radius * self.scale * 1e12 - text.get_height()))
            elif isinstance(body, Rocket):
                text = font.render("Rocket", True, (255,255,255))
                self.WIN.blit(text, (x, y - 10))

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

            if event.key == pygame.K_q:
                sim.scale *= 2
            if event.key == pygame.K_a:
                sim.scale *= 0.5
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicking = True
            mouse_start_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            clicking = False
        
    if clicking:
        x_off = (mouse_start_pos[0] - pygame.mouse.get_pos()[0]) / sim.scale
        y_off = (mouse_start_pos[1] - pygame.mouse.get_pos()[1]) / sim.scale

        for body in sim.bodies:
            body.position[0] -= x_off
            body.position[1] += y_off
        
        mouse_start_pos = pygame.mouse.get_pos()

    print(f"{sim.time} Seconds")
    sim.step()
    sim.draw()

pygame.quit()