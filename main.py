import pygame
import math

# Good values to use:
# Mass for bodies that need to interact with eachother: 5*10^3- 5*10^4
# Mass for star: 5*10^5+
# Distance of planet from a star is best > 200 and velocity > 10


pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
WIDTH, HEIGHT = screen.get_width(), screen.get_height()
trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

offset = (0, 0)

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
        self.x += self.vx
        self.y += self.vy
        self.trail.append((self.x, self.y))
        if len(self.trail) > 255:
            self.trail.pop(0)

        for index, item in enumerate(self.trail):
            op_col = (self.color[0], self.color[1], self.color[2], index)
            pygame.draw.circle(
                trail_surface,
                op_col,
                (item[0] + offset[0], item[1] + offset[1]),
                1
            )

        screen.blit(trail_surface, (0, 0))

        pygame.draw.circle(screen, self.color, (self.x + offset[0], self.y + offset[1]), self.radius)

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


bodies = [
    Body(50000, 25, 500, 500, 0, 0, (255, 0, 0)),
    Body(100, 10, 700, 500, 0, 12, (0, 255, 0)),
    Body(100, 10, 700, 700, -9, 9, (0, 0, 255)),
]


def center_of_mass():
    x_com = sum([i.mass * i.x for i in bodies]) / sum([i.mass for i in bodies])
    y_com = sum([i.mass * i.y for i in bodies]) / sum([i.mass for i in bodies])
    return WIDTH // 2 - x_com, HEIGHT // 2 - y_com


running = True
while running:
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
                offset = center_of_mass()

    for body in bodies:
        body.update_speed()
    for body in bodies:
        body.draw()

    pygame.display.flip()
    clock.tick(fps)
