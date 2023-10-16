import pygame
import random


pygame.init()

WIDTH, HEIGHT = 1300, 650
pixelOnColor = (38, 251, 255)
pixelOffColor = (0, 0, 0)
borderColor = (0, 17, 209)
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("NeonFunk")

class Pixel:
    def __init__(self, x, y, size):
        self.x, self.y = x, y
        self.size = size
        self.isOn = False
        self.offset = self.size*0.2
    def draw(self):
        if self.isOn:
            pygame.draw.rect(screen, random.choice(colors), (self.x+self.offset, self.y+self.offset, 0.6*self.size, 0.6*self.size))
        else:
            pygame.draw.rect(screen, pixelOffColor, (self.x, self.y, self.size, self.size))
        pygame.draw.polygon(screen, borderColor, [[self.x, self.y], [self.x+pixelSize, self.y], 
                            [self.x+pixelSize, self.y+pixelSize], [self.x, self.y+pixelSize]], 1)


pixelSize = 50
colors = [(0,255,0), (255,255,0), (0,255,255), (255,0,255)]

pixelPoints = []
offset = 50
j = offset
while j < HEIGHT-40-offset:
    i = offset
    while i < WIDTH-40-offset:
        pixelPoints.append((i, j))
        i += pixelSize
    j += pixelSize

pixels = []
pixelMap = {}
for x, y in pixelPoints:
    p = Pixel(x, y, pixelSize)
    pixels.append(p)
    pixelMap[(x, y)] = p

clock = pygame.time.Clock()

pixelsModified = False
# currentPixels = []
# i, length = 0, len(pixels)
animation = False

while True:
    clock.tick(5)
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (20, 20, WIDTH-40, HEIGHT-40), 3, 10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_SPACE:
                if not animation:
                    animation = True
                else:
                    animation = False

    """ ---------------------------------------------
        |                                           |
        |       A N I M A T I O N   I               |
        |                                           |
        ---------------------------------------------
    """
    # No Signal Effect
    if not animation:
        for p in pixels:
            if random.randint(0, 2) == 1:
                p.isOn = True
            else:
                p.isOn = False
    for p in pixels:
        p.draw()
    
    pygame.time.wait(100)

    pygame.display.update()
