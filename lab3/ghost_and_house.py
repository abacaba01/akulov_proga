import pygame
from pygame.draw import *

pygame.init()

FPS = 30

#background
screen = pygame.display.set_mode((500, 700))
rect(screen, (102, 102, 102), (0, 0, 500, 310))
ellipse(screen, (26, 26, 26), (200, 140, 300, 50))

#house
rect(screen, (40, 34, 11), (30, 150, 250, 380))

#windowsdown
rect(screen, (43, 17, 0), (55, 400, 50, 70))
rect(screen, (43, 17, 0), (130, 400, 50, 70))
rect(screen, (212, 170, 0), (205, 400, 50, 70))

#windowstop
rect(screen, (72, 62, 55), (60, 150, 25, 150))
rect(screen, (72, 62, 55), (115, 150, 25, 150))
rect(screen, (72, 62, 55), (170, 150, 25, 150))
rect(screen, (72, 62, 55), (225, 150, 25, 150))

#balcon
rect(screen, (26, 26, 26), (0, 310, 310, 50))
rect(screen, (26, 26, 26), (15, 260, 280, 15))

x1 = 10
y1 = 275
for i in range(7):
    rect(screen, (26, 26, 26), (x1, y1, 10, 35))
    x1 += 47

#top
polygon(screen, (0, 0, 0), [(0, 150), (30, 100), (280, 100), (310, 150)])
rect(screen, (26, 26, 26), (80, 50, 20, 60))
rect(screen, (26, 26, 26), (200, 50, 20, 80))

#moon
circle(screen, (255, 255, 255), (450, 50), 50)
ellipse(screen, (51, 51, 51), (30, 40, 400, 50))
ellipse(screen, (77, 77, 77), (250, 20, 250, 40))
ellipse(screen, (77, 77, 77), (330, 80, 400, 30))

#ghost
circle(screen, (179, 179, 179), (400, 530,), 20)
polygon(screen, (179, 179, 179), [(385, 540), (350, 610), (380, 580), (400, 615), (410, 580), (420, 605), (430, 580),
                                  (460, 615), (420, 530)])
circle(screen, (127, 194, 210), (405, 524,), 5)
circle(screen, (127, 194, 210), (395, 524,), 5)
circle(screen, (0, 0, 0), (405, 524,), 2)
circle(screen, (0, 0, 0), (395, 524,), 2)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
