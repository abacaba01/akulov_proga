import pygame as pg
import numpy as np
from random import randint

SCREEN_SIZE = (800, 600)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pg.init()

pg.mixer.init()
pg.mixer.music.load('kleo.mp3')
pg.mixer.music.play()



class Ball():
    def __init__(self, coord, vel, rad=10, color=None):
        if color is None:
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

    def check_alive(self):
        v = self.vel[1] ** 2 + self.vel[0] ** 2
        if v < 4 and self.coord[1] > SCREEN_SIZE[1] - 2 * self.rad:
            return 0


class Score():
    def __init__(self, numb_used=0, numb_dest=0, numb_used_final=0, time=2 * 1800, time_okr=0):
        self.numb_used = numb_used
        self.numb_dest = numb_dest
        self.time = time
        self.numb_used_final = numb_used_final
        self.time_okr = time_okr

    def score(self):
        f1 = pg.font.Font(None, 36)
        text1 = f1.render('очков' + ' : ' + str(self.numb_dest), 1, (255, 255, 255))
        screen.blit(text1, (10, 10))
        text1 = f1.render('попыток' + ' : ' + str(self.numb_used), 1, (255, 255, 255))
        screen.blit(text1, (10, 30))
        text1 = f1.render('времени осталось' + ' : ' + str(self.time_okr) + 'сек', 1, (255, 255, 255))
        screen.blit(text1, (10, 570))

    def final_score(self):
        f1 = pg.font.Font(None, 36)
        text1 = f1.render('очков' + ' : ' + str(self.numb_dest), 1, (255, 255, 255))
        screen.blit(text1, (330, 280))
        text1 = f1.render('попыток' + ' : ' + str(self.numb_used_final), 1, (255, 255, 255))
        screen.blit(text1, (330, 320))

    def number_time(self):
        self.time -= 1
        self.time_okr = int(self.time / 3) / 10


class Gun():
    def __init__(self, coord=[30, SCREEN_SIZE[1] // 2], min_pow=10, max_pow=30):
        self.coord = coord
        self.angle = 0
        self.min_pow = min_pow
        self.max_pow = max_pow
        self.power = min_pow
        self.active = False

    def draw(self, screen):
        end_pos = [self.coord[0] + self.power * np.cos(self.angle), self.coord[1] + self.power * np.sin(self.angle)]
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
        if rad is None:
            self.rad = randint(20, 40)
        if color is None:
            self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        if x is None:
            self.x = randint(100, SCREEN_SIZE[0] - 100)
        if y is None:
            self.y = randint(100, SCREEN_SIZE[1] - 100)

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.rad)

    def check_collide(self, ball):
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
        self.score = Score()

    def new_aim(self):
        for i in range(4):
            self.target.append(Target())

    def process(self, events, screen):
        done = self.handle_events(events)
        self.draw(screen)

        self.move()
        self.gun.preparation()
        self.collide()
        self.rubbish()

        return done

    def draw(self, screen):
        if self.score.time > 0:
            screen.fill(BLACK)
            for ball in self.balls:
                ball.draw(screen)
            for target in self.target:
                target.draw(screen)
            self.score.number_time()
            self.score.score()
            self.gun.draw(screen)
        else:
            self.score.numb_used_final = self.score.numb_used
            self.balls = []
            self.target = []
            screen.fill(BLACK)
            self.score.final_score()

    def collide(self):
        for ball in self.balls:
            for i in range(0, len(self.target)):
                if Target.check_collide(self.target[i], ball) == 1:
                    self.score.numb_dest += 1

                    self.target.pop(i)
                    return
        if len(self.target) == 0 and len(self.balls) == 0:
            Manager.new_aim(self)

    def rubbish(self):
        for i in range(len(self.balls)):
            if Ball.check_alive(self.balls[i]) == 0:
                self.balls.pop(i)
                return

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
                    if self.score.time > 0:
                        self.balls.append(self.gun.strike())
                        self.score.numb_used += 1
                    else:
                        pass
        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)

        return done


screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("The gun of Abacaba")
clock = pg.time.Clock()

mgr = Manager()

done = False

score = 0

while not done:
    clock.tick(30)

    done = mgr.process(pg.event.get(), screen)
    pg.display.flip()

pg.quit()
