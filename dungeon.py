
from tkinter import Widget
from warnings import simplefilter
import pygame
import random
import math
import enum

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

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

    def __repr__(self):
        return (self.x, self.y, self.width, self.height)


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
            bend_point = x1 + (random.randint(0, distance_x) * x_incr)

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
            bend_point = y1 + (random.randint(0, distance_y) * y_incr)

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
        self.room = None
        self.path = None
        self.parent = None

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

        return self.children

    def create_room(self, min_room_size:int=1, min_cells_from_side:int=1):
        """Generates a room that fits within the Partition"""
        max_room_width = self.width - (2 * min_cells_from_side)
        max_room_height = self.height - (2 * min_cells_from_side)

        if max_room_width < min_room_size or max_room_height < min_room_size:
            return  # if too small, stop it

        room_width = random.randint(min_room_size, max_room_width)
        room_height = random.randint(min_room_size, max_room_height)
        
        room_x = self.x + random.randint(min_cells_from_side, self.width - room_width - 1)
        room_y = self.y + random.randint(min_cells_from_side, self.height - room_height - 1)

        self.room = Room(room_x, room_y, room_width, room_height)

        return self.room

    def create_key_point(self) -> tuple:
        """Generates a point that can be used to create a path between self and sibling"""
        key_point_x = (self.room.x*2 + self.room.width) /2
        key_point_y = (self.room.y*2 + self.room.height) /2

        return (key_point_x, key_point_y)


    def create_path_between_children(self) -> Path:
        """Generates a pathway between the key points of this partition's children"""
        child_0 = self.children[0]
        child_1 = self.children[1]

        if child_0 is not None and child_1 is not None:
            if child_0.key_point is None:
                child_0.create_key_point()

            if child_1.key_point is None:
                child_1.create_key_point()

            self.path = Path()
            x1, y1 = child_0.key_point
            x2, y2 = child_1.key_point

            self.path.connect_points(x1, y1, x2, y2)

            return self.path




def create_partitions(x: int, y: int, width: int, height: int, divisions: int, memo=set()):
    """Generates an initial MapPartition and recursively creates children to the depth specified"""
    partition = Partition(x, y, width, height)
    if divisions > 1:
        if (aspect_ratio := partition.width/partition.height) == 1:
            divide_direction = Direction(random.randint(1, 2))
        else:
            divide_direction = Direction(1) if aspect_ratio > 1 else Direction(2)


        child_1, child_2 = partition.create_children(divide_direction)
        if child_1 and child_2:
            # partition.create_path_between_children()
            create_partitions(child_1.x, child_1.y, child_1.width, child_1.height, divisions-1, memo)
            create_partitions(child_2.x, child_2.y, child_2.width, child_2.height, divisions-1, memo)

    else:
        room = partition.create_room()
        if room:
            center_x, center_y = partition.create_key_point()
            pygame.draw.circle(display, RED, (center_x*40, center_y*40), 5)
            memo.add(room.__repr__()) 
    return memo


TILE_WIDTH = 40

pygame.init()

run = True
display = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()

cells = create_partitions(0, 0, 32, 18, 4)

while run:
    # display.fill(BLACK)
    for x,y,w,h in cells:
        if (x,y,w,h) is not None:
            pygame.draw.rect(display, WHITE, (x*TILE_WIDTH, y*TILE_WIDTH, w*TILE_WIDTH, h*TILE_WIDTH),1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            display.fill(BLACK)
            cells = create_partitions(0, 0, 32, 18, 4, memo=set())
            

    pygame.display.update()
