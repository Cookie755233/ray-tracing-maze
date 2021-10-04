
import pygame
import random
import math

from pygame import fastevent

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (30, 30, 30)


def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [
                        (x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)


class Ray:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.dir = (math.cos(angle), math.sin(angle))

    def update(self, mx, my):
        self.x = mx
        self.y = my

    def checkCollision(self, wall):
        x1 = wall.start_pos[0]
        y1 = wall.start_pos[1]
        x2 = wall.end_pos[0]
        y2 = wall.end_pos[1]

        x3 = self.x
        y3 = self.y
        x4 = self.x + self.dir[0]
        y4 = self.y + self.dir[1]

        # Using line-line intersection formula to get intersection point of ray and wall
        # Where (x1, y1), (x2, y2) are the ray pos and (x3, y3), (x4, y4) are the wall pos
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        numerator = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        if denominator == 0:
            return None

        t = numerator / denominator
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

        if 1 > t > 0 and u > 0:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            collidePos = [x, y]
            return collidePos


def get_shadow(mx, my, Ox, Oy, O_width):
    A, B, C, D = (Ox, Oy),(Ox, Oy+O_width),\
         (Ox+O_width, Oy+O_width), (Ox+O_width, Oy)

    if mx < Ox:
        if my < Oy:
            return (B, 1), (D, 1)
        elif Oy <= my <= Oy+O_width:
            return (A, 1), (B, 1)
        elif my > Oy:
            return (A, 1), (C, 1)
    if Ox <= mx <= Ox+O_width:
        if my < Oy:
            return (A, -1), (D, 1)
        elif my > Oy:
            return (B, -1), (C, 1)
    if mx > Ox:
        if my < Oy:
            return (A, -1), (C, -1)
        elif Oy <= my <= Oy+O_width:
            return (D,-1), (C, -1)
        elif my > Oy:
            return (B,-1), (D, -1)


run = True
display = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()


while run:
    clock.tick(60)
    mx, my = pygame.mouse.get_pos()

    display.fill((100,100,100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for i in range(150):
        draw_circle_alpha(display, (255, 255, 255, 2), (mx, my), i)
    

    shadow = get_shadow(mx,my, 300,300, 50)

    try:
        slope1 = (my-shadow[0][0][1])/(mx-shadow[0][0][0])
        slope2 = (my-shadow[1][0][1])/(mx-shadow[1][0][0])
    except ZeroDivisionError:
        pass

    for i in range(10):
        draw_polygon_alpha(display, (100, 100, 100, 100-5*i),
                          [(shadow[0][0][0] + 10*i*shadow[0][1], shadow[0][0][1] + slope1*i*shadow[0][1]),
                           (shadow[0][0][0], shadow[0][0][1]),
                           (shadow[1][0][0], shadow[1][0][1]),
                           (shadow[1][0][0] + 10*i*shadow[1][1], shadow[1][0][1] + slope2*i*shadow[1][1])])

    pygame.draw.rect(display, (0, 0, 0), (300,300, 50, 50))

    pygame.display.update()

pygame.quit()
exit()
