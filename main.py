#
# 3 body problem simulator
# @cartertrafton
#
############################## file set up
import pygame
from random import *
import numpy as np
import time
import sys

# initiate pygame and clock
pygame.init()
clock = pygame.time.Clock()
game_font = pygame.font.SysFont('ubuntu', 15)

# dimensions
WIDTH = 1000
HEIGHT = 600

# gravitational constant
g = 4.4

# set up colors:
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# set up surface plane
surface = pygame.display.set_mode((WIDTH, HEIGHT))  # ((width, height))
pygame.display.set_caption('3 body')
surface.fill(BLACK)

# trails
global trails_active
trails_active = False

# trails button
trails_button = pygame.Rect(0, 0, 100, 50)
trails_button_surface = game_font.render("TRAILS", True, (0, 0, 0))
pygame.draw.rect(surface, WHITE, trails_button)
surface.blit(trails_button_surface, (50, 10))

# exit button
exit_button = pygame.Rect(WIDTH-100, 0, 100, 50)
exit_button_surface = game_font.render("EXIT", True, (0, 0, 0))
pygame.draw.rect(surface, WHITE, exit_button)
surface.blit(exit_button_surface, (WIDTH-90, 10))

# reset button
reset_button = pygame.Rect(WIDTH/2 - 50, 0, 100, 50)
reset_button_surface = game_font.render("RESET", True, (0, 0, 0))
pygame.draw.rect(surface, WHITE, reset_button)
surface.blit(reset_button_surface, (WIDTH/2 - 30, 10))

############################## celestial body object
class Body(object):
    def __init__(self, m, x, y, r, c):
        # mass, postion (x, y), color
        self.mass = m
        self.position = np.array([x, y])
        self.last_position = np.array([x, y])
        self.velocity = np.array([0, 0])
        self.accel = np.array([randint(-1,1), randint(-1,1)])
        self.color = c
        self.radius = r

    def applyForce(self, force):
        # apply forces to a body
        f = force / self.mass
        self.accel = np.add(self.accel, f)

    def update(self):
        # update position based on velocity and reset accel
        self.velocity = np.add(self.velocity, self.accel)
        self.last_position = self.position
        self.position = np.add(self.position, self.velocity)
        self.accel = 0
        if(self.position[0] > WIDTH) or (self.position[0] < 0) or (self.position[1] > HEIGHT) or (self.position[1] < 0):
            self.randomize_position()
            print("object left screen")

    def display(self):
        # draw over old object location
        pygame.draw.circle(surface, BLACK, (int(self.last_position[0]), int(self.last_position[1])), self.radius)  	# (drawLayer, color, (coordinates), radius)

        # draw trail (Comment this line out to remove trails)
        if trails_active == True:
            pygame.draw.line(surface, WHITE, (int(self.last_position[0]), int(self.last_position[1])), (int(self.position[0]), int(self.position[1])), 5)

        # draw new object location
        pygame.draw.circle(surface, self.color, (int(self.position[0]), int(self.position[1])), self.radius)


    def attract(self, m, g):
        # gravitational code rewritten from Daniel Shiffman's "Nature of Code"
        force = self.position - m.position
        distance = np.linalg.norm(force)
        distance = constrain(distance, 5.0, 25.0)
        force = normalize(force)
        strength = (g * self.mass * m.mass) / float(distance * distance)
        force = force * strength
        return force

    def randomize_position(self):
        self.position[0] = randrange(1000)
        self.position[1] = randrange(600)
        self.velocity = np.array([0, 0])
        return

############################## set up and draw
def setup():
    # planets
    body1 = Body(randint(0, 10), 700, 200, 5, BLUE)
    body2 = Body(randint(0, 10), 600, 200, 5, RED)
    body3 = Body(randint(0, 10), 500, 286, 5, YELLOW)

    # list of all bodies
    global bodies
    bodies = [body1, body2, body3]
    return


def draw():
    # for each body: apply forces, update position, and draw
    for body in bodies:
        for other_body in bodies:
            if (body != other_body):
                global g
                force = other_body.attract(body, g)
                body.applyForce(force)
        body.update()
        body.display()

    # Re-draw buttons
    pygame.draw.rect(surface, WHITE, trails_button)
    surface.blit(trails_button_surface, (10, 10))
    pygame.draw.rect(surface, WHITE, exit_button)
    surface.blit(exit_button_surface, (WIDTH-90, 10))
    pygame.draw.rect(surface, WHITE, reset_button)
    surface.blit(reset_button_surface, (WIDTH/2 - 30, 10))

    return


############################## mathematical functions

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


def normalize(force):
    normal = np.linalg.norm(force, ord=1)
    if normal == 0:
        normal = np.finfo(force.dtype).eps
    return force / normal


############################## main loop

if __name__ == "__main__":
    # initial set up
    setup()
    while True:
        # draw bodies to screen
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # trails button
                if trails_button.collidepoint(mouse_pos):
                    #print("trails button pushed")
                    if trails_active == True:
                        trails_active = False
                        surface.fill(BLACK)
                    else:
                        trails_active = True
                if exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if reset_button.collidepoint(mouse_pos):
                    for body in bodies:
                        body.randomize_position()
                    surface.fill(BLACK)

        pygame.display.update()
        time.sleep(0.05)
