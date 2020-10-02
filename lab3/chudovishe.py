import pygame
from pygame.draw import *


FPS = 30
screen = pygame.display.set_mode((400, 400))
rect(screen, (255, 255, 255), (0, 0, 400, 400))

#голова
circle(screen, (0, 51, 0), (200, 200), 100)

#глаза
circle(screen, (204, 0, 0), (165, 165), 25)
circle(screen, (204, 0, 0), (235, 165), 20)
circle(screen, (0, 0, 0), (165, 165), 10)
circle(screen, (0, 0, 0), (235, 165), 10)

#брови
polygon(screen, (0, 0, 0), [(100, 100), (100, 120), (200, 170), (200, 150)])
polygon(screen, (0, 0, 0), [(200, 170), (200, 150), (300, 100), (300, 120)])

#рот
rect(screen, (0, 0, 0), (150, 240, 100, 20))

#зубы
polygon(screen, (255, 255, 153), [(153, 240), (160, 220), (170, 240), (180, 220), (190, 240), (200, 220), (210, 240), (220, 220), (230, 240), (240, 220), (247, 240)])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()