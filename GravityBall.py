import pygame
import sys

pygame.init()

screen = pygame.display.set_mode([1000, 700])
pygame.display.set_caption("PhysicsBall")
clock = pygame.time.Clock()
font_color=(0,255,155)
font_obj=pygame.font.SysFont("calibri",20)

class Ball:
    def __init__(self, xpos, pos, u):
        self.position = pos
        self.displacement = 0
        self.initialVelocity = 400
        self.velocity = self.initialVelocity
        self.highestPoint = 0
        self.moveRight = False
        self.moveLeft = False
        self.x = xpos
        self.fallDirection = 1
        self.now = 0
    
    def simulate(self, simulation, acceleration, e):
        if simulation:    
            t = pygame.time.get_ticks() - self.now
            t = t/1000

            self.displacement = self.initialVelocity*t + (acceleration/2)*t*t 
            self.velocity = self.initialVelocity + acceleration*t

            if self.fallDirection == 1:
                if self.velocity >= 0: 
                    self.position = 560 - self.displacement
                else:
                    self.fallDirection = -1
                    self.now = pygame.time.get_ticks()
                    self.highestPoint = self.position
                    self.initialVelocity = 0
                    acceleration = -acceleration
            else:
                if self.position < 560:
                    self.position = self.highestPoint + self.displacement
                else:
                    self.fallDirection = 1
                    self.now = pygame.time.get_ticks()
                    self.initialVelocity = e * self.velocity
                    acceleration = -acceleration
    
ball = Ball(300, 560, 200)

def displayInfo(position, displacement, velocity, t):
    position_text = font_obj.render("Position: "+ str(round(position, 2)),True,font_color)
    displacement_text = font_obj.render("Displacement: "+ str(round(displacement, 2)),True,font_color)
    velocity_text = font_obj.render("Velocity: "+ str(round(velocity, 2)),True,font_color)
    time_elapsed = font_obj.render("Time: "+ str(round(t, 2)),True,font_color)
    return position_text, displacement_text, velocity_text, time_elapsed

#ball variables
position = 560
displacement = 0
initialVelocity = 400
velocity = initialVelocity
highestPoint = 0
moveRight = False
moveLeft = False
x = 400
fallDirection = 1

#environment variables
e = 0.8
acceleration = -800
now = 0
simulation = False
t = 0


while True:
    screen.fill((0,0,0))
    if highestPoint > 559:
        position = 560
        highestPoint = 0
        velocity = 0
        displacement = 0
        simulation = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not simulation:
                    simulation = True
                    initialVelocity = 400
                    now = pygame.time.get_ticks()
                    acceleration = -200
                    fallDirection = 1
            if event.key == pygame.K_d:
                moveRight = True
            if event.key == pygame.K_a:
                moveLeft = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moveRight = False
            if event.key == pygame.K_a:
                moveLeft = False

    position_text, displacement_text, velocity_text, time_elapsed = displayInfo(position, displacement, velocity, t)
    ball.simulate(True, -800, 0.8)
    if simulation:    
        t = pygame.time.get_ticks() - now
        t = t/1000

        displacement = initialVelocity*t + (acceleration/2)*t*t 
        velocity = initialVelocity + acceleration*t

        if fallDirection == 1:
            if velocity >= 0: 
                position = 560 - displacement
            else:
                fallDirection = -1
                now = pygame.time.get_ticks()
                highestPoint = position
                initialVelocity = 0
                acceleration = 800
        else:
            if position < 560:
                position = highestPoint + displacement
            else:
                fallDirection = 1
                now = pygame.time.get_ticks()
                initialVelocity = e * velocity
                acceleration = -800
        
    pygame.draw.ellipse(screen, [0, 255, 200], [x, position, 40, 40])
    pygame.draw.line(screen, [255,255,255], [0,600], [1000,600])
    
    screen.blit(displacement_text, (20, 50))
    screen.blit(velocity_text, (20, 70))
    screen.blit(position_text, (20, 30))
    screen.blit(time_elapsed, (20, 90))

    if moveRight:
        x += 0.1
    if moveLeft:
        x -= 0.1
    pygame.display.flip()