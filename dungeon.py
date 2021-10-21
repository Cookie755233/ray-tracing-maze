
import pygame
import random
import math
import enum

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

TILE_WIDTH = 25
ROW = 20
COL = 10

class Direction(enum.Enum):
    DIV_X = 1
    DIV_Y = 2 

class TileTypes(enum.Enum):
    EMPTY = "empty"
    FLOOR = "floor"
    PATH = "path"

class Room:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self): 
        return f'{self.x}, {self.y}'
        
    def __repr__(self):
        return self.x, self.y, self.width, self.height

    def create_rect(self):
        return self.x*TILE_WIDTH, self.y*TILE_WIDTH, self.width*TILE_WIDTH, self.height*TILE_WIDTH

    def create_key_point(self) -> tuple:
        """Generates a point that can be used to create a path between self and sibling"""
        x, y = self.x + self.width/2, self.y + self.height/2
        return x*TILE_WIDTH, y*TILE_WIDTH

class Path:
    def __init__(self):
        self.path = []

    def connect_points(self, x1: int, y1: int, x2: int, y2: int) -> list:
        """Connect points using L or Z shaped paths"""
        self.path = [(x1, y1)] # clear any existing path

        delta_x = x2 - x1
        delta_y = y2 - y1
        distance_x = abs(delta_x)
        distance_y = abs(delta_y)

        x_incr = 0 if distance_x == 0 else delta_x / distance_x
        y_incr = 0 if distance_y == 0 else delta_y / distance_y

        x = x1
        y = y1

        force_decision = 0
        if distance_x == distance_y:
            force_decision = random.randint(1, 2) # if the x any y distances are equal, randomly pick a direction

        if force_decision == 1 or distance_x > distance_y:
            bend_point = x1 + (random.randint(0, int(distance_x)) * x_incr)

            while True:
                if x == bend_point:
                    while True:
                        y += y_incr
                        self.path.append((x, y))

                        if y == y2:
                            break

                x += x_incr
                self.path.append((x, y))

                if x == x2:
                    break

        elif force_decision == 2 or distance_x < distance_y:
            bend_point = y1 + (random.randint(0, int(distance_y)) * y_incr)

            while True:
                if y == bend_point:
                    while True:
                        x += x_incr
                        self.path.append((x, y))

                        if x == x2:
                            break

                y += y_incr
                self.path.append((x, y))

                if y == y2:
                    break

        return self.path


class Partition:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.children = (None, None)
        self.path = None
        self.parent = None

    def __str__(self): return f'{self.x}, {self.y}'

    def __repr__(self):
        return (self.x, self.y, self.width, self.height)

    def create_children(self, direction=Direction, divide_range=0.7)-> tuple:
        '''Generate children cells by splitting the parent along a random axis'''
        portion = (2*random.random() - 1) * divide_range

        if direction is Direction.DIV_X:
            divide_x = math.trunc(self.width/2 + self.width/2*portion) 
            child_1 = child_2 = None
            
            if divide_x > 0 and divide_x < self.width:
                child_1 = Partition(self.x, self.y, divide_x, self.height)
                child_1.parent = self
                child_2 = Partition(self.x + divide_x, self.y, self.width - divide_x, self.height)
                child_2.parent = self
            self.children = (child_1, child_2)

        else:
            divide_y = math.trunc(self.height/2 + self.height/2*portion)
            child_1 = child_2 = None

            if divide_y > 0 and divide_y < self.height:
                child_1 = Partition(self.x, self.y, self.width, divide_y)
                child_1.parent = self
                child_2 = Partition(self.x, self.y+divide_y, self.width, self.height - divide_y)
                child_2.parent = self
            self.children = (child_1, child_2)

        return self.children # (Partition, Partition)

    def create_room_object(self, min_room_size:int=2, min_cells_from_side:int=1):
        """Generates a room that fits within the Partition -> Room object or None"""
        max_room_width = self.width - (2 * min_cells_from_side)
        max_room_height = self.height - (2 * min_cells_from_side)

        if max_room_width < min_room_size or max_room_height < min_room_size:
            return # if too small, return False

        room_width = random.randint(min_room_size, max_room_width)
        room_height = random.randint(min_room_size, max_room_height)
        
        room_x = self.x + random.randint(min_cells_from_side, self.width - room_width - 1)
        room_y = self.y + random.randint(min_cells_from_side, self.height - room_height - 1)

        return Room(room_x, room_y, room_width, room_height) 


def draw_room(x: int, y: int, width: int, height: int, divisions: int):
    parent = Partition(x, y, width, height)

    if divisions > 0:
        # avoid random cuts in one side only #
        if (aspect_ratio := parent.width/parent.height) == 1:
            divide_direction = Direction(random.randint(1, 2))
        else:
            divide_direction = Direction(1) if aspect_ratio > 1 else Direction(2)

        child_1, child_2 = parent.create_children(divide_direction)

        if child_1 and child_2:
            # draw partitions 
            # pygame.draw.rect(display, WHITE, (child_1.x*TILE_WIDTH, child_1.y*TILE_WIDTH, child_1.width*TILE_WIDTH, child_1.height*TILE_WIDTH),1)
            # pygame.draw.rect(display, WHITE, (child_2.x*TILE_WIDTH, child_2.y*TILE_WIDTH, child_2.width*TILE_WIDTH, child_2.height*TILE_WIDTH),1)

            # create room if room width/height > 2 else return None
            room_1 = child_1.create_room_object()
            room_2 = child_2.create_room_object()

            if room_1 and (divisions-1 == 0):
                rect_1 = room_1.create_rect()
                x1, y1 = room_1.create_key_point()
                pygame.draw.rect(display, YELLOW, rect_1,1)
            if room_2 and (divisions-1 == 0):
                rect_2 = room_2.create_rect()
                x2, y2 = room_2.create_key_point()
                pygame.draw.rect(display, RED, rect_2,1)
                
            draw_room(child_1.x, child_1.y, child_1.width, child_1.height, divisions-1)
            draw_room(child_2.x, child_2.y, child_2.width, child_2.height, divisions-1)






pygame.init()
clock = pygame.time.Clock()

display = pygame.display.set_mode((ROW*2*TILE_WIDTH+3, COL*2*TILE_WIDTH+3))

div = 1
while True:
    display.fill(BLACK)
    cells = draw_room(0, 0, ROW*2, COL*2, div)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                div += 1
            if event.key == pygame.K_DOWN:
                div -=1
                
            

    pygame.display.update()
