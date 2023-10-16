import pygame
import numpy as np

pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])

cx, cy = (WIDTH//2, HEIGHT//2)
#edge distance from origin
hEdge, vEdge = 1000, 1000
#gap between each line
lineGap = 40

hLines, vLines = vEdge // lineGap, hEdge // lineGap
leftCoords, rightCoords = [], []
topCoords, bottomCoords = [], []

#setting up horizontal coordinates
leftCoords.append((cx-hEdge, cy))
rightCoords.append((cx+hEdge, cy))

for i in range(1, vLines+1):
    dy = i*lineGap
    leftCoords.append((cx-hEdge, cy+dy))
    rightCoords.append((cx+hEdge, cy+dy))
    leftCoords.append((cx-hEdge, cy-dy))
    rightCoords.append((cx+hEdge, cy-dy))

#setting up vertical coordinates
topCoords.append((cx, cy-vEdge))
bottomCoords.append((cx, cy+vEdge))

for i in range(1, hLines+1):
    dx = i*lineGap
    topCoords.append((cx+dx, cy-vEdge))
    bottomCoords.append((cx+dx, cy+vEdge))
    topCoords.append((cx-dx, cy-vEdge))
    bottomCoords.append((cx-dx, cy+vEdge))

vectors = []
curX = 1
for v in range(20):
    vectors.append((7, 0))
    curX += 0.25
angles = [0 for x, y in vectors]
angleMult = []
curMul = 1
for i in range(len(angles)):
    angleMult.append(0.001*curMul)
    curMul += 1
vectors = np.array(vectors)
totalVectors = len(vectors)

# 2D plane points
phi = 0.01    # Initial orientation of plane
plane_points = []
plane_size = 320
plane_gap = 40

plane_rows = plane_size // plane_gap
plane_size_half = plane_size // 2
for y in range(-plane_size_half, plane_size_half+1, plane_gap):
    points_row = []
    for x in range(-plane_size_half, plane_size_half+1, plane_gap):
        points_row.append((x, y))
    plane_points.append(points_row)

gridColor = (61, 61, 61)
axesColor = (200, 200, 200)
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    screen.fill((16, 16, 16))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # # draw the cartesian plane
    # for i in range(1, 2*vLines+1):
    #     pygame.draw.line(screen, gridColor, leftCoords[i], rightCoords[i])
    #     pygame.draw.line(screen, gridColor, topCoords[i], bottomCoords[i])
    # # x-axis and y-axis
    # pygame.draw.line(screen, axesColor, leftCoords[0], rightCoords[0])
    # pygame.draw.line(screen, axesColor, topCoords[0], bottomCoords[0])


    # for i in range(totalVectors):
    #     phi = angles[i]
    #     rotation = np.array([
    #         [np.cos(phi), -np.sin(phi)],
    #         [np.sin(phi), np.cos(phi)]
    #     ])
    #     x, y = np.dot(rotation, vectors[i])
    #     pygame.draw.line(screen, (71, 236, 255), (cx, cy), (cx+x*lineGap, cy+y*lineGap), 2)
    #     angles[i] -= angleMult[i]


    # Draw the Plane
    # for p_row in plane_points:
    #     for point in p_row:
    #         rotation = np.array([
    #             [np.cos(phi), -np.sin(phi)],
    #             [np.sin(phi), np.cos(phi)]
    #         ])
    #         x, y = np.dot(rotation, point)
    #         pygame.draw.circle(screen, (215, 236, 12), (cx+x, cy+y), 2)


    for row in range(plane_rows+1):
        for col in range(plane_rows):
            curx, cury = plane_points[row][col]
            nx, ny = plane_points[row][col+1]
            pygame.draw.line(screen, (140, 140, 140), (cx+curx, cy+cury), (cx+nx, cy+ny))


    for row in range(plane_rows):
        for col in range(plane_rows+1):
            curx, cury = plane_points[row][col]
            nx, ny = plane_points[row+1][col]
            pygame.draw.line(screen, (180, 180, 180), (cx+curx, cy+cury), (cx+nx, cy+ny))


    for row in range(plane_rows+1):
        for col in range(plane_rows+1):
            rotation = np.array([
                [np.cos(phi), -np.sin(phi)],
                [np.sin(phi), np.cos(phi)]
            ])
            plane_points[row][col] = np.dot(rotation, plane_points[row][col])

    # Center Dot
    pygame.draw.circle(screen, (255,255,255), (cx, cy), 4)
    pygame.display.update()
