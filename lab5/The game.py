import pygame
import random
from pygame.draw import *

'''
создаем экран и некоторые константы, которые нужна для работы главного цикла 
'''
pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("My Game")
done = False
clock = pygame.time.Clock()
name = input()

'''
музыка
'''

pygame.mixer.init()
pygame.mixer.music.load('minimal.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.1)
sound1 = pygame.mixer.Sound('1.wav')
sound2 = pygame.mixer.Sound('2.wav')
sound3 = pygame.mixer.Sound('3.wav')
sound4 = pygame.mixer.Sound('4.wav')
sound5 = pygame.mixer.Sound('5.wav')
sounds = [sound1, sound2, sound3, sound4, sound5]

'''
некоторые константы, которые мне не хочется вспоминать
'''

score = 0
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, GREEN, YELLOW, MAGENTA, CYAN]
number_of_tiks = 30 * 20

'''
возращает функции от кружочка, по еоторым идет его движение
'''


def new_ball():
    t = random.randint(0, 9)
    if t == 1:
        return {
            'x': random.randint(250, 950),
            'y': random.randint(150, 450),
            'r': random.randint(20, 30),
            't': t,
            'Vx': int((random.randint(0, 1)-0.5) * 20),
            'Vy': int((random.randint(0, 1)-0.5) * 20),
            'color': COLORS[random.randint(0, 5)]
        }
    else:
        return {
            'x': random.randint(250, 950),
            'y': random.randint(150, 450),
            'r': random.randint(20, 30),
            't': t,
            'Vx': random.randint(-5, 5),
            'Vy': random.randint(-5, 5),
            'color': COLORS[random.randint(0, 5)]
        }


'''
создает набор кружочков
'''

a = random.randint(10, 15)
pool = [new_ball() for i in range(a)]

'''
заставляет кружочки ещдить и не дает им уйти за пределы некоторой области
'''


def move_ball(unit):
    unit['x'] += unit['Vx']
    unit['y'] += unit['Vy']
    if unit['t'] == 1:
        circle(screen, RED, (unit['x'], unit['y']), 20)
        circle(screen, YELLOW, (unit['x'], unit['y']), 10)
    else:
        circle(screen, unit['color'], (unit['x'], unit['y']), unit['r'])
    if unit['x'] >= 1000 - unit['r'] or unit['x'] <= 200 + unit['r']:
        unit['Vx'] *= (-1)
    if unit['y'] >= 500 - unit['r'] or unit['y'] <= 100 + unit['r']:
        unit['Vy'] *= (-1)


'''
проверяет не тыкнули мы в кружочек
если мы попали, то в зависимости от типа кружка увеличивает наш счет
затем функция перезаписывает старый кружок, т.е рандомит его новые параметры
'''


def click():
    global score
    event_x, event_y = event.pos
    for unit in pool:
        if ((unit['x'] - event_x) ** 2 + (unit['y'] - event_y) ** 2) < unit['r'] ** 2:
            sound = sounds[random.randint(0, 4)]
            sound.play()
            if unit['t'] == 1:
                score += 10
            else:
                score += 1

            t = random.randint(0, 9)

            if t == 1:
                unit['x'] = random.randint(250, 950)
                unit['y'] = random.randint(150, 450)
                unit['r'] = random.randint(20, 30)
                unit['t'] = t
                unit['Vx'] = int((random.randint(0, 1) - 0.5) * 20)
                unit['Vy'] = int((random.randint(0, 1) - 0.5) * 20)
                unit['color'] = COLORS[random.randint(0, 5)]

            else:
                unit['x'] = random.randint(250, 950)
                unit['y'] = random.randint(150, 450)
                unit['r'] = random.randint(20, 30)
                unit['t'] = t
                unit['Vx'] = random.randint(-10, 10)
                unit['Vy'] = random.randint(-10, 10)
                unit['color'] = COLORS[random.randint(0, 5)]


'''
показывает время в левом верхнем углу экрана
'''


def time(q):
    q_sec = int((q / 30) * 10) / 10
    text1 = f1.render(str(q_sec) + ' sec', 1, (255, 255, 255))
    screen.blit(text1, (0, 10))


'''
создаем кружочки и таблицу счета
'''

for unit in pool:
    new_ball()
f1 = pygame.font.Font(None, 36)
text1 = f1.render('your score ' + str(score), 1, (255, 255, 255))
screen.blit(text1, (510, 10))

'''
создаем главный цикл 
'''

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click()
    '''
    проверяем не закончилось ли время, если оно не закончилось создаем все элементы и проверяем нажатие
    если закончилось, что запрашиваем имя игрока и добавляем его счет в текстовый файлик
    '''
    if number_of_tiks > 0:
        for unit in pool:
            move_ball(unit)

        pygame.display.update()
        clock.tick(30)
        screen.fill(BLACK)
        rect(screen, (59, 68, 75,), (200, 100, 800, 400))
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render('your score ' + str(score), 1, (255, 255, 255))
        screen.blit(text1, (510, 10))
        number_of_tiks -= 1
        time(number_of_tiks)
    else:
        for unit in pool:
            unit['r'] = 0
        pygame.display.update()
        rect(screen, (0, 0, 0), (0, 0, 1200, 600))
        text1 = f1.render('your final score ' + str(score), 1, (255, 255, 255))
        screen.blit(text1, (510, 300))
        number_of_tiks -= 1
    if number_of_tiks == -1:
        screen.blit(text1, (510, 300))
        with open('players.txt', 'a') as f:
            print(name + ':' + str(score), file=f)
    if number_of_tiks < -1:
        pygame.display.update()
        rect(screen, (0, 0, 0), (0, 0, 1200, 600))
        text1 = f1.render('your final score ' + str(score), 1, (255, 255, 255))
        screen.blit(text1, (510, 300))
        number_of_tiks -= 1
pygame.quit()
