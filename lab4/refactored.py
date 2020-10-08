import pygame
import numpy as np
import random

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)


def screen_update(x, y):
    """
    нужна чтобы обновлять экран каждый раз
    x - кордината по х, нужна для обновления цвета
    y - указатель на время суток в зависимости от остатка при делении на 2
     """
    if x < 0:
        time_of_day = (64, 64, 128 + 64)
    else:
        if x > 800:
            time_of_day = (64, 64, 128 + 64)
        else:
            t = ((x / 800) * 128) // 1

            if (y % 2) == 0:
                if x <= 400:
                    time_of_day = (64 + t, 64 + t, 127 + 62 + t)
                else:
                    time_of_day = (128 + 64 - t, 128 + 64 - t, 254 + 62 - t)
            else:
                if x <= 400:
                    time_of_day = (64 - t, 64 - t, 128 + 63 - t)
                else:
                    time_of_day = (t - 64, t - 64, 64 + t)

    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.draw.rect(screen, time_of_day, (0, 0, 800, 300))
    pygame.draw.rect(screen, (0, 96, 0), (0, 300, 800, 600))


def blit_with_scale(x, y, scale, surface):
    """
        накладывает поверхность на экран.
        просто не трогай она нужна для работы других функций.
    """
    w, h = surface.get_size()
    surface = pygame.transform.scale(surface,
                                     (int(w * scale), int(h * scale)))
    screen.blit(surface, (x - w * scale // 2,
                          y - h * scale // 2))


def draw_home(x, y, scale):
    """
        Нарисовать дом
        x, y {int} - координаты центра домика
        scale {float} - масштабирование домика. линейные размеры
                        умножаются на эту величину
        по умолчанию размеры домика 200 х 280
    """
    surface = pygame.Surface((200, 280), pygame.SRCALPHA)
    home_rect = pygame.Rect(0, 130, 200, 150)
    pygame.draw.rect(surface, pygame.Color("#a06117"), home_rect)
    pygame.draw.polygon(surface, pygame.Color("#f93838"),
                        [(0, 130), (100, 0), (200, 130)])
    window_rect = pygame.Rect((0, 0), (60, 40))
    window_rect.center = home_rect.center
    pygame.draw.rect(surface, pygame.Color("#3790d5"), window_rect)

    blit_with_scale(x, y, scale, surface)


def draw_tree(x, y, scale):
    """
        Нарисовать дерево
        x, y {int} - координаты центра дерева
        scale {float} - масштабирование дерева. линейные размеры
                        умножаются на эту величину
        по умолчанию размеры дерева 150 х 230
    """
    surface = pygame.Surface((150, 230), pygame.SRCALPHA)

    pygame.draw.rect(surface, pygame.Color("black"), (70, 70, 20, 500))
    for coords in [(610, 205), (560, 190),
                   (600, 160), (645, 190),
                   (570, 230), (640, 230)]:
        coords = (coords[0] - 525, coords[1] - 130)
        pygame.draw.circle(surface, pygame.Color("#256927"), coords, 30)
        pygame.draw.circle(surface, pygame.Color("black"), coords, 30, 1)

    blit_with_scale(x, y, scale, surface)


def draw_clouds(x, y, scale):
    """
        Нарисовать облака
        x, y {int} - координаты центра.
        scale {float} - масштабирование. линейные размеры
                        умножаются на эту величину

    """
    surface = pygame.Surface((210, 140), pygame.SRCALPHA)
    for coords in [(350, 80), (480, 80), (410, 70), (450, 120), (390, 130)]:
        coords = (coords[0] - 310, coords[1] - 30)  # немотивированное действие
        pygame.draw.circle(surface, pygame.Color("white"), coords, 40)
        pygame.draw.circle(surface, pygame.Color("#484646"), coords, 40, 1)

    blit_with_scale(x, y, scale, surface)


def draw_sun(x, y, radius, z):
    """
        Нарисовать солнце
        x, y {int} - координаты центра.
        radius {int} - радиус
        остаток от деления числа z на 2 определяет солнце либо луну
    """

    if (z % 2) == 0:
        a = np.arange(0, 360, 5)
        p1_x = x + radius * np.cos(np.radians(a))
        p1_y = y + radius * np.sin(np.radians(a))

        p2_x = x + (radius + radius / 10) * np.cos(np.radians(a))
        p2_y = y + (radius + radius / 10) * np.sin(np.radians(a))

        coords = [(p1_x[i], p1_y[i]) if i % 2 == 0 else (p2_x[i], p2_y[i])
                for i in range(360 // 5)]
        pygame.draw.polygon(screen, pygame.Color("#f77658"), coords)

    else:
        pygame.draw.circle(screen, (192, 192, 192), (x, y), radius)




"""
   создаем тик и название приложения, 
"""

pygame.display.set_caption("My Game")
done = False
clock = pygame.time.Clock()

'''
создаем машинку
'''

pygame.mixer.music.load('LOLIPOP.mp3')
pygame.mixer.music.play()
sc = pygame.display.set_mode((400, 300))
lambo_surf = pygame.image.load('lambo.png')
lambo_surf.set_colorkey((255, 255, 255))

"""
   набор изначально заданных констант, которые далее изменяются      
"""
a = 1000
y = 0
x_sun = -50
y_sun = 250
x_cloud = np.array([100, 300, 500])
y_cloud = np.array([200, 100, 150])
z_cloud = np.array([0.5, 0.7, 1])
x_cloud_speed = np.array([1, 2, 1])

"""
   основной цикл, в котором происходят все действия  
"""

while done == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen_update(x_sun, y)

    """
       рисуем все объекты      
    """

    draw_sun(x_sun, y_sun, 30, y)

    draw_clouds(x_cloud[2], y_cloud[2], z_cloud[2])
    draw_clouds(x_cloud[1], y_cloud[1], z_cloud[1])
    draw_clouds(x_cloud[0], y_cloud[0], z_cloud[0])

    draw_home(400, 300, 0.75)

    draw_tree(100, 300, 1)
    draw_tree(700, 300, 0.75)
    draw_tree(550, 300, 0.5)
    draw_tree(250, 300, 0.75)

    """
       двигаем все объекты      
    """

    for i in range(3):
        if x_cloud[i] >= 900:
            x_cloud[i] = -100
            y_cloud[i] = random.randint(50, 250)
            z_cloud[i] = random.randint(5, 10) / 10
            x_cloud_speed[i] = random.randint(1, 3)
        x_cloud[i] += x_cloud_speed[i]

    if x_sun >= 950:
        x_sun = -50
        y_sun = 250
        y += 1
    else:
        x_sun += 2
    if x_sun < 400:
        y_sun -= 1
    else:
        y_sun += 1

    lambo_rect = lambo_surf.get_rect(center=(a, 500))
    sc.blit(lambo_surf, lambo_rect)

    a -= 3
    if a < -400:
        a = 1200

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
