
from operator import index
import pygame
import numpy as np
import math
from itertools import groupby


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLUE = (65, 105, 225)
YELLOW = (255, 255, 0)

TILE_WIDTH = 50
ROW = 20
COL = 10

LIGHT_RADIUS = 100
LIGHT_ALPHA = 2.5
SHADOW_ALPHA = 50 


class Tile:
    def __init__(self):
        self.tile_list = [[0 for _ in range(ROW)] for _ in range(COL)]

    def draw(self):
        ''' Draw True in self.tile_list '''
        for x, row in enumerate(self.tile_list):
            for y, col in enumerate(row):
                if col == 1:
                    rect = pygame.Rect(y*TILE_WIDTH, x*TILE_WIDTH, TILE_WIDTH, TILE_WIDTH)
                    rect.center = (y*TILE_WIDTH + 1/2*TILE_WIDTH,
                                   x*TILE_WIDTH + 1/2*TILE_WIDTH)
                    pygame.draw.rect(display, BLACK, rect)

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

    def get_vertexs(self, walls):
        ''' return vertexs '''
        if len(walls) > 0:
            vertexs = list(set([edge[1] for edge in walls] + [edge[2] for edge in walls]))

        return vertexs

    def offset_vertexs(self, x, y, walls, vertexs, offset=0.001, dummy_length=1000):
        ''' return offseted vertexs in grid system '''
        offsets = [v for v in vertexs]
        
        for vx, vy in vertexs:
            rad = math.atan2(vx*TILE_WIDTH-x, vy*TILE_WIDTH-y)
            c_clockwise, clockwise = rad-offset, rad+offset

            dummy_1 = (x + dummy_length*math.sin(c_clockwise),
                       y + dummy_length*math.cos(c_clockwise))
            dummy_2 = (x + dummy_length*math.sin(clockwise),
                       y + dummy_length*math.cos(clockwise))

            offsets = offsets + [(x/TILE_WIDTH, y/TILE_WIDTH) for x,y in [dummy_1, dummy_2]]
        return offsets

class Ray:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def check_collision(self, walls, offsets) -> list:
        ''' pass in offseted vertexs -> return lists of nearest collision points in grid system'''

        def voxel(p):
            ''' round up coords to pass in fuz_filter'''
            return tuple(round(x, 1) for x in p)
    
        def fuz_filter(points):
            return list({voxel(p):p for p in points}.values())

        collide_points = []
        for vx, vy in offsets:
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

        # remove similar/duplicate points to reduce the amount of ray : Credits to u/chimeraA_!
        collide_points = list(set(collide_points))
        fuz_points = fuz_filter(collide_points)

        return sorted(fuz_points, key=lambda x: math.atan2(x[1]-self.y/TILE_WIDTH, x[0]-self.x/TILE_WIDTH))

    def draw_shadow(self, points):
        ''' pass in valid points, return polygons of shadows -> [[(coord),(coord)], []..] '''
        # for i, p in enumerate(points):
        #     font = pygame.font.SysFont('Arial',10)
        #     render =font.render(f'{i}', True, RED)
        #     display.blit(render, (p[0]*TILE_WIDTH+5, p[1]*TILE_WIDTH+5))

        def get_missing(points, given):
            leng = len(points)
            target = [i for i in range(leng)]
            output = [list(g) for t, g in groupby(target, key=lambda x: x in given) if not t]
            if output and output[0][0] == target[0] and output[-1][-1] == target[-1]:
                output[-1] += output.pop(0)
            print(output)
            
            for l in output:
                if l[0]-1<0:         l = [l[-1]] + l + [l[0]+1]
                elif l[-1]+1 > leng: l = [l[0]-1] + l + [0]
                else:                l = [l[0]-1] + l + [l[-1]+1]
            print(output)

            return output


        if len(points) > 8:
            indexes = [i for i, (x,y) in enumerate(points) if x != 0 and y != 0]
            missings = get_missing(points, indexes)


    def draw_lights(self, collide_points, fill=True):
        ''' connect all valid points '''
        grid_to_coord = [(np.array(c)*TILE_WIDTH).tolist() for c in collide_points]

        if fill:
            if len(collide_points) > 8 :
                tartget_rect = pygame.Rect(0, 0, ROW*TILE_WIDTH+1, COL*TILE_WIDTH+1)
                surface = pygame.Surface(tartget_rect.size, pygame.SRCALPHA)
                pygame.draw.polygon(surface, (*WHITE, SHADOW_ALPHA), grid_to_coord)
                display.blit(surface, tartget_rect)
        else:           
            for coord in grid_to_coord:
                pygame.draw.line(display, YELLOW, (self.x, self.y), coord)



class Mouse:
    def __init__(self, x, y):
        self.x = x 
        self.y = y
        self.pos = (self.x, self.y)
        
    def create_neighbors(self, radius=20, num=0):
        ''' return neighbors + self.pos in a list in coord system, create a 'fuzzy' look '''
        neighbors = [self.pos]

        if num == 0: return neighbors

        for i in range(0, 360, int(360/num)):
            x = self.x + radius*math.cos(math.radians(i))
            y = self.y + radius*math.sin(math.radians(i))
            neighbors.append((x, y))
        
        return neighbors
    

def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)






pygame.init()
pygame.display.set_caption('Shadow casting')
pygame.font.init()
display = pygame.display.set_mode((ROW*TILE_WIDTH+3, COL*TILE_WIDTH+3)) # +1 to properly show outline

clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 100) # 100 = 0.1sec -> counter -= x every 0.1 second.

counter = 100
text = pygame.font.SysFont('Arial', 100, bold=True)

tile = Tile()

while True: 
    display.fill(BLACK)
    tile.draw()

    ''' FPS stress test '''
    fps = str(int(clock.get_fps()))
    nBlocks = list(np.array(tile.tile_list).flat).count(1)
    fps_font = pygame.font.SysFont('Arial', 20)
    fps_render = fps_font.render(f'FPS : {fps} | Blocks : {nBlocks}', True, RED)
    display.blit(fps_render, (10, 10))

    ''' Mouse '''
    mx, my = pygame.mouse.get_pos()
    mouse = Mouse(mx, my)
    neighbors = mouse.create_neighbors(num=0)
    
    for n in neighbors:
        pygame.draw.circle(display, RED, n, 1)

    ''' Tile map '''
    walls = tile.get_walls()
    vertexs = tile.get_vertexs(walls)

    for wall in walls:
        pygame.draw.line(display, WHITE,
                         (wall[1][0]*TILE_WIDTH, wall[1][1]*TILE_WIDTH),
                         (wall[2][0]*TILE_WIDTH, wall[2][1]*TILE_WIDTH))
    
    ''' Draw rays '''
    for nx, ny in neighbors:
        offsets = tile.offset_vertexs(nx, ny, walls, vertexs) 
        ray = Ray(nx, ny)
        points = ray.check_collision(walls, offsets)
        ray.draw_shadow(points)
        ray.draw_lights(points, fill=True)
        

    ''' Light '''
    # for i in range(LIGHT_RADIUS):
    #     draw_circle_alpha(display, (*WHITE, LIGHT_ALPHA), (mx, my), i*1.5)


    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            counter -= 1
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            tile.color(tile.tile_list, mx, my)

    # Time
    # if counter < 0:
    #     display.blit(text.render('YOU LOSE', True, RED), (100,100))
    clock.tick(144)

    pygame.display.update()
