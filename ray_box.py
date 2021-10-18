
from typing import List
import pygame
import numpy as np
import random

from pygame.version import ver

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLUE = (65, 105, 225)

TILE_WIDTH = 40
ROW = 25
COL = 15

class Tile:
    def __init__(self):
        self.tile_list = [[0 for _ in range(ROW)] for _ in range(COL)]
        # for i, row in enumerate(self.tile_list):
        #     if not(i == 0 or i == ROW-1):
        #         row[1:-1] = [0 for _ in range(len(row)-2)]

    def draw(self):
        ''' Draw where the mouse is clicked '''
        for x, row in enumerate(self.tile_list):
            for y, col in enumerate(row):
                if col == 1 :
                    rect = pygame.Rect(y*TILE_WIDTH, x*TILE_WIDTH, TILE_WIDTH-5, TILE_WIDTH-5)
                    rect.center = (y*TILE_WIDTH + 1/2*TILE_WIDTH, x*TILE_WIDTH + 1/2*TILE_WIDTH)
                    pygame.draw.rect(display, BLACK, rect)

    def get_edges(self, edge_ID=0):
        ''' Create lists of [(start_point, end_point), ...] '''

        def check(row, col, outputs):
            ''' Check each edge if they have colored neighbor or not '''
            lefts = [left for left in outputs if left[0] == 'LEFT']
            tops = [top for top in outputs if top[0] == 'TOP']
            rights = [right for right in outputs if right[0] == 'RIGHT']
            bottoms = [bottom for bottom in outputs if bottom[0] == 'BOTTOM']
            
            # check left
            if not self.tile_list[row][col-1]:
                if len(lefts) == 0:
                    outputs.append(['LEFT', (col, row), (col, row+1)])
                else:
                    for left in lefts:
                        if (col,row) == left[2]:
                            left[2] = (col, row+1)
                            break
                    else:
                        outputs.append(['LEFT', (col, row), (col, row+1)])
            
            # check top 
            if not self.tile_list[row-1][col]:
                if len(tops) == 0:
                    outputs.append(['TOP', (col, row), (col+1, row)])
                else:
                    for top in tops:
                        if (col,row) == top[2]:
                            top[2] = (col+1, row)
                            break
                    else:
                        outputs.append(['TOP', (col, row),  (col+1, row)])

            # check right : Chances that row/col+1 > row/col-1
            try:
                if not self.tile_list[row][col+1]:
                    if len(rights) == 0:
                        outputs.append(['RIGHT', (col+1, row), (col+1, row+1)])
                    else:
                        for right in rights:
                            if (col+1,row) == right[2]:
                                right[2] = (col+1, row+1)
                                break
                        else:
                            outputs.append(['RIGHT', (col+1, row),  (col+1, row+1)])
            except IndexError: outputs.append(['RIGHT', (col+1, row),  (col+1, row+1)])

            # check bottom 
            try:
                if not self.tile_list[row+1][col]:
                    if len(bottoms) == 0:
                        outputs.append(['BOTTOM', (col, row+1), (col+1, row+1)])
                    else:
                        for bottom in bottoms:
                            if (col,row+1) == bottom[2]:
                                bottom[2] = (col+1, row+1)
                                break
                        else:
                            outputs.append(['BOTTOM', (col, row+1),  (col+1, row+1)])
            except IndexError: outputs.append(['BOTTOM', (col, row+1),  (col+1, row+1)])

        outputs = []
        for x, row in enumerate(self.tile_list):
            for y, col in enumerate(row):
                if col == 1:
                    check(x, y, outputs)

        return outputs
    
    def get_vertexs(self, edges, vertexs=[(0,0), (ROW, 0), (ROW, COL), (0, COL)]):
        if len(edges)>0:
            vertexs = [(0,0), (ROW, 0), (ROW, COL), (0, COL)] \
                + list(set([edge[1] for edge in edges] + [edge[2] for edge in edges]))

        return vertexs



def color(map, mx, my):
    col, row = mx//TILE_WIDTH, my//TILE_WIDTH
    if not map[row][col]:
        map[row][col] = True
    else: 
        map[row][col] = False

    
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 15)
display = pygame.display.set_mode((ROW*TILE_WIDTH, COL*TILE_WIDTH))

world_map = Tile()

while True:
    mx, my = pygame.mouse.get_pos()
    coordinates = font.render(f'({mx//TILE_WIDTH},{my//TILE_WIDTH})', False, RED)
    
    display.fill(WHITE)

    world_map.draw()
    edges = world_map.get_edges()
    vertexs = world_map.get_vertexs(edges)

    for edge in edges:
        pygame.draw.line(display, RED,
         (edge[1][0]*TILE_WIDTH, edge[1][1]*TILE_WIDTH),
         (edge[2][0]*TILE_WIDTH, edge[2][1]*TILE_WIDTH))
    for x, y in vertexs:
        pygame.draw.circle(display, PURPLE, (x*TILE_WIDTH, y*TILE_WIDTH), 1)
        pygame.draw.line(display, BLUE, (mx, my), (x*TILE_WIDTH, y*TILE_WIDTH), 1)

    pygame.draw.circle(display, GREY, (mx, my), 3)
    display.blit(coordinates, (mx, my+30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            color(world_map.tile_list, mx, my)

    pygame.display.update()
