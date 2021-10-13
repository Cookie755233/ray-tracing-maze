
import pygame
import random
import math
import enum

class Direction(enum.Enum):
    DIV_X = 1
    DIV_Y = 2 

class Room:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Dungeon:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.children = (None, None)
        self.room = None
        self.path = None
        self.parent = None

    def create_children(self, direction=Direction)-> tuple:
        '''Generate children cells by splitting the parent along a random axis'''
        
        portion = random.uniform(0.3, 0.7)

        if direction is Direction.DIV_X:
            divide_x = math.trunc(self.width/2 + self.width/2*portion) 
            
            child_1 = None
            child_2 = None

            if divide_x > 0 and divide_x < self.width:
                child_1 = Dungeon(self.x, self.y, divide_x, self.height)
                child_1.parent = self

                child_2 = Dungeon(self.x + divide_x, self.y, self.width - divide_x, self.height)
                child_2.parent = self

            self.children = (child_1, child_2)
        
        else:
            divide_y = math.trunc(self.height/2 + self.height/2*portion)
            
            child_1 = None
            child_2 = None

            if divide_y > 0 and divide_y < self.width:
                child_1 = Dungeon(self.x, self.y, divide_y, self.height)
                child_1.parent = self

                child_2 = Dungeon(self.x + divide_y, self.y, self.width - divide_y, self.height)
                child_2.parent = self
        
            self.children = (child_1, child_2)

        return self.children

    # def create_room(self, min_room_size:int=2, min_cells_from_side:int=1):
    #     """Generates a room that fits within the Dungeon"""
    #     max_room_width = self.width - (2 * min_cells_from_side)
    #     max_room_height = self.height - (2 * min_cells_from_side)

    #     if max_room_width < min_room_size or max_room_height < min_room_size:
    #         return  # if too small, stop it

    #     room_width = random.randint(min_room_size, max_room_width)
    #     room_height = random.randint(min_room_size, max_room_height)
        
    #     room_x = self.x + random.randint(min_cells_from_side, self.width - room_width - 1)
    #     room_y = self.y + random.randint(min_cells_from_side, self.height - room_height - 1)

    #     self.room = Room(room_x, room_y, room_width, room_height)

    #     return self.room


def create_partitions(x: int, y: int, width: int, height: int, divisions: int) -> Dungeon:
    """Generates an initial MapPartition and recursively creates children to the depth specified"""
    partition = Dungeon(x, y, width, height)

    recurse_partitions(partition, divisions)

    return partition

def recurse_partitions(partition: Dungeon, divisions: int) -> None:
    """Recursively generates children MapPartitions to the depth specified"""
    if divisions == 0:
        # partition.create_room() # create a room in each of the final level partitions
        return

    aspect_ratio = partition.width / partition.height

    divide_direction = Direction(1) if aspect_ratio > 1 else Direction(2)

    if aspect_ratio == 1:
        divide_direction = Direction(random.randint(1, 2))

    child_1, child_2 = partition.create_children(divide_direction)

    if child_1 is not None:
        recurse_partitions(child_1, divisions - 1)
    if child_2 is not None:
        recurse_partitions(child_2, divisions - 1)

create_partitions(0, 0, 200, 200, 4)












# pygame.init()

# display = pygame.display.set_mode((500, 500))
# clock = pygame.time.Clock()
# run = True

# while run:
#     display.fill((0, 0, 0))

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False

#     pygame.display.update()
