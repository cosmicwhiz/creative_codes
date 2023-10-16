import pygame
import sys
import numpy as np
from math import *


pygame.init()
WIDTH, HEIGHT = 1200, 600

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Tesseract")

projectionMatrix = np.array([
    [1, 0, 0],
    [0, 1, 0]
])

def getTesseract(x, y, z, w):
    return np.array([
        [-x, -y, z, w],
        [x, -y, z, w],
        [x, y, z, w], 
        [-x, y, z, w],
        [-x, -y, -z, w], 
        [x, -y, -z, w],
        [x, y, -z, w],
        [-x, y, -z, w],
        [-x, -y, z, -w],
        [x, -y, z, -w],
        [x, y, z, -w], 
        [-x, y, z, -w],
        [-x, -y, -z, -w], 
        [x, -y, -z, -w],
        [x, y, -z, -w],
        [-x, y, -z, -w]
    ])

projection3d = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0]
])

projection2d = np.array([
    [1, 0, 0],
    [0, 1, 0],
])

tesseract = getTesseract(50, 50, 50, 50)


def connectPoints(i, j, point):
    pygame.draw.line(screen, (255, 255, 255), (point[i][0], point[i][1]), (point[j][0], point[j][1]), 2)


def pointsConnector(points):
    connectPoints(0, 4, points)
    connectPoints(1, 5, points)
    connectPoints(2, 6, points)
    connectPoints(3, 7, points)

    connectPoints(0, 3, points)
    connectPoints(1, 2, points)
    connectPoints(4, 7, points)
    connectPoints(5, 6, points)

    connectPoints(0, 1, points)
    connectPoints(2, 3, points)
    connectPoints(4, 5, points)
    connectPoints(6, 7, points)

clock = pygame.time.Clock()
offsetX, offsetY = WIDTH // 2, HEIGHT // 2
angle = 0

while True:
    clock.tick(60)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    angle += 0.01

    rotationY = np.array([
        [cos(angle), 0, -sin(angle), 0],
        [0, 1, 0, 0],
        [sin(angle), 0, cos(angle), 0],
        [0, 0, 0, 1]
    ])

    rotationW = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, cos(angle), -sin(angle)],
        [0, 0, sin(angle), cos(angle)]
    ])

    for point in tesseract:
        rotatedPoint = np.dot(rotationY, point)
        rotatedPoint = np.dot(rotationW, rotatedPoint)
        projected3d = np.dot(projection3d, rotatedPoint)
        x, y = np.dot(projection2d, projected3d)
        pygame.draw.circle(screen, (255, 255, 255), (x+offsetX, y+offsetY), 2)
    
    pygame.display.update()
    