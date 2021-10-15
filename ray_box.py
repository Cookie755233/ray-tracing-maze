
from typing import List
import pygame
import numpy as np
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
RED = (255, 0, 0)

TILE_WIDTH = 30
ROW = 20
COL = 20

class Tile:
    def __init__(self):
        self.tile_list = [[0 for _ in range(ROW)] for _ in range(COL)]

    def draw(self):
        ''' Draw where the mouse is clicked '''
        for y, col in enumerate(self.tile_list):
            for x, row in enumerate(col):
                if row == 1 :
                    pygame.draw.rect(display, BLACK, (x*TILE_WIDTH, y*TILE_WIDTH, TILE_WIDTH, TILE_WIDTH))

    def to_poly_map(self) -> list:
        ''' Create lists of [(start_point, end_point), ...] '''
        
        

        pass


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
    coordinates = font.render(f'({mx},{my})', False, RED)
    
    display.fill(WHITE)

    world_map.draw()

    pygame.draw.circle(display, GREY, (mx, my), 3)
    display.blit(coordinates, (mx-30, my-30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            color(world_map.tile_list, mx, my)

    pygame.display.update()
