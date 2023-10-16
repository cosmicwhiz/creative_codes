import pygame
import numpy as np
from math import *
import sys

pygame.init()
WIDTH, HEIGHT = 1300, 650

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Perspective Draw")

def getCubePoints(x, y, z):
    return np.array([
        [-x, -y, z],
        [x, -y, z],
        [x, y, z], 
        [-x, y, z],
        [-x, -y, -z], 
        [x, -y, -z],
        [x, y, -z],
        [-x, y, -z]
    ])

cubeX, cubeY, cubeZ = 150, 100, 150

room = getCubePoints(cubeX, cubeY, cubeZ)

timeX, timeY, timeZ = 50, 50, 50
timeBox = getCubePoints(timeX, timeY, timeZ)

px, py, pz = 0, 0, -500
cameraZ = -300
angle = 0
angleInc = pi/120
cameraInc = True

projectionMatrix = np.array([
    [1, 0, 0],
    [0, 1, 0]
])

def connectPoints(i, j, point):
    pygame.draw.line(screen, (255, 255, 255), (point[i][0], point[i][1]), (point[j][0], point[j][1]), 2)

offsetX, offsetY = WIDTH//2, HEIGHT//2
clock = pygame.time.Clock()
mx, my = 0, 0
rightbuttonClick = False
speed = 3

while True:
    clock.tick(60)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                mx, my = pygame.mouse.get_pos()
                rightbuttonClick = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                rightbuttonClick = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    if rightbuttonClick:
        x, y = pygame.mouse.get_pos()
        if x - mx > 0:
            angle -= 0.02
        elif x - mx < 0:
            angle += 0.02
        mx, my = x, y
    # angle += angleInc
    rotationY = np.array([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)]
    ])
    rotationNY = np.array([
        [cos(speed*angle), 0, sin(speed*angle)],
        [0, 1, 0],
        [-sin(speed*angle), 0, cos(speed*angle)]
    ])

    rotatedPoints = []
    timeRotationPoints = []
    for point in room:
        rotatedPoints.append(np.dot(rotationY, point))
    for point in timeBox:
        timeRotationPoints.append(np.dot(rotationNY, point))
    
    
    projectedPoints = []
    for x, y, z in rotatedPoints:
        l, m, n = x - px, y - py, z - pz
        t = (cameraZ-pz)/(z-pz)
        projectedX = px + t*l
        projectedY = py + t*m
        projectedPoints.append([offsetX+projectedX, offsetY+projectedY, cameraZ])
    
    timeProjectionPoints = []
    for x, y, z in timeRotationPoints:
        l, m, n = x - px, y - py, z - pz
        t = (cameraZ-pz)/(z-pz)
        projectedX = px + t*l
        projectedY = py + t*m
        timeProjectionPoints.append([offsetX+projectedX, offsetY+projectedY, cameraZ])    
    # for x, y, z in timeProjectionPoints:
    #     pygame.draw.circle(screen, (255, 255, 255), (x, y), 2)

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

    connectPoints(0, 4, timeProjectionPoints)
    connectPoints(1, 5, timeProjectionPoints)
    connectPoints(2, 6, timeProjectionPoints)
    connectPoints(3, 7, timeProjectionPoints)

    connectPoints(0, 3, timeProjectionPoints)
    connectPoints(1, 2, timeProjectionPoints)
    connectPoints(4, 7, timeProjectionPoints)
    connectPoints(5, 6, timeProjectionPoints)

    connectPoints(0, 1, timeProjectionPoints)
    connectPoints(2, 3, timeProjectionPoints)
    connectPoints(4, 5, timeProjectionPoints)
    connectPoints(6, 7, timeProjectionPoints)


    if cameraZ >= 400:
        cameraInc = False
    elif cameraZ <= -300:
        cameraInc = True
    if cameraInc:
        cameraZ += 2
        angle += angleInc
    else:
        cameraZ -= 2
        angle -= angleInc
    pygame.display.update()
