import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import numpy as np


# name = input("Please enter your name: ")
name = "st4rboy"
capture = cv.VideoCapture(0)
detector = HandDetector(maxHands=1)

def rescaleFrame(frame, scale):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

offset = 10

WIDTH, HEIGHT = 640, 480

info = np.zeros((100, 200, 3), dtype='uint8')
blank = np.zeros((HEIGHT, WIDTH, 3), dtype='uint8')
blank[:] = (31, 31, 31)
info[:] = (31, 31, 31)

canDraw = False

while True:
    isTrue, frame = capture.read()
    hands, frame = detector.findHands(frame)
    if hands:
        hand = hands[0]
        print(hand['bbox'])
        # width, height = hand['bbox']
        x, y, z = hand['lmList'][8]
        # handImg = frame[y-offset:y+height+offset, x-offset:x+width+offset]
        if canDraw:
            cv.circle(blank, (WIDTH-x, y), 5, (255, 255, 255), thickness=-1)
    cv.putText(frame, f'Hello {name}!', (frame.shape[1]//3, 4*frame.shape[0]//5),
        cv.FONT_HERSHEY_SIMPLEX, 0.8, (200, 231, 0), 2)
    cv.putText(info, f"'d' : Toggle drawing", (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv.putText(info, f"'c' : Clear Screen", (10, 40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    # cv.imshow('Frame', frame)
    cv.imshow('Drawing', blank)
    cv.imshow('Info', info)
    k = cv.waitKey(20)
    if k == -1:
        continue
    if k == 27:
        break
    if k == ord('d'):
        if not canDraw:
            canDraw = True
        else:
            canDraw = False
    if k == ord('c'):
        # blank = np.zeros((HEIGHT, WIDTH, 3), dtype='uint8')
        blank[:] = (31, 31, 31)
capture.release()
cv.destroyAllWindows()

cv.waitKey(0)

# pygame.init()

# WIDTH, HEIGHT = 1200, 600
# WHITE = (255, 255, 255)

# screen = pygame.display.set_mode([WIDTH, HEIGHT])
# pygame.display.set_caption("OpenCV Shape Detector")


# clock = pygame.time.Clock()

# while True:
#     clock.tick(60)
#     screen.fill((0, 0, 0))

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 pygame.quit()
#                 exit()

#     pygame.display.update()
