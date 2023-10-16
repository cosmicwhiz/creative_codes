import pygame
import numpy as np
from math import *


pygame.init()

WHITE = (255, 255, 255)
# color = (94, 255, 177)
# color = (255, 74, 161)
color = (3, 252, 223)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("3D Projection")

projectionMatrix = np.array([
        [1, 0, 0],
        [0, 1, 0]
    ])

xLimit, yLimit, zLimit = 150, 150, 150

edgePoints = np.array([
        [-xLimit, -yLimit, zLimit],
        [xLimit, -yLimit, zLimit],
        [xLimit, yLimit, zLimit], 
        [-xLimit, yLimit, zLimit],
        [-xLimit, -yLimit, -zLimit], 
        [xLimit, -yLimit, -zLimit],
        [xLimit, yLimit, -zLimit],
        [-xLimit, yLimit, -zLimit]
    ])

cubes = []
colorIndex = 0
incAmount = 25

inc = 0
while inc <= xLimit:
    points = []
    for x, y, z in edgePoints:
        if x < 0:
            points.append([x+inc, y, z])
        else:
            points.append([x-inc, y, z])
    cubes.append(np.array(points))
    inc += incAmount
    colorIndex += 1

yIndex = colorIndex
inc = 0
while inc <= yLimit:
    points = []
    for x, y, z in edgePoints:
        if y < 0:
            points.append([x, y+inc, z])
        else:
            points.append([x, y-inc, z])
    cubes.append(np.array(points))
    inc += incAmount
    colorIndex += 1

zIndex = colorIndex
inc = 0
while inc <= zLimit:
    points = []
    for x, y, z in edgePoints:
        if z < 0:
            points.append([x, y, z+inc])
        else:
            points.append([x, y, z-inc])
    cubes.append(np.array(points))
    inc += incAmount

angle = 0
rotating = True
offsetX = WIDTH//2
offsetY = HEIGHT//2
xTilt = 0.2
stretch = 1
clock = pygame.time.Clock()

def connectPoints(i, j, points):
    pygame.draw.line(screen, color, (points[i][0], points[i][1]), (points[j][0], points[j][1]), 1)

while True:
    clock.tick(60)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_p:
                if rotating:
                    rotating = False
                else:
                    rotating = True
    
    rotationX = np.array([
        [stretch, 0, 0],
        [0, cos(xTilt), -sin(xTilt)],
        [0, sin(xTilt), cos(xTilt)]
    ])

    rotationY = np.array([
        [cos(angle), 0, sin(angle)],
        [0, stretch, 0],
        [-sin(angle), 0, cos(angle)]
    ])
    
    rotationZ = np.array([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, stretch]
    ])

    projectedCubes = []
    if rotating:
        angle += -0.005
    
    for points in cubes:
        i = 0
        projectedPoints = [[n, n] for n in range(8)]
        for p in points:
            rotatedMatrix = np.dot(rotationY, p)
            rotatedMatrix = np.dot(rotationX, rotatedMatrix)
            rotatedMatrix = np.dot(rotationZ, rotatedMatrix)

            x, y = np.dot(projectionMatrix, rotatedMatrix)
            projectedPoints[i] = [offsetX+x, offsetY+y]
            # pygame.draw.circle(screen, WHITE, (offsetX+x, offsetY+y), 3)
            i += 1
        projectedCubes.append(projectedPoints)
    
    for projectedPoints in projectedCubes:
        connectPoints(0, 4, projectedPoints)
        connectPoints(1, 5, projectedPoints)
        connectPoints(2, 6, projectedPoints)
        connectPoints(3, 7, projectedPoints)

        connectPoints(0, 3, projectedPoints)
        connectPoints(1, 2, projectedPoints)
        connectPoints(4, 7, projectedPoints)
        connectPoints(5, 6, projectedPoints)

        connectPoints(0, 1, projectedPoints)
        connectPoints(2, 3, projectedPoints)
        connectPoints(4, 5, projectedPoints)
        connectPoints(6, 7, projectedPoints)

    pygame.display.update()

