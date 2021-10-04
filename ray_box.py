
import pygame
import numpy
import random

from pygame.version import ver

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 15)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
RED = (255, 0, 0)
display = pygame.display.set_mode((500, 300))


def generate_blocks(blocks=[]):
    blocks.clear()
    for _ in range(3):
        blocks.append(pygame.Rect(random.randint(0, 300),
                      random.randint(0, 300), 50, 50))
    return blocks


blocks = generate_blocks()
while True:
    mx, my = pygame.mouse.get_pos()
    coordinates = font.render(f'({mx},{my})', False, RED)

    display.fill(WHITE)
    for block in blocks:
        pygame.draw.rect(display, BLACK, block, 3)
        vertexs = [block.topleft, block.bottomleft,
                   block.bottomright, block.topright]
        to_draw = [True, True, True, True]
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
                pygame.draw.line(display, RED, (mx, my), v)

    pygame.draw.circle(display, GREY, (mx, my), 3)
    display.blit(coordinates, (mx-30, my-30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            blocks = generate_blocks()

    pygame.display.update()
