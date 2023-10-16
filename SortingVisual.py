import pygame
import sys
import random


pygame.init()
WIDTH, HEIGHT = 1001, 600

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Sort Visual")

class SortRect:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height

    def draw(self):
        coords = [
            (self.x, self.y),
            (self.x+self.width, self.y), 
            (self.x+self.width, self.y-self.height), 
            (self.x, self.y-self.height)
        ]
        pygame.draw.polygon(screen, (224, 25, 92), coords)
        pygame.draw.polygon(screen, (255, 255, 255), coords, 1)


rectWidth = 10
totalElements = 100
baseHeight = 6
elements = [n for n in range(1, 101)]
arr = []
for i in range(totalElements):
    ind = random.randint(0, totalElements-1)
    arr.append(elements[ind])
    elements.pop(ind)
    totalElements -= 1
print(arr)

rectangles = []
for i in range(100):
    rect = SortRect(rectWidth*i, HEIGHT, rectWidth, arr[i]*baseHeight)
    rectangles.append(rect)

clock = pygame.time.Clock()
i, j = 0, 0

while True:
    screen.fill((0, 0, 0))
    clock.tick(300)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    for r in rectangles:
        r.draw()

    if i < 100:
        if arr[j] > arr[j+1]:
            rectangles[j].height, rectangles[j+1].height = rectangles[j+1].height, rectangles[j].height
            arr[j], arr[j+1] = arr[j+1], arr[j]
        if j < 98-i:
            j += 1
        else:
            i += 1
            j = 0
    pygame.display.update()