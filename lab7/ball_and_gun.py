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
        self.vel[1] += int(1 * t_step)
        for i in range(2):
            self.coord[i] += int(self.vel[i] * t_step)
        self.check_walls()

    def check_walls(self):
        n = [[1, 0], [0, 1]]
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                self.flip_vel(n[i], 0.8, 0.9)
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                self.flip_vel(n[i], 0.8, 0.9)

    def flip_vel(self, axis, coef_perp=1., coef_par=1.):
        vel = np.array(self.vel)
        n = np.array(axis)
        n = n / np.linalg.norm(n)
        vel_perp = vel.dot(n) * n
        vel_par = vel - vel_perp
        ans = -vel_perp * coef_perp + vel_par * coef_par
        self.vel = ans.astype(np.int).tolist()





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
    def __init__(self, x=None, y=None, rad=None, color=None):
        if color == None:
            self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        if x == None:
            self.x = randint(100, SCREEN_SIZE[0] - 100)
        if y == None:
            self.y = randint(100, SCREEN_SIZE[1] - 100)
        if rad == None:
            self.rad = randint(20, 40)

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.rad)

    def collide(self, ball):
        dist = (self.x - ball.coord[0]) ** 2 + (self.y - ball.coord[1]) ** 2
        mindist = (self.rad + ball.rad) ** 2
        if dist < mindist:
           return 1

class Manager():
    def __init__(self):
        self.gun = Gun()
        self.balls = []
        self.target = []
        self.new_aim()

    def new_aim(self):
        for i in range(3):
            self.target.append(Target())

    def process(self, events, screen):
        done = self.handle_events(events)
        self.draw(screen)
        self.gun.draw(screen)
        self.move()
        self.gun.preparation()
        for ball in self.balls:
            for target in self.target:
                Target.collide(target, ball)

        return done


    def draw(self, screen):
        screen.fill(BLACK)
        for ball in self.balls:
            ball.draw(screen)
        for target in self.target:
            target.draw(screen)

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

score = 0

while not done:
    clock.tick(30)

    done = mgr.process(pg.event.get(), screen)
    pg.display.flip()

pg.quit()