'''
press V to display velocity vectors

'''

import pygame
from random import randint
from math import sqrt, pow, sin, cos, pi

vec = pygame.math.Vector2
FPS = 60
RAD = pi / 180.0
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FIND_DISTANCE = 100

# Ants
num_of_ants = 3
ants_vel = []
ants_pos = []

VEL = 2
target = []
wand_counter = []

vec_visibility = True
VEC_LENGTH = 50

for _ in range(num_of_ants):
    ants_pos.append(vec(randint(0, WIDTH), randint(0, HEIGHT)))
    ants_vel.append(vec(1, 0))
    target.append(vec(0, 0))
    wand_counter.append(1)

# Food
num_of_food = 10
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


def velocity_vecs():
    for antt in range(num_of_ants):
        pygame.draw.line(SCREEN, 'red', [ants_pos[antt].x, ants_pos[antt].y],
                         [ants_pos[antt].x + ants_vel[antt].x * VEC_LENGTH,
                          ants_pos[antt].y + ants_vel[antt].y * VEC_LENGTH], 2)


def feromon_to_home():
    pass


def feromon_to_food():
    pass


def is_collision(a_pos, b_pos):
    # Calculating the distance between points (Формула расчета дистанции между точками)
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
            if event.key == pygame.K_v:
                vec_visibility = not vec_visibility

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                pass

    # Передвижение муравья
    for ant in range(num_of_ants):  # Задаем угол движения
        ants_pos[ant] += ants_vel[ant] * VEL

        dist = [-1, 100000000000]
        for food in range(num_of_food):

            cur_dist = distance_to(ants_pos[ant], foods_pos[food])
            # distance to food (Определяем дистанцию муравьев о еды)
            if FIND_DISTANCE >= cur_dist and cur_dist < dist[1]:
                dist = [food, cur_dist]
            if food + 1 == num_of_food and dist[0] != -1:  # Go to food if it in detection radius (Идет к еде если она в радиусе обнаружения)
                wand_counter[ant] = 2
                print(dist)
                ants_vel[ant] = direction_to(ants_pos[ant], foods_pos[dist[0]]).normalize()
            else:  # Wandering algorithm (Алгоритм рандомного блуждания)
                if wand_counter[ant] == 1:
                    target[ant] = ants_vel[ant].rotate(randint(-90, 90))
                    ants_vel[ant] = target[ant]
                wand_counter[ant] += 1
                if wand_counter[ant] >= FPS * 8:
                    wand_counter[ant] = 1
            # Check collision of the ants with food(Определяем коллизию муравьев с едой)
            if is_collision(ants_pos[ant], foods_pos[food]):
                foods_pos[food].x = randint(0, WIDTH)
                foods_pos[food].y = randint(0, HEIGHT)

        if ants_pos[ant].x <= 0:  # Барьеры слева и справа
            ants_vel[ant] = ants_vel[ant].reflect(vec(1, 0))
            ants_pos[ant].x = 1
        elif ants_pos[ant].x >= WIDTH:
            ants_vel[ant] = ants_vel[ant].reflect(vec(-1, 0))
            ants_pos[ant].x = WIDTH - 1
        elif ants_pos[ant].y <= 0:
            ants_vel[ant] = ants_vel[ant].reflect(vec(0, -1))
            ants_pos[ant].y = 0 + 1
        elif ants_pos[ant].y >= HEIGHT:
            ants_vel[ant] = ants_vel[ant].reflect(vec(0, 1))
            ants_pos[ant].y = HEIGHT - 1

    if vec_visibility:
        velocity_vecs()
    foods()
    ants()
    # print(wand_counter)
    clock.tick(FPS)
    pygame.display.update()  # Обновляем экран
