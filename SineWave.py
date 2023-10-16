import pygame
import sys
import math


pygame.init()
screen = pygame.display.set_mode([800,400])
pygame.display.set_caption("Shapes")
pi = math.pi
coords = []

x, y = 0, 198
r, g = 255, 255
incX = True
addCoords = True

def drawAxes():
    pygame.draw.line(screen, (255,255,255), [0,200], [800,200])
    pygame.draw.line(screen, (255,255,255), [400,0], [400,400])

rotateX = False
i = 0
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                if incX == False:
                    rotateX = True
        
    rx = x*25
    ry = (math.sin((x)))*50

    if addCoords:
        coords.append((rx,ry))
    
    if rotateX:
        if i <= 6.28:
            pygame.draw.rect(screen, (0,0,0), [0,0,800,400])
            for coord in coords:
                newY= coord[1]*math.cos(i)
                x = coord[0]
                pygame.draw.ellipse(screen, (255,255,0), [398+x,y-newY,5,5])
                pygame.draw.ellipse(screen, (255,255,0), [398-x,y+newY,5,5])
            i += 0.01
        else:
            i = 0
    drawAxes()

    pygame.draw.ellipse(screen, (r,g,0), [398+rx,y-ry,5,5])
    pygame.draw.ellipse(screen, (r,g,0), [398-rx,y+ry,5,5])

    if x >= 1.57*4:
        incX = False
        addCoords = False
        rotateX = True
    if incX:
        x += 0.01
    pygame.time.delay(1)
    pygame.display.flip()
