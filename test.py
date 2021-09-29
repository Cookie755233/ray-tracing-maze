import pygame
import random
import math

pygame.init()


def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


class Ray:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle=angle
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


def drawRays(ray, rectX, rectY, width, color):
    corners = [(rectX ,rectY), (rectX+width ,rectY),
             (rectX ,rectY+width), (rectX+width ,rectY+width)]
    distances = []
    for corner in corners:
        dx, dy = ray.x - corner[0], ray.y - corner[1]
        distances.append(math.sqrt(dx**2 + dy**2))
    


        pygame.draw.line(display, color, (ray.x, ray.y), closestPoint)
    else:
        closestPoint = (ray.x+100*math.cos(ray.angle*math.pi/180),
                        ray.y+100*math.sin(ray.angle*math.pi/180))
        pygame.draw.line(display, color, (ray.x, ray.y), closestPoint)



run = True
display = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()


while run:
    clock.tick(60)
    mx, my = pygame.mouse.get_pos()

    display.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for i in range(1, 150):
        draw_circle_alpha(display, (255,255,255,2), (mx, my), i)


    pygame.draw.rect(display,(0,0,0),(50,50,50,50))
    pygame.draw.rect(display,(0,0,0),(150,150,50,50))
    pygame.draw.rect(display,(0,0,0),(150,300,50,50))
    

    pygame.display.update()

pygame.quit()
exit()