
import pygame
import numpy as np
import random

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 15)
display = pygame.display.set_mode((500, 300))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
RED = (255, 0, 0)

class Block:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.topleft = (x, y)
        self.bottomleft = (x, y+width)
        self.bottomright = (x+width, y+width)
        self.topright = (x+width, y)

    def draw(self):
        pygame.draw.line(display, RED, self.topleft, self.bottomleft, 2)
        pygame.draw.line(display, RED, self.bottomleft, self.bottomright, 2)
        pygame.draw.line(display, RED, self.bottomright, self.topright, 2)
        pygame.draw.line(display, RED, self.topright, self.topleft, 2)


def generate_blocks(blocks=[]):
    blocks.clear()
    for _ in range(1):
        blocks.append(pygame.Rect(random.randint(0, 300),
                      random.randint(0, 300), 50, 50))
    return blocks
def checkCollision(block_start, block_end, ray_start, ray_end):
    x1 = block_start[0]
    y1 = block_start[1]
    x2 = block_end[0]
    y2 = block_end[1]
    x3 = ray_start[0]
    y3 = ray_start[1]
    x4 = ray_end[0]
    y4 = ray_end[1]

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
        collidePos = (x, y)
        return collidePos




blocks = generate_blocks()
while True:
    mx, my = pygame.mouse.get_pos()
    coordinates = font.render(f'({mx},{my})', False, RED)
    
    display.fill(WHITE)
    for block in blocks:
        pygame.draw.rect(display, BLACK, block, 3)
        Block(100,100,50).draw()
        vertexs = [block.topleft, block.bottomleft,
                   block.bottomright, block.topright]
        '''to_draw = [True, True, True, True]
        for i, j in vertexs:
            if mx > i:
                if my > j:
                    to_draw[0] = False
                else:
                    to_draw[1] = False
            else:
                if my < j:
                    to_draw[2] = False
                else:
                    to_draw[3] = False
        for v, t in zip(vertexs, to_draw):
            if t:
                pygame.draw.line(display, RED, (mx, my), v)'''

    pygame.draw.circle(display, GREY, (mx, my), 3)
    display.blit(coordinates, (mx-30, my-30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            blocks = generate_blocks()

    pygame.display.update()
