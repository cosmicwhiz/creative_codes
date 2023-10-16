import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1366, 770
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Fourier Series")

clock = pygame.time.Clock()

fontColor = (3, 207, 252)
fontSize = 24
fontGap = (28/30)*fontSize
fontOffset = (1/6)*fontSize
font = pygame.font.SysFont("Orbitron", fontSize)

one = font.render("1", True, fontColor)
zero = font.render("0", True, fontColor)

digits = [one, zero]

while True:
    # clock.tick(60)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
    i = 5
    while i < WIDTH:
        j = 5
        while j < HEIGHT:
            screen.blit(random.choice(digits), (i, j))
            j += fontGap
        i += fontGap
    pygame.time.delay(100)
    pygame.display.update()