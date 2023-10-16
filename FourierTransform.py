import pygame
import sys
from math import sin, cos, pi, radians
import random

pygame.init()

WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Fourier Series")

class FourierCircle:
    def __init__(self, centerCoords, startAngle, radius, angFreq):
        self.x, self.y = centerCoords
        self.radius = radius
        self.angFreq = angFreq
        self.angle = startAngle
        self.endx, self.endy = self.getEndCoords()
    
    def getEndCoords(self):
        return (self.x+self.radius*cos(self.angle), self.y+self.radius*sin(self.angle))
    
    def fourierDraw(self, screen, circleCol, lineCol):
        pygame.draw.circle(screen, circleCol, (self.x, self.y), self.radius, 2)
        # pygame.draw.line(screen, lineCol, (self.x, self.y), (self.endx, self.endy), 2)
        self.angle += self.angFreq
        self.endx, self.endy = self.getEndCoords()

clock = pygame.time.Clock()

# generate all the cirlces
fourierCircles = []
totalFourierCircles = 1000

firstCircle = FourierCircle((WIDTH//2, HEIGHT//2), radians(80), 30, 0)
fourierCircles.append(firstCircle)

curFreq = 0.005
for i in range(1, totalFourierCircles):
    freqMultiplier = 1
    if i % 2 == 0:
        freqMultiplier = -1
    startCoords = fourierCircles[i-1].endx, fourierCircles[i-1].endy
    stAngle = radians(random.randint(0, 359))
    if i < 20:
        rad = random.randint(30, 50)
    else:
        rad = random.randint(1, 10)
    circle = FourierCircle(startCoords, stAngle, rad, freqMultiplier*curFreq)
    fourierCircles.append(circle)
    if i % 2 == 0:
        curFreq += 0.0005

# for c in fourierCircles:
#     print("Center:",(c.x, c.y)," EndCoords:",(c.endx, c.endy)," w:",c.angFreq, "Radius:",c.radius)
locus = []
animate = True
colors = [(84, 22, 180), (112, 39, 195), (185, 76, 225), (150, 0, 205), (164, 66, 220), (181, 100, 227), 
            (228, 0, 224), (236, 71, 233), (244, 47, 242), (0, 181, 236), (204, 255, 0), (255, 106, 0)]

while True:
    clock.tick(120)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE:
                if animate:
                    animate = False
                else:
                    animate = True
    
    fourierCircles[0].fourierDraw(screen, (66, 245, 236), (255, 255, 255))
    for i in range(1, totalFourierCircles):
        fc = fourierCircles[i]
        # if i < 20:
        #     lineCol = (0, 0, 0)
        # else:
        lineCol = (255, 255, 255)
        fc.fourierDraw(screen, (56, 225, 255), lineCol)
        fc.x, fc.y = fourierCircles[i-1].endx, fourierCircles[i-1].endy
    
    # if animate:
    #     locus.append([fourierCircles[-1].endx, fourierCircles[-1].endy])
    # for lx, ly in locus:
    #     pygame.draw.circle(screen, (255, 102, 168), (lx, ly), 1)

    pygame.display.update()