import math

import pygame
from random import randint
from math import sqrt, pow, sin, cos, pi

vec = pygame.math.Vector2

RAD = pi / 180.0
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FIND_DISTANCE = 100

# Ants
num_of_ants = 3
ants_vel = []
ants_pos = []

VEL = 4
target = []
wand_counter = []
for _ in range(num_of_ants):
    ants_pos.append(vec(randint(0, WIDTH), randint(0, HEIGHT)))
    ants_vel.append(vec(1, 0))
    target.append(vec(0, 0))
    wand_counter.append(1)

# Food
num_of_food = 1
foods_pos = []
for _ in range(num_of_food):
    foods_pos.append(vec(randint(0, WIDTH), randint(0, HEIGHT)))
    # food_x.append(WIDTH / 2 - 50)
    # food_y.append(HEIGHT / 2 +50)
################
# -Functions-##
################

# FPS
clock = pygame.time.Clock()


def ants():
    for antt in range(num_of_ants):
        pygame.draw.circle(SCREEN, 'white', [ants_pos[antt].x, ants_pos[antt].y], 8)


def foods():
    for fd in range(num_of_food):
        pygame.draw.circle(SCREEN, 'green', [foods_pos[fd].x, foods_pos[fd].y], 5)


def feromon_to_home():
    pass


def feromon_to_food():
    pass


def is_collision(a_pos, b_pos):
    # Формула расчета дистанции между точками
    if distance_to(a_pos, b_pos) < 8:
        return True
    else:
        return False


def distance_to(a_pos, b_pos):
    return (a_pos - b_pos).length()


def direction_to(a_pos, b_pos):
    return (b_pos - a_pos).normalize()


# Game Loop

pygame.init()
running = True

while running:
    SCREEN.fill('black')  # Устанавливаем цвет заливки экрана

    for event in pygame.event.get():  # Создаем цикл, перебирающий все происходящие эвенты
        # Если нажимается крестик на окне => игра закрывается
        if event.type == pygame.QUIT:
            running = False

        # Обработка нажатий клавиш
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT:
                pass
            if event.key == pygame.K_RIGHT:
                pass
            if event.key == pygame.K_SPACE:
                pass

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                pass

    # Передвижение муравья
    for ant in range(num_of_ants):  # Задаем угол движения
        ants_pos[ant] += ants_vel[ant] * VEL

        if ants_pos[ant].x <= 0:  # Барьеры слева и справа
            ants_vel[ant] = ants_vel[ant].reflect(vec(1,0))
            ants_pos[ant].x = 0
        elif ants_pos[ant].x >= WIDTH:
            ants_vel[ant] = ants_vel[ant].reflect(vec(-1,0))
            ants_pos[ant].x = WIDTH
        elif ants_pos[ant].y <= 0:
            ants_vel[ant] = ants_vel[ant].reflect(vec(0,-1))
            ants_pos[ant].y = 0
        elif ants_pos[ant].y >= HEIGHT:
            ants_vel[ant] = ants_vel[ant].reflect(vec(0,1))
            ants_pos[ant].y = HEIGHT

        for food in range(num_of_food):
            dist = distance_to(ants_pos[ant], foods_pos[food], )  # Определяем дистанцию муравьев о еды
            if dist <= FIND_DISTANCE:  # Идет к еде если она в радиусе обнаружения
                ants_vel[ant] = direction_to(ants_pos[ant], foods_pos[food]) * VEL
            else:  # Алгоритм рандомного блуждания
                if wand_counter[ant] == 1:
                    target[ant] = ants_vel[ant].rotate(randint(-90, 90))
                ants_vel[ant] = target[ant]
                wand_counter[ant] += 1
                if wand_counter[ant] >= 60 * 2:
                    wand_counter[ant] = 1
            print(ants_pos[ant])
            # Определяем коллизию муравьев с едой
            if is_collision(ants_pos[ant], foods_pos[food]):
                foods_pos[food].x = randint(0, WIDTH)
                foods_pos[food].y = randint(0, HEIGHT)

    foods()
    ants()
    clock.tick(60)
    pygame.display.update()  # Обновляем экран
