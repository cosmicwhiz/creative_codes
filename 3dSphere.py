import pygame
import numpy as np
from math import *
import random


pygame.init()
WIDTH, HEIGHT = 1300, 700

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("3D Sphere")

projectionMatrix = np.array([
    [1, 0, 0],
    [0, 1, 0]
])

class Sphere3D:
    def __init__(self, x, y, radius, gap, color, speed):
        self.x, self.y = x, y
        self.radius = radius
        self.gap = gap
        self.color = color
        self.points = []
        self.xMove, self.yMove = random.choice((-1, 1)), random.choice((-1, 1))
        self.movementSpeed = speed
        self.angle = 0
        self.getPoints()
    
    def getPoints(self):
        theta = 0
        while theta <= pi:
            # radius makes phi angle with the x-axis
            phi = 0
            while phi < 2*pi:
                self.points.append([self.radius*sin(theta)*cos(phi), self.radius*sin(theta)*sin(phi), 
                                self.radius*cos(theta)])
                phi += self.gap
            theta += pi/20

        self.points = np.array(self.points)
    
    def draw(self):
        rotationX = np.array([
            [1, 0, 0],
            [0, cos(self.angle), -sin(self.angle)],
            [0, sin(self.angle), cos(self.angle)]
        ])

        rotationY = np.array([
            [cos(self.angle), 0, -sin(self.angle)],
            [0, 1, 0],
            [sin(self.angle), 0, cos(self.angle)]
        ])
        
        rotationZ = np.array([
            [cos(self.angle), -sin(self.angle), 0],
            [sin(self.angle), cos(self.angle), 0],
            [0, 0, 1]
        ])
        for point in self.points:
            rotatedMatrix = np.dot(rotationX, point)
            rotatedMatrix = np.dot(rotationY, rotatedMatrix)
            # rotatedMatrix = np.dot(rotationZ, rotatedMatrix)
            x, y = np.dot(projectionMatrix, rotatedMatrix)
            pygame.draw.circle(screen, self.color, (self.x+x, self.y+y), 1)
        
        self.angle += 0.01

        # to control the movement direction
        if self.xMove == 1:
            self.x += self.movementSpeed
        elif self.xMove == -1:
            self.x -= self.movementSpeed
        if self.yMove == 1:
            self.y += self.movementSpeed
        elif self.yMove == -1:
            self.y -= self.movementSpeed

        # to detect the collisions with the window walls
        if self.x + self.radius >= WIDTH-25:
            self.xMove = -1
        elif self.x - self.radius <= 25:
            self.xMove = 1
        if self.y - self.radius <= 25:
            self.yMove = 1
        elif self.y + self.radius >= HEIGHT-25:
            self.yMove = -1



# offsetX, offsetY = WIDTH // 2, HEIGHT // 2
clock = pygame.time.Clock()
radii = [200]
colors = [(0,255,0), (255,255,0), (0,255,255), (255,0,255)]
curTime = 0

spheres = []
# get random spheres
for i in range(1):
    sphere = Sphere3D(random.randint(120, WIDTH-120), random.randint(120, HEIGHT-120), random.choice(radii), 
            pi/25, random.choice(colors), random.randint(3, 10))
    spheres.append(sphere)

while True:
    clock.tick(60)
    screen.fill((11, 11, 11))
    pygame.draw.rect(screen, (255, 255, 255), (20, 20, WIDTH-40, HEIGHT-40), 2, 5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    for sphere in spheres:
        sphere.draw()
        if pygame.time.get_ticks() - curTime >= 1000:
            # sphere.color = random.choice(colors)
            curTime = pygame.time.get_ticks()

    pygame.display.update()

