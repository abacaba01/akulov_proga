import pygame as pg
import numpy as np
from random import randint

'''
набор констант
'''
SCREEN_SIZE = (800, 600)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


pg.init()
'''
музыкальное сопровождение
'''

pg.mixer.init()
pg.mixer.music.load('kleo.mp3')
pg.mixer.music.play()


class Walls():
    '''
    отвечает за стены, об которые, ударяясь шар меняет траекторию движения
    за стенки очки не начисляются
    '''
    def __init__(self, coord=None, length=None, width=None, color=None, a=None):
        if coord is None:
            coord = [randint(150, 650), randint(100, 500)]
        self.coord = coord
        if length is None:
            length = randint(100, 220)
        self.length = length
        if width is None:
            width = 40
        self.width = width
        if color is None:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = color
        if a == 1:
            self.length, self.width = self.width, self.length

    def draw(self, screen):
        '''
        рисует сами препятствия
        '''
        pg.draw.rect(screen, self.color, (self.coord[0], self.coord[1], self.length, self.width))

    def check_walls(self, ball):
        '''
        проверяет для выбранного шара и стенки не находятся ли они достаточно близко, чтобы было соприкосновение
        '''
        if self.coord[0] - 10 < ball.coord[0] < self.coord[0] + self.length + 10:
            if self.coord[1] - 10 < ball.coord[1] < self.coord[1] + self.width + 10:
                return 0


class Ball():
    '''
    класс шаров, отвечает за вылетающие шары
    '''

    def __init__(self, coord, vel, rad=10, color=None):
        if color is None:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color = color
        self.coord = coord
        self.vel = vel
        self.rad = rad

    def draw(self, screen):
        '''
        рисует шарик
        '''

        pg.draw.circle(screen, self.color, self.coord, self.rad)

    def move(self, t_step=1.):
        '''
        двигает шар и запускает функцию, которая проверяет не ударились ли он об край экрана
        '''
        self.vel[1] += int(1 * t_step)
        for i in range(2):
            self.coord[i] += int(self.vel[i] * t_step)
        self.check_walls()

    def flip(self, wall):
        '''
        функция, которая отвечает за то, чтобы изменить скорость шара, если они ударился об препятствие
        '''
        if wall.coord[1] < self.coord[1] < wall.coord[1] + wall.width and (self.coord[0] < wall.coord[0] + 15
                                                                           or self.coord[0] > wall.coord[
                                                                               0] + wall.length - 15):
            self.vel[0] *= -1
            if wall.coord[0] + 20 > self.coord[0]:
                self.coord[0] = wall.coord[0] - 10
            else:
                self.coord[0] = wall.coord[0] + 10 + wall.length
        if wall.coord[0] < self.coord[0] < wall.coord[0] + wall.length and (self.coord[1] < wall.coord[1] + 15
                                                                            or self.coord[1] > wall.coord[
                                                                                1] + wall.width - 15):
            self.vel[1] *= -1
            if wall.coord[1] + 20 > self.coord[1]:
                self.coord[1] = wall.coord[1] - 10
            else:
                self.coord[1] = wall.coord[1] + 10 + wall.width

    def check_walls(self):
        '''
        функция, проверяет не ударился ли шара обстенку, в случае удара вызывает flip_vel
        '''
        n = [[1, 0], [0, 1]]
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                self.flip_vel(n[i], 0.8, 0.9)
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                self.flip_vel(n[i], 0.8, 0.9)

    def flip_vel(self, axis, coef_perp=1., coef_par=1.):
        '''
        вызываемая в случае удара о край экрана функция, которая меняет направление скорости шара в этом случае
        '''
        vel = np.array(self.vel)
        n = np.array(axis)
        n = n / np.linalg.norm(n)
        vel_perp = vel.dot(n) * n
        vel_par = vel - vel_perp
        ans = -vel_perp * coef_perp + vel_par * coef_par
        self.vel = ans.astype(np.int).tolist()

    def check_alive(self):
        '''
        проверяет шар на его движение, если его коллебания малы, то удаляет его с экрана
        '''
        v = self.vel[1] ** 2 + self.vel[0] ** 2
        if v < 4 and self.coord[1] > SCREEN_SIZE[1] - 2 * self.rad:
            return 0


class Score():
    '''
    отвечает за счет в игре и ее длительность
    '''
    def __init__(self, numb_used=0, numb_dest=0, numb_used_final=0, time=2 * 1800, time_okr=0):
        self.numb_used = numb_used
        self.numb_dest = numb_dest
        self.time = time
        self.numb_used_final = numb_used_final
        self.time_okr = time_okr

    def score(self):
        '''
        функция счета очков, оставшегося времени и потраченных шаров
        '''
        f1 = pg.font.Font(None, 36)
        text1 = f1.render('очков' + ' : ' + str(self.numb_dest), 1, (255, 255, 255))
        screen.blit(text1, (10, 10))
        text1 = f1.render('шариков ушло' + ' : ' + str(self.numb_used), 1, (255, 255, 255))
        screen.blit(text1, (10, 30))
        text1 = f1.render('времени осталось' + ' : ' + str(self.time_okr) + 'сек', 1, (255, 255, 255))
        screen.blit(text1, (10, 570))

    def final_score(self):
        '''
        финальная заставка, которая будет говорить о количестве потраченных шаров за все время и набранных очках
        '''
        f1 = pg.font.Font(None, 36)
        text1 = f1.render('финальный счет' + ' : ' + str(self.numb_dest), 1, (255, 255, 255))
        screen.blit(text1, (330, 280))
        text1 = f1.render('шариков ушло' + ' : ' + str(self.numb_used_final), 1, (255, 255, 255))
        screen.blit(text1, (330, 320))

    def number_time(self):
        '''
        таймер, необходимый чтобы понять, когда игра закончилась
        '''
        self.time -= 1
        self.time_okr = int(self.time / 3) / 10


class Gun():
    '''
    пушка, отвечает за создание шаров, выстрел происзодит в направлении курсора,
    сила выстрела зависит от длительности зажима
    '''
    def __init__(self, coord=[30, SCREEN_SIZE[1] // 2], min_pow=10, max_pow=28):
        self.coord = coord
        self.angle = 0
        self.min_pow = min_pow
        self.max_pow = max_pow
        self.power = min_pow
        self.active = False

    def draw(self, screen):
        '''
        рисует саму пушку
        '''
        end_pos = [self.coord[0] + self.power * np.cos(self.angle), self.coord[1] + self.power * np.sin(self.angle)]
        pg.draw.line(screen, WHITE, self.coord, end_pos, 10)

    def strike(self):
        '''
        выстрел, записывает кординаты и скорости выпущенного шарика
        '''
        vel = [int(self.power * np.cos(self.angle)), int(self.power * np.sin(self.angle))]
        self.active = False
        self.power = self.min_pow
        return Ball(list(self.coord), vel)

    def preparation(self):
        '''
        расчитывает силу с которой будет выстрел
        '''
        if self.active and self.power < self.max_pow:
            self.power += 1

    def set_angle(self, mouse_pos):
        '''
        определяет позицию курсора на экране
        '''
        self.angle = np.arctan2(mouse_pos[1] - self.coord[1],
                                mouse_pos[0] - self.coord[0])


class Target():
    '''
    функция, создаюзая цели, в которые нужно попасть, чтобы  набрать очки
    '''
    def __init__(self, x=None, y=None, rad=None, color=None):
        if rad is None:
            self.rad = randint(20, 40)
        if color is None:
            self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        if x is None:
            self.x = randint(100, SCREEN_SIZE[0] - 100)
        if y is None:
            self.y = randint(150, SCREEN_SIZE[1] - 100)

    def draw(self, screen):
        '''
        рисует цель
        '''
        pg.draw.circle(screen, self.color, (self.x, self.y), self.rad)

    def check_collide(self, ball):
        '''
        проверяет выбранный шарик и выбранную цель не слишком ли близки они
        '''
        dist = (self.x - ball.coord[0]) ** 2 + (self.y - ball.coord[1]) ** 2
        mindist = (self.rad + ball.rad) ** 2
        if dist < mindist:
            return 1


class Manager():
    '''
    отвечает за работу программы
    '''
    def __init__(self):
        self.gun = Gun()
        self.balls = []
        self.target = []
        self.new_aim()
        self.score = Score()
        self.walls = []
        self.new_walls()

    def new_aim(self):
        '''
        создает набор новых целей, если во все предыдущие попали
        '''
        for i in range(4):
            self.target.append(Target())

    def new_walls(self):
        '''
        создает 4 препятсвия так, чтобы в каждой четверти было по 1
        '''
        self.walls.append((Walls(coord=(randint(50, 400), randint(50, 300)), a=randint(1, 2))))
        self.walls.append((Walls(coord=(randint(50, 400), randint(300, 550)), a=randint(1, 2))))
        self.walls.append((Walls(coord=(randint(400, 750), randint(50, 400)), a=randint(1, 2))))
        self.walls.append((Walls(coord=(randint(400, 750), randint(300, 550)), a=randint(1, 2))))

    def process(self, events, screen):
        '''
        процесс игры, создает события, необходимые на каждом ходу
        '''
        done = self.handle_events(events)
        self.draw(screen)
        self.move()
        self.gun.preparation()
        self.collide()
        self.rubbish()
        for i in range(len(self.balls)):
            for j in range(len(self.walls)):
                if Walls.check_walls(self.walls[j], self.balls[i]) == 0:
                    Ball.flip(self.balls[i], self.walls[j])

        return done

    def draw(self, screen):
        '''
        в зависимости от времени выводит изображения на экран
        если еще осталось время то рисует все необходимое, в противном случае - заставка
        '''
        if self.score.time > 0:
            screen.fill(BLACK)
            for ball in self.balls:
                ball.draw(screen)
            for target in self.target:
                target.draw(screen)
            self.score.number_time()
            self.score.score()
            self.gun.draw(screen)
            for wall in self.walls:
                wall.draw(screen)
        else:
            self.score.numb_used_final = self.score.numb_used
            self.balls = []
            self.target = []
            screen.fill(BLACK)
            self.score.final_score()

    def collide(self):
        '''
        проходит циклом по всем шарам и всем мишеням, определяя не столкнулись ли они
        в случае столкновения удаляет мишень и увеличивает количество очков на 1
        при исчезновении всех мишеней и шаров создает новые мишени
        '''
        for ball in self.balls:
            for i in range(0, len(self.target)):
                if Target.check_collide(self.target[i], ball) == 1:
                    self.score.numb_dest += 1

                    self.target.pop(i)
                    return
        if len(self.target) == 0 and len(self.balls) == 0:
            Manager.new_aim(self)

    def rubbish(self):
        '''
        убирает шары, колебания которых малы проходя по циклу и применяя к ним функцию check_alive
        '''
        for i in range(len(self.balls)):
            if Ball.check_alive(self.balls[i]) == 0:
                self.balls.pop(i)
                return

    def move(self):
        '''
        проходя по циклу сдвигает все шары
        '''
        for ball in self.balls:
            ball.move()

    def handle_events(self, events):
        '''
        функция отвечающая за нажатия кнопок
        стрелочки заставлят пушку смещаться вверх и вниз
        зажатие - усиливает вылетающий снаряд
        в случае выстрела увеличивает количество вылетевших шаров на 1
        '''
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


'''
называем игру и создаем экран
'''

screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("The gun of Abacaba")
clock = pg.time.Clock()

mgr = Manager()

done = False

score = 0
'''
основное тело
'''
while not done:
    clock.tick(30)

    done = mgr.process(pg.event.get(), screen)
    pg.display.flip()

pg.quit()
