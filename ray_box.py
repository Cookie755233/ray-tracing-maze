
from typing import List
import pygame
import numpy as np
import random
import math

from pygame.version import ver


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLUE = (65, 105, 225)

TILE_WIDTH = 70
ROW = 15
COL = 10
LIGHT_RADIUS = 100
ALPHA_LEVEL = 2.5


class Tile:
    def __init__(self):
        self.tile_list = [[0 for _ in range(ROW)] for _ in range(COL)]

    def draw(self):
        ''' Draw True in self.tile_list '''
        for x, row in enumerate(self.tile_list):
            for y, col in enumerate(row):
                if col == 1:
                    rect = pygame.Rect(y*TILE_WIDTH, x*TILE_WIDTH, TILE_WIDTH-5, TILE_WIDTH-5)
                    rect.center = (y*TILE_WIDTH + 1/2*TILE_WIDTH,
                                   x*TILE_WIDTH + 1/2*TILE_WIDTH)
                    pygame.draw.rect(display, WHITE, rect)

    def color(self, map, mx, my):
        ''' invert tiles' True/False '''
        col, row = mx//TILE_WIDTH, my//TILE_WIDTH
        if not map[row][col]:
            map[row][col] = True
        else:
            map[row][col] = False

    def get_walls(self, edge_ID=0):
        ''' Create lists of [(start_point, end_point), ...] '''

        def check(row, col, walls):
            ''' Check each edge if they have colored neighbor or not '''
            lefts = [left for left in walls if left[0] == 'LEFT']
            tops = [top for top in walls if top[0] == 'TOP']
            rights = [right for right in walls if right[0] == 'RIGHT']
            bottoms = [bottom for bottom in walls if bottom[0] == 'BOTTOM']

            # check left
            if not self.tile_list[row][col-1]:
                if len(lefts) == 0:
                    walls.append(['LEFT', (col, row), (col, row+1)])
                else:
                    for left in lefts:
                        if (col, row) == left[2]:
                            left[2] = (col, row+1)
                            break
                    else:
                        walls.append(['LEFT', (col, row), (col, row+1)])

            # check top
            if not self.tile_list[row-1][col]:
                if len(tops) == 0:
                    walls.append(['TOP', (col, row), (col+1, row)])
                else:
                    for top in tops:
                        if (col, row) == top[2]:
                            top[2] = (col+1, row)
                            break
                    else:
                        walls.append(['TOP', (col, row),  (col+1, row)])

            # check right : Chances that row/col+1 > row/col-1
            try:
                if not self.tile_list[row][col+1]:
                    if len(rights) == 0:
                        walls.append(['RIGHT', (col+1, row), (col+1, row+1)])
                    else:
                        for right in rights:
                            if (col+1, row) == right[2]:
                                right[2] = (col+1, row+1)
                                break
                        else:
                            walls.append(
                                ['RIGHT', (col+1, row),  (col+1, row+1)])
            except IndexError:
                walls.append(['RIGHT', (col+1, row),  (col+1, row+1)])

            # check bottom
            try:
                if not self.tile_list[row+1][col]:
                    if len(bottoms) == 0:
                        walls.append(
                            ['BOTTOM', (col, row+1), (col+1, row+1)])
                    else:
                        for bottom in bottoms:
                            if (col, row+1) == bottom[2]:
                                bottom[2] = (col+1, row+1)
                                break
                        else:
                            walls.append(['BOTTOM', (col, row+1),  (col+1, row+1)])
            except IndexError:
                walls.append(['BOTTOM', (col, row+1),  (col+1, row+1)])

        walls = [('EDGE', (0, 0), (ROW, 0)),
                   ('EDGE', (ROW, 0), (ROW, COL)),
                   ('EDGE', (ROW, COL), (0, COL)),
                   ('EDGE', (0, COL), (0, 0))]
        for x, row in enumerate(self.tile_list):
            for y, col in enumerate(row):
                if col == 1:
                    check(x, y, walls)

        return walls

    def get_vertexs(self, mx, my, edges):
        ''' return vertexs & sort in clockwise order'''
        if len(edges) > 0:
            vertexs = list(set([edge[1] for edge in edges] + [edge[2] for edge in edges]))

        return sorted(vertexs, key=lambda v: math.atan2(v[1]-my//TILE_WIDTH, v[0]-mx//TILE_WIDTH))

    def offset_vertexs(self, mx, my, vertexs, degrees=0.0001):
        for vx, vy in vertexs:
            angle = math.degrees(math.atan2(vx-mx, vy-my))
            c_clockwise = angle - degrees
            clockwise = angle + degrees

        


class Shadow:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def check_collision(self, walls, vertexs) -> list:
        ''' return lists nearest collision points '''
        collide_points = []
        for vx, vy in vertexs:
            temp =[]
            for wall in walls:
                x1, y1, x2, y2 = wall[1][0], wall[1][1], wall[2][0], wall[2][1]
                x3, y3, x4, y4 = self.x/TILE_WIDTH, self.y/TILE_WIDTH, vx, vy

                s1_x, s1_y = x2-x1, y2-y1
                s2_x, s2_y = x4-x3, y4-y3

                if (-s2_x*s1_y + s1_x*s2_y):
                    s = (-s1_y*(x1-x3) + s1_x*(y1-y3)) / (-s2_x*s1_y + s1_x*s2_y)
                    t = ( s2_x*(y1-y3) - s2_y*(x1-x3)) / (-s2_x*s1_y + s1_x*s2_y)

                    if 0 <= s <= 1 and 0 <= t <=1:
                        i_x = x1 + (t * s1_x)
                        i_y = y1 + (t * s1_y)
                        if all([i_x >= 0, i_y >= 0]):
                            temp.append((i_x, i_y))
                            
            temp.sort(key = lambda x: (x[0]-vx)**2 + (x[1]-vy)**2)
            if temp:
                collide_points.append(temp[-1])

        return list(set(collide_points))



def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


pygame.init()
pygame.font.init()
coord = pygame.font.SysFont('Arial', 15)
display = pygame.display.set_mode((ROW*TILE_WIDTH, COL*TILE_WIDTH))
# display = pygame.display.set_mode((1300,700))

clock = pygame.time.Clock()
# 100 = 0.1sec -> counter -= x every 0.1 second.
pygame.time.set_timer(pygame.USEREVENT, 100)
counter = 100
text = pygame.font.SysFont('Arial', 100, bold=True)

world_map = Tile()

while True:
    mx, my = pygame.mouse.get_pos()
    coordinates = coord.render(
        f'({mx//TILE_WIDTH},{my//TILE_WIDTH})', False, RED)

    display.fill(BLACK)

    world_map.draw()
    walls = world_map.get_walls()
    vertexs = world_map.get_vertexs(mx, my, walls)

    shadow = Shadow(mx, my)

    # for i in range(LIGHT_RADIUS):
    #     draw_circle_alpha(
    #         display, (255, 255, 255, ALPHA_LEVEL), (mx, my), i*1.5)

    for wall in walls:
        pygame.draw.line(display, BLUE,
                         (wall[1][0]*TILE_WIDTH, wall[1][1]*TILE_WIDTH),
                         (wall[2][0]*TILE_WIDTH, wall[2][1]*TILE_WIDTH), 1)
    # for x, y in vertexs:
        # pygame.draw.circle(display, PURPLE, (x*TILE_WIDTH, y*TILE_WIDTH), 3)
        # pygame.draw.line(display, BLUE, (mx, my),
        #                  (x*TILE_WIDTH, y*TILE_WIDTH), 1)

    shadows = shadow.check_collision(walls,vertexs)
    for x, y in shadows:
        pygame.draw.circle(display, RED, (x*TILE_WIDTH, y*TILE_WIDTH), 3)
        pygame.draw.line(display, BLUE, (mx,my), (x*TILE_WIDTH, y*TILE_WIDTH),1)
        

    pygame.draw.circle(display, GREY, (mx, my), 3)
    display.blit(coordinates, (mx, my+30))

    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            counter -= 1
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            world_map.color(world_map.tile_list, mx, my)

    # Time
    # if counter < 0:
    #     display.blit(text.render('YOU LOSE', True, RED), (100,100))
    # clock.tick(60)

    pygame.display.update()
