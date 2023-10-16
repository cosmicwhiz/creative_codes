import pygame
import random
import heapq


pygame.init()
WIDTH, HEIGHT = 400, 400

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("PathFinder")

class Cell:
    def __init__(self, x, y, size):
        self.x, self.y = x, y
        self.size = size
        self.isOn = False
        self.isCurrent = False
        self.isObstacle = False
        self.isPath = False
        self.offset = self.size // 5
    
    def draw(self):
        if self.isOn:
            if self.isCurrent:
                pygame.draw.rect(screen, (0,255,0), (self.x, self.y, self.size, self.size))
            elif self.isPath:
                pygame.draw.rect(screen, (0,255,0), (self.x, self.y, self.size, self.size), 1)
            else:
                pygame.draw.rect(screen, (48,85,65), (self.x, self.y, self.size, self.size), 1)
        elif self.isObstacle:
            pygame.draw.rect(screen, (200,0,0), (self.x, self.y, self.size, self.size), 1)
            # pygame.draw.line(screen, (255,0,0), (self.x+self.offset, self.y+self.offset), (self.x+self.size-self.offset, self.y+self.size-self.offset))
            # pygame.draw.line(screen, (255,0,0), (self.x-self.offset+self.size, self.y+self.offset), (self.x+self.offset, self.y+self.size-self.offset))
        else:
            pygame.draw.rect(screen, (21,21,21), (self.x, self.y, self.size, self.size), 1)


# create the grid cells
cellSize = 20
gridCells = []
grid = []

def generateGrid():
    curY = 0
    while curY + cellSize <= HEIGHT:
        curX = 0
        row, cellRow = [], []
        while curX + cellSize <= WIDTH:
            cell = Cell(curX, curY, cellSize)
            cellVal = 0
            if random.randint(1, 5) == 1:
                cell.isObstacle = True
                cellVal = 1                
            cellRow.append(cell)
            row.append(cellVal)
            curX += cellSize
        curY += cellSize
        grid.append(row)
        gridCells.append(cellRow)

    gridCells[0][0].isObstacle = gridCells[-1][-1].isObstacle = False

generateGrid()
clock = pygame.time.Clock()

rows, cols = HEIGHT//cellSize, WIDTH//cellSize

def isValid(x, y):
        return x >= 0 and y >= 0 and x < rows and y < cols

def neighbors(x, y):
    w = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    res = []
    for i, j in w:
        if isValid(i, j):
            res.append((i, j))
    return res

pq = [(0, 0, 0)]
visited = {}
totalWalls = rows*cols
findPath = True
prev = current = None

[visited.setdefault((i, j), 1e+9) for i in range(-1, rows) for j in range(-1, cols)]

path = []
pathLen = [0]
def getPath():
    i, j = rows-1, cols-1
    if visited[(i-1, j)] == visited[(i, j-1)] and visited[(i-1, j)] == 1e9:
        return
    while i >= 0 and j >= 0:
        path.append(gridCells[i][j])
        pathLen[0] += 1
        if visited[(i-1, j)] == visited[(i, j-1)]:
            options = [(0, -1), (-1, 0)]
            dx, dy = random.choice(options)
            i += dx
            j += dy
        elif visited[(i-1, j)] < visited[(i, j-1)]:
            i -= 1
        else:
            j -= 1
pathInd = 0

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
            if event.key == pygame.K_r:
                gridCells, grid = [], []
                generateGrid()
                pq = [(0, 0, 0)]
                findPath = True
                prev = current = None
                visited = {}
                [visited.setdefault((i, j), 1e+9) for i in range(-1, rows) for j in range(-1, cols)]
                path = []
                pathLen = [0]
                pathInd = 0
    
    if pq and findPath:
        u, row, col = heapq.heappop(pq)
        gridCells[row][col].isOn = True
        gridCells[row][col].isCurrent = True
        if prev: prev.isCurrent = False
        prev = gridCells[row][col]
        if row == rows-1 and col == cols-1:
            findPath = False
        if visited[(row, col)] <= u:
            continue
        visited[(row, col)] = u
        for r, c in neighbors(row, col):
            if grid[r][c] != 1:
                heapq.heappush(pq, (u+1, r, c))
    else:
        prev.isCurrent = False
        if not path:
            getPath()
            path = path[::-1]
            for row in gridCells:
                for cell in row:
                    cell.isOn = False
        else:
            if pathInd < pathLen[0]:
                path[pathInd].isOn = True
                path[pathInd].isPath = True
                pathInd += 1
            
    for row in gridCells:
        for cell in row:
            cell.draw()
    pygame.display.update()