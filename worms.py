import os
import sys
import pygame
import menu
import random

pygame.init()
screen_rect = (0, 0, 1200, 600)
GRAVITY = 0.5
all_sprites = pygame.sprite.Group()
all_sprites2 = pygame.sprite.Group()
all_sprites3 = pygame.sprite.Group()
tile_width = tile_height = 40
first_flag = True
flag_board2 = False
sprites1 = []
sprites2 = []
flag_move = True
game_started_flag = False
now_player = 1
strelka = '<----'
win = 0
win2 = 0
kletki_x = None
kletki_y = None
pygame.mixer.music.load('sound/background_music.mp3')
pygame.mixer.music.play(-1)
digging_sound = pygame.mixer.Sound('sound/digging.mp3')
win_sound = pygame.mixer.Sound('sound/win.mp3')


def load_image(name, colorkey=None):
    fullname = os.path.join('kartinki', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    return image

class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("particle.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites3)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект: 
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()

def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


signs_images = {'cover': load_image('grass.png'),
                'hit': load_image('hit.png'),
                'dirt': load_image('miss.png')}


def change_matrix(sprite, board, insect, new_value):
    if insect == 1:
        for i in board.kletki:
            if i[0] == sprite.rect.x and i[1] == sprite.rect.y:
                board.board[i[4][0]][i[4][1]] = new_value
    if insect == 2:
        for i in board.kletki:
            if sprite.pos == 1:
                if i[0] == sprite.rect.x and i[1] == sprite.rect.y:
                    board.board[i[4][0]][i[4][1]] = new_value
                    board.board[i[4][0] + 1][i[4][1]] = new_value
            if sprite.pos == 2:
                if i[0] == sprite.rect.x and i[1] == sprite.rect.y:
                    board.board[i[4][0]][i[4][1]] = new_value
                    board.board[i[4][0]][i[4][1] + 1] = new_value
    if insect == 3:
        for i in board.kletki:
            if sprite.pos == 1:
                if i[0] == sprite.rect.x and i[1] == sprite.rect.y:
                    board.board[i[4][0]][i[4][1]] = new_value
                    board.board[i[4][0] + 1][i[4][1]] = new_value
                    board.board[i[4][0] + 2][i[4][1]] = new_value
            if sprite.pos == 2:
                if i[0] == sprite.rect.x and i[1] == sprite.rect.y:
                    board.board[i[4][0]][i[4][1]] = new_value
                    board.board[i[4][0]][i[4][1] + 1] = new_value
                    board.board[i[4][0]][i[4][1] + 2] = new_value
    if insect == 4:
        for i in board.kletki:
            if sprite.pos == 1:
                if i[0] == sprite.rect.x and i[1] == sprite.rect.y:
                    board.board[i[4][0]][i[4][1]] = new_value
                    board.board[i[4][0] + 1][i[4][1]] = new_value
                    board.board[i[4][0] + 2][i[4][1]] = new_value
                    board.board[i[4][0] + 3][i[4][1]] = new_value
            if sprite.pos == 2:
                if i[0] == sprite.rect.x and i[1] == sprite.rect.y:
                    board.board[i[4][0]][i[4][1]] = new_value
                    board.board[i[4][0]][i[4][1] + 1] = new_value
                    board.board[i[4][0]][i[4][1] + 2] = new_value
                    board.board[i[4][0]][i[4][1] + 3] = new_value

def change_player():
    global now_player, strelka
    if now_player == 2:
        now_player = 1
        strelka = '<----'
    else:
        now_player = 2
        strelka = '---->'

def hide():
    global first_flag, flag_board2, board2, matrix1, matrix2, flag_move, game_started_flag
    if first_flag:
        matrix1 = board.board
        for i in all_sprites:
            sprites1.append((i.rect.x, i.rect.y, i.pos))
            i.place = True
            if i.pos == 2:
                i.pos = 1
                i.image = pygame.transform.rotate(
                    i.image,
                    90
                )
                i.rect[2] = i.image.get_size()[0]
                i.rect[3] = i.image.get_size()[1]
            i.rect.x = i.start_xy[0]
            i.rect.y = i.start_xy[1]
        board.board = [[0] * board.width for _ in range(board.height)]
        first_flag = False
    else:
        matrix2 = board.board
        for i in all_sprites:
            sprites2.append((i.rect.x, i.rect.y, i.pos))
            if i.pos == 2:
                i.pos = 1
                i.image = pygame.transform.rotate(
                    i.image,
                    90
                )
                i.rect[2] = i.image.get_size()[0]
                i.rect[3] = i.image.get_size()[1]
            i.rect.x = i.start_xy[0]
            i.rect.y = i.start_xy[1]
        board.board = [[0] * board.width for _ in range(board.height)]
        #new_sprites()
        for i in all_sprites:
            pass
        board2 = Board(720, 100)
        flag_board2 = True
        board.board = matrix1
        for i in all_sprites:
            i.rect.x = sprites1[list(all_sprites).index(i)][0]
            i.rect.y = sprites1[list(all_sprites).index(i)][1]
            if i.pos != sprites1[list(all_sprites).index(i)][2]:
                if i.pos == 1:
                    i.pos = 2
                else:
                    i.pos = 1
                i.image = pygame.transform.rotate(
                    i.image,
                    90
                )
                i.rect[2] = i.image.get_size()[0]
                i.rect[3] = i.image.get_size()[1]
        board2.board = matrix2
        for i in all_sprites2:
            i.rect.x = sprites2[list(all_sprites2).index(i)][0] + 640
            i.rect.y = sprites2[list(all_sprites2).index(i)][1]
            if i.pos != sprites2[list(all_sprites2).index(i)][2]:
                if i.pos == 1:
                    i.pos = 2
                else:
                    i.pos = 1
                i.image = pygame.transform.rotate(
                    i.image,
                    90
                )
                i.rect[2] = i.image.get_size()[0]
                i.rect[3] = i.image.get_size()[1]
        flag_move = False
        game_started_flag = True
bg_surf = pygame.image.load("kartinki/bg.png")
bg = bg_surf.get_rect(bottomright=(480, 500))
bg2 = bg_surf.get_rect(bottomright=(1120, 500))
big_bg_surf = pygame.image.load("kartinki/big_bg.png")
big_bg = big_bg_surf.get_rect(bottomright=(1200, 600))
big_bg2_surf = pygame.image.load("kartinki/big_bg2.png")
big_bg2 = big_bg2_surf.get_rect(bottomright=(1200, 600))

win1_surf = pygame.image.load("kartinki/final_1_win.png")
winner1 = win1_surf.get_rect(bottomright=(1200, 600))
win2_surf = pygame.image.load("kartinki/final_2_win.png")
winner2 = win2_surf.get_rect(bottomright=(1200, 600))
winning = True

hacker_surf = pygame.image.load("kartinki/hacker.png")
hacker = win2_surf.get_rect(bottomright=(1200, 600))


class Sprite(pygame.sprite.Sprite):
    def __init__(self, place, start_xy, x, y, name_kartinki, number, pos, *group):
        super().__init__(*group)
        self.place = place
        self.start_xy = start_xy
        self.pos = pos
        self.number = number
        self.name_image = name_kartinki
        self.image = load_image(name_kartinki)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.koords_x = x
        self.koords_y = y


class Board:
    # создание поля
    def __init__(self, left, top):
        self.width = 10
        self.height = 10

        # главная матрица
        self.board = [[0] * self.width for _ in range(self.height)]

        # значения по умолчанию
        self.left = left
        self.top = top
        self.cell_size = 40

        self.dirt = load_image("miss.png")
        self.grass = load_image("grass.png")
        self.dirt_hit = load_image("dirt_hit.png")
        self.hit = load_image("hit.png")

    # отрисовка поля
    def render(self, screen):
        self.board_render(screen)

    def board_render(self, screen):
        # список с клетками (x, y, x1, y1, (pos_x, pos_y))
        self.kletki = []
        for i in range(self.width):
            for h in range(self.height):
                if self.board[i][h] == 0 or self.board[i][h] == 1:
                    # создание пустого поля
                    screen.blit(self.grass, (
                        self.left + self.cell_size * i,
                        self.top + self.cell_size * h,
                        self.cell_size, self.cell_size
                    ))
                if self.board[i][h] == 2:
                    # создание пустого поля
                    screen.blit(self.dirt, (
                        self.left + self.cell_size * i,
                        self.top + self.cell_size * h,
                        self.cell_size, self.cell_size
                    ))
                if self.board[i][h] == 3:
                    # создание пустого поля
                    screen.blit(self.dirt_hit, (
                        self.left + self.cell_size * i,
                        self.top + self.cell_size * h,
                        self.cell_size, self.cell_size
                    ))
                if self.board[i][h] == 4:
                    # создание пустого поля
                    screen.blit(self.hit, (
                        self.left + self.cell_size * i,
                        self.top + self.cell_size * h,
                        self.cell_size, self.cell_size
                    ))
                    # пополнение kletki
                self.kletki.append([
                    self.left + self.cell_size * i,
                    self.top + self.cell_size * h,
                    self.left + self.cell_size * (i + 1),
                    self.top + self.cell_size * (h + 1), (i, h)
                ])

    # def sprites_render(self, screen):

    # получение позиции клетки
    def get_cell(self, mouse_pos):
        flag = True
        # проверка находится ли клик мышки в поле
        for i in range(len(self.kletki)):
            if mouse_pos[0] in range(
                    self.kletki[i][0],
                    self.kletki[i][2]
            ) and mouse_pos[1] in range(self.kletki[i][1], self.kletki[i][3]):
                flag = False

    # изменить значения по умолчанию
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
    # def sprites_render


ant1 = Sprite(True, (600, 140), 600, 140, "ant.png", 1, 1, all_sprites)
ant2 = Sprite(True, (680, 140), 680, 140, "ant.png", 1, 1, all_sprites)
ant3 = Sprite(True, (760, 140), 760, 140, "ant.png", 1, 1, all_sprites)
ant4 = Sprite(True,(840, 140), 840, 140, "ant.png", 1, 1, all_sprites)
caterpillar1 = Sprite(True, (600, 240), 600, 240, "bug.png", 2, 1, all_sprites)
caterpillar2 = Sprite(True, (720, 240), 720, 240, "bug.png", 2, 1, all_sprites)
caterpillar3 = Sprite(True, (840, 240), 840, 240, "bug.png", 2, 1, all_sprites)
worm1 = Sprite(True, (600, 320), 600, 320, "worm.png", 3, 1, all_sprites)
worm2 = Sprite(True, (760, 320), 760, 320, "worm.png", 3, 1, all_sprites)
snake1 = Sprite(True, (600, 410), 600, 410, "snake.png", 4, 1, all_sprites)

ant1_2 = Sprite(True, (600, 140), 0, 0, "ant.png", 1, 1, all_sprites2)
ant2_2 = Sprite(True, (680, 140), 0, 0, "ant.png", 1, 1, all_sprites2)
ant3_2 = Sprite(True, (760, 140), 0, 0, "ant.png", 1, 1, all_sprites2)
ant4_2 = Sprite(True, (840, 140), 0, 0, "ant.png", 1, 1, all_sprites2)
caterpillar1_2 = Sprite(True, (600, 240), 0, 0, "bug.png", 2, 1, all_sprites2)
caterpillar2_2 = Sprite(True, (720, 240), 0, 0, "bug.png", 2, 1, all_sprites2)
caterpillar3_2 = Sprite(True, (840, 240), 0, 0, "bug.png", 2, 1, all_sprites2)
worm1_2 = Sprite(True, (600, 320), 0, 0, "worm.png", 3, 1, all_sprites2)
worm2_2 = Sprite(True, (760, 320), 0, 0, "worm.png", 3, 1, all_sprites2)
snake1_2 = Sprite(True, (600, 410), 0, 0, "snake.png", 4, 1, all_sprites2)
def digging(j, board, i):
    if j.number == 1:
        if (j.rect.x == i[0] and j.rect.y == i[1] 
            and board.board[i[4][0]][i[4][1]] == 3):
            board.board[i[4][0]][i[4][1]] = 4
    if j.number == 2:
        if j.pos == 1:
            if j.rect.x == i[0] and j.rect.y == i[1]:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0] + 1][i[4][1]] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0] + 1][i[4][1]] = 4
            if j.rect.x == i[0] - 40 and j.rect.y == i[1]:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0] - 1][i[4][1]] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0] - 1][i[4][1]] = 4
        if j.pos == 2:
            if j.rect.x == i[0] and j.rect.y == i[1]:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0]][i[4][1] + 1] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0]][i[4][1] + 1] = 4
            if j.rect.x == i[0] and j.rect.y == i[1] - 40:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0]][i[4][1] - 1] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0]][i[4][1] - 1] = 4
    if j.number == 3:
        if j.pos == 1:
            if j.rect.x == i[0] and j.rect.y == i[1]:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0] + 1][i[4][1]] == 3 
                    and board.board[i[4][0] + 2][i[4][1]] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0] + 1][i[4][1]] = 4
                    board.board[i[4][0] + 2][i[4][1]] = 4
            if j.rect.x == i[0] - 40 and j.rect.y == i[1]:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0] - 1][i[4][1]] == 3 
                    and board.board[i[4][0] + 1][i[4][1]] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0] - 1][i[4][1]] = 4
                    board.board[i[4][0] + 1][i[4][1]] = 4
            if j.rect.x == i[0] - 80 and j.rect.y == i[1]:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0] - 1][i[4][1]] == 3 
                    and board.board[i[4][0] - 2][i[4][1]] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0] - 1][i[4][1]] = 4
                    board.board[i[4][0] - 2][i[4][1]] = 4
        if j.pos == 2:
            if j.rect.x == i[0] and j.rect.y == i[1]:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0]][i[4][1] + 1] == 3 
                    and board.board[i[4][0]][i[4][1] + 2] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0]][i[4][1] + 1] = 4
                    board.board[i[4][0]][i[4][1] + 2] = 4
            if j.rect.x == i[0] and j.rect.y == i[1] - 40:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0]][i[4][1] - 1] == 3 
                    and board.board[i[4][0]][i[4][1] + 1] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0]][i[4][1] - 1] = 4
                    board.board[i[4][0]][i[4][1] + 1] = 4
            if j.rect.x == i[0] and j.rect.y == i[1] - 80:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0]][i[4][1] - 1] == 3 
                    and board.board[i[4][0]][i[4][1] - 2] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0]][i[4][1] - 1] = 4
                    board.board[i[4][0]][i[4][1] - 2] = 4
    if j.number == 4:
        if j.pos == 1:
            if j.rect.x == i[0] and j.rect.y == i[1]:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0] + 1][i[4][1]] == 3 
                    and board.board[i[4][0] + 2][i[4][1]] == 3 
                    and board.board[i[4][0] + 3][i[4][1]] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0] + 1][i[4][1]] = 4
                    board.board[i[4][0] + 2][i[4][1]] = 4
                    board.board[i[4][0] + 3][i[4][1]] = 4
            if j.rect.x == i[0] - 40 and j.rect.y == i[1]:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0] - 1][i[4][1]] == 3 
                    and board.board[i[4][0] + 1][i[4][1]] == 3 
                    and board.board[i[4][0] + 2][i[4][1]] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0] - 1][i[4][1]] = 4
                    board.board[i[4][0] + 1][i[4][1]] = 4
                    board.board[i[4][0] + 2][i[4][1]] = 4
            if j.rect.x == i[0] - 80 and j.rect.y == i[1]:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0] - 1][i[4][1]] == 3 
                    and board.board[i[4][0] - 2][i[4][1]] == 3 
                    and board.board[i[4][0] + 1][i[4][1]] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0] - 1][i[4][1]] = 4
                    board.board[i[4][0] - 2][i[4][1]] = 4
                    board.board[i[4][0] + 1][i[4][1]] = 4
            if j.rect.x == i[0] - 120 and j.rect.y == i[1]:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0] - 1][i[4][1]] == 3 
                    and board.board[i[4][0] - 2][i[4][1]] == 3 
                    and board.board[i[4][0] - 3][i[4][1]] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0] - 1][i[4][1]] = 4
                    board.board[i[4][0] - 2][i[4][1]] = 4
                    board.board[i[4][0] - 3][i[4][1]] = 4
        if j.pos == 2:
            if j.rect.x == i[0] and j.rect.y == i[1]:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0]][i[4][1] + 1] == 3 
                    and board.board[i[4][0]][i[4][1] + 2] == 3 
                    and board.board[i[4][0]][i[4][1] + 3] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0]][i[4][1] + 1] = 4
                    board.board[i[4][0]][i[4][1] + 2] = 4
                    board.board[i[4][0]][i[4][1] + 3] = 4
            if j.rect.x == i[0] and j.rect.y == i[1] - 40:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0]][i[4][1] - 1] == 3 
                    and board.board[i[4][0]][i[4][1] + 1] == 3 
                    and board.board[i[4][0]][i[4][1] + 2] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0]][i[4][1] - 1] = 4
                    board.board[i[4][0]][i[4][1] + 1] = 4
                    board.board[i[4][0]][i[4][1] + 2] = 4
            if j.rect.x == i[0] and j.rect.y == i[1] - 80:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0]][i[4][1] - 1] == 3 
                    and board.board[i[4][0]][i[4][1] - 2] == 3 
                    and board.board[i[4][0]][i[4][1] + 1] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0]][i[4][1] - 1] = 4
                    board.board[i[4][0]][i[4][1] - 2] = 4
                    board.board[i[4][0]][i[4][1] + 1] = 4
            if j.rect.x == i[0] and j.rect.y == i[1] - 120:
                if (board.board[i[4][0]][i[4][1]] == 3 
                    and board.board[i[4][0]][i[4][1] - 1] == 3 
                    and board.board[i[4][0]][i[4][1] - 2] == 3 
                    and board.board[i[4][0]][i[4][1] - 3] == 3):
                    board.board[i[4][0]][i[4][1]] = 4
                    board.board[i[4][0]][i[4][1] - 1] = 4
                    board.board[i[4][0]][i[4][1] - 2] = 4
                    board.board[i[4][0]][i[4][1] - 3] = 4


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1200, 600
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    board = Board(80, 100)
    running = True
    mouse_flag = False
    sprite_now = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    insects_ready = True
                    for i in all_sprites:
                        if i.place == True:
                            insects_ready = False

                    if insects_ready is True:
                        if game_started_flag is False:
                            hide()

            if game_started_flag is False:
                if (event.type == pygame.MOUSEBUTTONDOWN
                        and pygame.mouse.get_pressed()[0]
                        and event.button == 1):
                        sprite_now = None
                        for i in all_sprites:
                            if (event.pos[0] >= i.rect.x
                                    and event.pos[1] >= i.rect.y
                                    and event.pos[1] <= i.rect.y \
                                    + i.image.get_size()[1]
                                    and event.pos[0] <= i.rect.x \
                                    + i.image.get_size()[0]):
                                sprite_now = i
                                change_matrix(sprite_now, board, sprite_now.number, 0)
                                mouse_flag = True

                if mouse_flag:
                    sprite_now.place = True
                    if event.type == pygame.MOUSEMOTION:
                        #if (40 >= event.pos[0] >= 1160
                            #and 40 >= event.pos[1] >= 560):
                        sprite_now.rect.x = event.pos[0] \
                                    - sprite_now.image.get_size()[0] / 2
                        sprite_now.rect.y = event.pos[1] \
                                    - sprite_now.image.get_size()[1] / 2

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                        sprite_now.image = pygame.transform.rotate(
                            sprite_now.image,
                            90
                        )
                        sprite_now.rect[2] = sprite_now.image.get_size()[0]
                        sprite_now.rect[3] = sprite_now.image.get_size()[1]
                        if sprite_now.pos == 1:
                            sprite_now.pos = 2
                        else:
                            sprite_now.pos = 1

                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        mouse_flag = False
                        if (480 >= sprite_now.rect.x + 10 >= 80 
                            and 500 >= sprite_now.rect.y + 10 >= 100 
                            and 480 >= sprite_now.rect.x \
                            + sprite_now.image.get_size()[0] - 10 >= 80 
                            and 500 >= sprite_now.rect.y \
                            + sprite_now.image.get_size()[1] - 10 >= 100):
                            for i in board.kletki:
                                kletki_x = i[4][0]
                                kletki_y = i[4][1]
                                if (i[2] >= sprite_now.rect.x + 10 >= i[0] 
                                    and i[3] >= sprite_now.rect.y + 10 >= i[1]):
                                    if sprite_now.number == 1:
                                        if board.board[kletki_x][kletki_y] == 0:
                                            sprite_now.rect.x = i[0]
                                            sprite_now.rect.y = i[1]
                                            sprite_now.place = False
                                            change_matrix(sprite_now, board, 1, 1)
                                        else:
                                            sprite_now.rect.x = sprite_now.koords_x
                                            sprite_now.rect.y = sprite_now.koords_y                                            
                                    if sprite_now.number == 2:
                                        if sprite_now.pos == 1:
                                            if (board.board[kletki_x][kletki_y] == 0 
                                                and board.board[kletki_x + 1][kletki_y] == 0):
                                                sprite_now.rect.x = i[0]
                                                sprite_now.rect.y = i[1]
                                                sprite_now.place = False
                                                change_matrix(sprite_now, board, 2, 1)
                                            else:
                                                sprite_now.rect.x = sprite_now.koords_x
                                                sprite_now.rect.y = sprite_now.koords_y
                                        if sprite_now.pos == 2:
                                            if (board.board[kletki_x][kletki_y] == 0 
                                                and board.board[kletki_x][kletki_y + 1] == 0):
                                                sprite_now.rect.x = i[0]
                                                sprite_now.rect.y = i[1]
                                                sprite_now.place = False
                                                change_matrix(sprite_now, board, 2, 1)
                                            else:
                                                sprite_now.rect.x = sprite_now.koords_x
                                                sprite_now.rect.y = sprite_now.koords_y
                                    if sprite_now.number == 3:
                                        if sprite_now.pos == 1:
                                            if (board.board[kletki_x][kletki_y] == 0 
                                                and board.board[kletki_x + 1][kletki_y] == 0 
                                                and board.board[kletki_x + 2][kletki_y] == 0):
                                                sprite_now.rect.x = i[0]
                                                sprite_now.rect.y = i[1]
                                                sprite_now.place = False
                                                change_matrix(sprite_now, board, 3, 1)
                                            else:
                                                sprite_now.rect.x = sprite_now.koords_x
                                                sprite_now.rect.y = sprite_now.koords_y
                                        if sprite_now.pos == 2:
                                            if (board.board[kletki_x][kletki_y] == 0 
                                                and board.board[kletki_x][kletki_y + 1] == 0 
                                                and board.board[kletki_x][kletki_y + 2] == 0):
                                                sprite_now.rect.x = i[0]
                                                sprite_now.rect.y = i[1]
                                                sprite_now.place = False
                                                change_matrix(sprite_now, board, 3, 1)
                                            else:
                                                sprite_now.rect.x = sprite_now.koords_x
                                                sprite_now.rect.y = sprite_now.koords_y
                                    if sprite_now.number == 4:
                                        if sprite_now.pos == 1:
                                            if (board.board[kletki_x][kletki_y] == 0 
                                                and board.board[kletki_x + 1][kletki_y] == 0 
                                                and board.board[kletki_x + 2][kletki_y] == 0 
                                                and board.board[kletki_x + 3][kletki_y] == 0):
                                                sprite_now.rect.x = i[0]
                                                sprite_now.rect.y = i[1]
                                                sprite_now.place = False
                                                change_matrix(sprite_now, board, 4, 1)
                                            else:
                                                sprite_now.rect.x = sprite_now.koords_x
                                                sprite_now.rect.y = sprite_now.koords_y
                                        if sprite_now.pos == 2:
                                            if (board.board[kletki_x][kletki_y] == 0 
                                                and board.board[kletki_x][kletki_y + 1] == 0 
                                                and board.board[kletki_x][kletki_y + 2] == 0 
                                                and board.board[kletki_x][kletki_y + 3] == 0):
                                                sprite_now.rect.x = i[0]
                                                sprite_now.rect.y = i[1]
                                                sprite_now.place = False
                                                change_matrix(sprite_now, board, 4, 1)
                                            else:
                                                sprite_now.rect.x = sprite_now.koords_x
                                                sprite_now.rect.y = sprite_now.koords_y
                        else:                             
                            sprite_now.rect.x = sprite_now.koords_x
                            sprite_now.rect.y = sprite_now.koords_y
                             


            if game_started_flag is True:
                if pygame.mouse.get_focused() == True and (win2 != 20 and win != 20):
                    pygame.mouse.set_visible(False)
                    image_kursor = load_image("kursor.png")
                    x_kursor, y_kursor = pygame.mouse.get_pos()
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if now_player == 1:
                        for i in board.kletki:
                            if (i[0] <= event.pos[0] and i[1] <= event.pos[1] 
                                and i[2] >= event.pos[0] 
                                and i[3] >= event.pos[1]):
                                if board.board[i[4][0]][i[4][1]] == 0:
                                    if win2 < 20 and win < 20:
                                        digging_sound.play()
                                    board.board[i[4][0]][i[4][1]] = 2
                                    create_particles(pygame.mouse.get_pos())
                                    change_player()
                                if board.board[i[4][0]][i[4][1]] == 1:
                                    if win2 < 20 and win < 20:
                                        digging_sound.play()
                                    board.board[i[4][0]][i[4][1]] = 3
                                    create_particles(pygame.mouse.get_pos())
                                    win += 1
                                for j in all_sprites:
                                    digging(j, board, i)
                    elif now_player == 2:
                        for i in board2.kletki:
                            if (i[0] <= event.pos[0] and i[1] <= event.pos[1] 
                                and i[2] >= event.pos[0] 
                                and i[3] >= event.pos[1]):
                                if board2.board[i[4][0]][i[4][1]] == 0:
                                    if win2 < 20 and win < 20:
                                        digging_sound.play()
                                    board2.board[i[4][0]][i[4][1]] = 2
                                    create_particles(pygame.mouse.get_pos())
                                    change_player()
                                if board2.board[i[4][0]][i[4][1]] == 1:
                                    if win2 < 20 and win < 20:
                                        digging_sound.play()
                                    board2.board[i[4][0]][i[4][1]] = 3
                                    create_particles(pygame.mouse.get_pos())
                                    win2 += 1
                                for j in all_sprites2:
                                    digging(j, board2, i)

        if game_started_flag is False:
            screen.blit(big_bg_surf, big_bg)
        else:
            screen.blit(big_bg2_surf, big_bg2)
        game_font = pygame.font.Font("freesansbold.ttf", 32)

        if flag_board2 is True:
            screen.blit(bg_surf, bg)
            screen.blit(bg_surf, bg2)
            all_sprites2.draw(screen)
            board2.render(screen)
        if game_started_flag is False:
            pygame.mixer.music.unpause()
            board.render(screen)
        all_sprites.draw(screen)
        if game_started_flag is True:
            chey_hod = game_font.render(strelka, False, (31, 63, 18))
            screen.blit(chey_hod, (560, 265))
            player1_text = game_font.render("PLAYER 1", False, (156, 0, 0))
            screen.blit(player1_text, (100, 40))
            player2_text = game_font.render("PLAYER 2", False, (28, 0, 155))
            screen.blit(player2_text, (740, 40))
            all_sprites3.update()
            board.render(screen)
            all_sprites3.draw(screen)
            clock.tick(50)
            screen.blit(image_kursor, (x_kursor, y_kursor))
        if win == 20:
            pygame.mixer.music.pause()
            if winning:
                win_sound.play()
                winning = False
            screen.blit(win2_surf, winner2)
            pygame.mouse.set_visible(True)
        if win2 == 20:
            pygame.mixer.music.pause()
            if winning:
                win_sound.play()
                winning = False
            screen.blit(win1_surf, winner1)
            pygame.mouse.set_visible(True)
        if win2 == 20 and win == 20:
            screen.blit(hacker_surf, hacker)
            pygame.mouse.set_visible(True)
        pygame.display.flip()
    pygame.quit()