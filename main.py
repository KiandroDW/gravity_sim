import pygame
import math
import random
import sys
import time

# Good values to use:
# Mass for bodies that need to interact with eachother: 5*10^3- 5*10^4
# Mass for star: 5*10^5+
# Distance of planet from a star is best > 200 and velocity > 10

args = sys.argv
search = False

if (len(args) > 1) and args[1] == "search":
    search = True

if not search:
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    WIDTH, HEIGHT = screen.get_width(), screen.get_height()
    trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
else:
    WIDTH, HEIGHT = 1920, 1080
center = (WIDTH // 2, HEIGHT // 2)

clock = pygame.time.Clock()

# Gravitational constant
G = 6.6743 * 10 ** -1   # *10^-10
# G is a bigger number here so we dont work with extreme values,
# this means all masses noted are actually *10^-5.

fps = 60


class Body:
    def __init__(self,
                 mass: int,
                 radius: int,
                 x: float,
                 y: float,
                 vx: float,
                 vy: float,
                 color: tuple):
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.trail = []

    def draw(self):
        self.update_pos()
        self.trail.append((self.x, self.y))
        if len(self.trail) > 255:
            self.trail.pop(0)

        for index in range(len(self.trail)):
            op_col = (self.color[0], self.color[1], self.color[2], index)
            pygame.draw.circle(
                trail_surface,
                op_col,
                (self.trail[index][0] + WIDTH // 2 - center[0], self.trail[index][1] + HEIGHT // 2 - center[1]),
                1
            )

        screen.blit(trail_surface, (0, 0))

        pygame.draw.circle(screen, self.color, (self.x + WIDTH // 2 - center[0], self.y + HEIGHT // 2 - center[1]), self.radius)

    def update_speed(self):
        for body in bodies:
            dx = body.x - self.x
            dy = body.y - self.y
            if abs(dx) > 1e-10 or abs(dy) > 1e-10:
                dist_squared = dx ** 2 + dy ** 2
                # F = m*a = G*M*m/d^2 => a = G*M/d^2
                a = G * body.mass / dist_squared
                angle = math.atan2(dy, dx)
                ax = math.cos(angle) * a
                ay = math.sin(angle) * a

                self.vx += ax
                self.vy += ay

    def update_pos(self):
        self.x += self.vx
        self.y += self.vy

    def __str__(self):
        return f"Body({self.mass}, {self.radius}, {self.x}, {self.y}, {self.vx}, {self.vy}, {self.color})"

bodies = [Body(1000, 10, 1169, 908, 0.6504895921664646, -0.9143752642893779, (35, 105, 255)), Body(1000, 10, 629, 537, 0.7081447763115003, 0.5825628241052676, (255, 16, 153)), Body(1000, 10, 706, 695, -0.9854231495023225, 0.5343663618799901, (255, 62, 79))]

colors = [
    (255, 0, 0),
    (255, 128,  0),
    (255, 255, 0),
    (128, 255, 0),
    (0, 255, 0),
    (0, 255, 128),
    (0, 255, 255),
    (0, 128, 255),
    (0, 0, 255),
    (128, 0, 255),
    (255, 0, 255),
    (255, 0, 128)
]


def generate_randoms(amount):
    colors = []
    for i in range(amount):
        i_255 = random.randint(0, 2)
        if i_255 == 0:
            colors.append((255, random.randint(0, 255), random.randint(0, 255)))
        elif i_255 == 1:
            colors.append((random.randint(0, 255), 255, random.randint(0, 255)))
        else:
            colors.append((random.randint(0, 255), random.randint(0, 255), 255))
    global bodies
    bodies = [
        Body(
            1000,
            10,
            random.randint(WIDTH // 2 - 600, WIDTH // 2 + 600),
            random.randint(HEIGHT // 2 - 400, HEIGHT // 2 + 400),
            random.random() * 2 - 1,
            random.random() * 2 - 1,
            colors[i]
        ) for i in range(amount)
    ]
    mapped = list(map(str, bodies))
    return str(mapped)


def center_of_mass():
    x_com = sum([i.mass * i.x for i in bodies]) / sum([i.mass for i in bodies])
    y_com = sum([i.mass * i.y for i in bodies]) / sum([i.mass for i in bodies])
    return x_com, y_com


tracking = -1
running = True
while running and not search:
    screen.fill((0, 0, 0))
    trail_surface.fill((0, 0, 0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_c:
                center = center_of_mass()
                tracking = -1
            if event.key == pygame.K_f:
                center = center_of_mass()
                tracking = -2
            if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                tracking = -1
                center = (WIDTH // 2, HEIGHT // 2)
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                tracking = 0
            if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                tracking = 1
            if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                tracking = 2
            if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                tracking = 3
            if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                tracking = 4
            if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                tracking = 5
            if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                tracking = 6
            if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                tracking = 7
            if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                tracking = 8
            if event.key == pygame.K_r:
                generate_randoms(random.randint(2, 50))

    for body in bodies:
        body.update_speed()
    for body in bodies:
        body.draw()

    if tracking >= 0 and len(bodies) > tracking:
        center = (bodies[tracking].x, bodies[tracking].y)

    if tracking == -2:
        center = center_of_mass()

    pygame.display.flip()
    clock.tick(fps)


def check_dist():
    max_dist = 0
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            dist = (bodies[i].x - bodies[j].x) ** 2 + (bodies[i].y - bodies[j].y) ** 2
            if dist > max_dist:
                max_dist = dist
    return max_dist < (HEIGHT * 2 / 3) ** 2


counter = 0
prev = generate_randoms(3)
start = time.time()
while running and search:
    for body in bodies:
        body.update_speed()
    for body in bodies:
        body.update_pos()

    if not check_dist():
        if counter > 216000:    # everything longer than 60 minutes
            print(f"Found stable configuration for {counter} steps!")
        counter = 0
        prev = generate_randoms(3)
        start = time.time()
    else:
        counter += 1
        if counter > 5184000:  # everything longer than 24 hour
            print(f"Possible infinite stable configuration! (took {time.time() - start}s):\n{prev}")
            counter = 0
            prev = generate_randoms(3)
            start = time.time()
