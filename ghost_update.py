import pygame
from pygame.draw import *
import random

pygame.init()

FPS = 30

#background
screen = pygame.display.set_mode((500, 700))
rect(screen, (102, 102, 102), (0, 0, 500, 300))
circle(screen, (255, 255, 255), (450, 50), 50)


def house(x,y):

    # house
    rect(screen, (40, 34, 11), (x, y, 100, 200))

    # windowsdown
    rect(screen, (43, 17, 0), ((x+10), (y+160), 20, 30))
    rect(screen, (43, 17, 0), ((x+40), (y+160), 20, 30))
    rect(screen, (212, 170, 0), ((x+70), (y+160), 20, 30))

    # windowstop
    rect(screen, (72, 62, 55), ((x+10), y, 10, 110))
    rect(screen, (72, 62, 55), ((x+30), y, 10, 110))
    rect(screen, (72, 62, 55), ((x+60), y, 10, 110))
    rect(screen, (72, 62, 55), ((x+80), y, 10, 110))

    # balcon
    rect(screen, (26, 26, 26), ((x-10), (y+110), 120, 15))
    rect(screen, (26, 26, 26), ((x-5), (y+80), 110, 10))

    x1 = x - 5
    y1 = y + 80
    for i in range(9):
        rect(screen, (26, 26, 26), (x1, y1, 5, 40))
        x1 += 13

    #roof
    polygon(screen, (0, 0, 0), [((x - 10), y), (x, (y - 20)), ((x + 100), (y - 20)), ((x + 110), y)])
    rect(screen, (26, 26, 26), ((x+5), (y-40), 10, 20))
    rect(screen, (26, 26, 26), ((x+35), (y-50), 15, 30))
    rect(screen, (26, 26, 26), ((x+60), (y-40), 10, 20))
    rect(screen, (26, 26, 26), ((x+90), (y-30), 5, 10))

def cloud1(x,y,z,m):
    ellipse(screen, (26, 26, 26), (x, y, z, m))

def cloud2(x,y,z,m):
    ellipse(screen, (51,55,51), (x, y, z, m))

def cloud3(x,y,z,m):
    ellipse(screen, (77, 77, 77), (x, y, z, m))




def ghost(x, y, t, m):
    circle(screen, (0, 0, 0), (x, y), t + 1)
    polygon(screen, (0, 0, 0),
            [(x - t - 1, y), ((x - 4 * t), (y + 5 * t + 1)), ((x - 3 * t), (y + 4 * t + 1)), ((x - 2 * t),
                                                                                              (y + 5 * t + 1)),
             (((x - t), (y + 4 * t + 1))), ((x, (y + 5 * t + 1))), ((x + t), (y + 4 * t + 1)), ((x + 2 * t),
                                                                                                (y + 5 * t + 1)),
             ((x + 3 * t), (y + 4 * t + 1)), ((x + 4 * t), (y + 5 * t + 1)), ((x + t + 1), y)])

    circle(screen, (179, 179, 179), (x, y), t)
    polygon(screen, (179, 179, 179),
                [(x - t, y), ((x - 4 * t), (y + 5 * t)), ((x - 3 * t), (y + 4 * t)), ((x - 2 * t), (y + 5 * t)),
                 (((x - t), (y + 4 * t))), ((x, (y + 5 * t))), ((x + t), (y + 4 * t)), ((x + 2 * t), (y + 5 * t)),
                 ((x + 3 * t), (y + 4 * t)), ((x + 4 * t), (y + 5 * t)), ((x + t), y)])
    if m == 1:
        circle(screen, (127, 194, 210, 255), ((x + 10), (y - 7),), 5)
        circle(screen, (127, 194, 210, 255), ((x - 3), (y - 7),), 5)
        circle(screen, (0, 0, 0, 255), ((x - 3), (y - 7)), 2)
        circle(screen, (0, 0, 0, 255), ((x + 10), (y - 7)), 2)

    if m == 0:
        circle(screen, (127, 194, 210, 255), ((x + 3), (y - 7),), 5)
        circle(screen, (127, 194, 210, 255), ((x - 10), (y - 7),), 5)
        circle(screen, (0, 0, 0, 255), ((x - 10), (y - 7)), 2)
        circle(screen, (0, 0, 0, 255), ((x + 3), (y - 7)), 2)

cloud1(30, 100, 200, 30)
cloud2(70, 200, 400, 40)
cloud3(120, 150, 200, 20)
house(50, 300)
house(200, 200)
house(370, 150)
ghost(50, 550, 10, 1)
ghost(100, 600, 15, 1)
ghost(400, 600, 12, 0)
ghost(450, 500, 15, 0)
ghost(300, 550, 20, 0)
ghost(390, 400, 15, 0)
cloud2(40, 0, 400, 40)
cloud1(400, 40, 200, 50)




pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
