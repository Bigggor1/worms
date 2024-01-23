import os
import sys
import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites1)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

def terminate():
    pygame.quit()
    sys.exit()

def load_image(name, colorkey=None):
    fullname = os.path.join('kartinki', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def start_screen():
    global  all_sprites1, dragon
    clock = pygame.time.Clock()
    pygame.display.set_caption('Бой букашек')
    all_sprites1 = pygame.sprite.Group()
    screen = pygame.display.set_mode((1200, 600))
    dragon = AnimatedSprite(load_image("dragon_sheet8x2.png"), 8, 2, 200, 350)
    fon = pygame.transform.scale(load_image('начальный_экран.png'), (1200, 600))
    screen.blit(fon, (0, 0))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                running = False
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return 'start'
        all_sprites1.update()
        all_sprites1.draw(screen)
        pygame.display.flip()
        clock.tick(20)
        pygame.display.update()
    pygame.quit()

print(start_screen())