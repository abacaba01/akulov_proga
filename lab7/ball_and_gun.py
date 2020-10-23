import pygame as pg
import numpy as np
from random import randint

SCREEN_SIZE = (800, 600)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pg.init()

class Ball():
    def __init__(self, coord, vel, rad=10, color=None):
        if color == None:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = color
        self.coord = coord
        self.vel = vel
        self.rad = rad

    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.coord, self.rad)

    def move(self, t_step=1.):
        for i in range(2):
            self.coord[i] += int(self.vel[i] * t_step)
        self.check_walls()

    def check_walls(self):
        if self.coord[0] < self.rad:
            self.vel[0] *= -1
        if self.coord[0] > 800 - self.rad:
            self.vel[0] *= -1
        if self.coord[1] < self.rad:
            self.vel[1] *= -1
        if self.coord[1] > 600 - self.rad:
            self.vel[1] *= -1


class Table():
    pass

class Gun():
    def __init__(self, coord=[30, SCREEN_SIZE[1] // 2], min_pow=10, max_pow=30):
        self.coord = coord
        self.angle = 0
        self.min_pow = min_pow
        self.max_pow = max_pow
        self.power = min_pow
        self.active = False

    def draw(self, screen):
        end_pos = [self.coord[0] + self.power* np.cos(self.angle), self.coord[1] + self.power * np.sin(self.angle)]
        pg.draw.line(screen, WHITE, self.coord, end_pos, 10)

    def strike(self):
        vel = [int(self.power * np.cos(self.angle)), int(self.power * np.sin(self.angle))]
        self.active = False
        self.power = self.min_pow
        return Ball(list(self.coord), vel)

    def preparation(self):
        if self.active and self.power < self.max_pow:
            self.power += 1

    def set_angle(self, mouse_pos):
        self.angle = np.arctan2(mouse_pos[1] - self.coord[1],
                                mouse_pos[0] - self.coord[0])

class Target():
    pass

class Manager():
    def __init__(self):
        self.gun = Gun()
        self.table = Table()
        self.balls = []

    def process(self, events, screen):
        done = self.handle_events(events)
        self.draw(screen)
        self.gun.draw(screen)
        self.move()
        self.gun.preparation()
        return done

    def draw(self, screen):
        screen.fill(BLACK)
        for ball in self.balls:
            ball.draw(screen)

    def move(self):
        for ball in self.balls:
            ball.move()

    def handle_events(self, events):
        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.gun.coord[1] -= 5
                elif event.key == pg.K_DOWN:
                    self.gun.coord[1] += 5
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.gun.active = True
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.balls.append(self.gun.strike())

        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)

        return done

screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("The gun of Zepopa")
clock = pg.time.Clock()

mgr = Manager()

done = False

while not done:
    clock.tick(30)

    done = mgr.process(pg.event.get(), screen)

    pg.display.flip()
