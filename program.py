import pygame
import os
import sys
from random import *


FPS = 50
WIDTH, HEIGHT = 1280, 720
clock = pygame.time.Clock()
# инициализация
pygame.init()
size = width, height = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Перемещение героя')


def load_image(name, colorkey=None):
    # локальное имя
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    # загрузка изображения
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            # первый пиксель
            colorkey = image.get_at((0, 0))
        # прозрачность фона
        image.set_colorkey(colorkey)
    else:
        #  сохранение прозрачности
        image = image.convert_alpha()
    # возвращение картинки
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.x, self.y = pos_x, pos_y

    def move(self, event):
        if event.key == pygame.K_LEFT:
            if self.x > 0 and (level_map[self.y][self.x - 1] == '.' or level_map[self.y][self.x - 1] == '@'):
                self.x -= 1
                self.rect.x -= tile_width
        if event.key == pygame.K_RIGHT:
            if self.x < level_x and (level_map[self.y][self.x + 1] == '.' or level_map[self.y][self.x + 1] == '@'):
                self.x += 1
                self.rect.x += tile_width
        if event.key == pygame.K_UP:
            if self.y > 0 and (level_map[self.y - 1][self.x] == '.' or level_map[self.y - 1][self.x] == '@'):
                self.y -= 1
                self.rect.y -= tile_height
        if event.key == pygame.K_DOWN:
            if self.y < level_y and (level_map[self.y + 1][self.x] == '.' or level_map[self.y + 1][self.x] == '@'):
                self.y += 1
                self.rect.y += tile_height


# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


level_map = load_level('map.txt')

if __name__ == '__main__':
    running = True

    player, level_x, level_y = generate_level(load_level('map.txt'))

    # создадим группу, содержащую все спрайты
    all_sprites = pygame.sprite.Group()

    start_screen()

    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)

    while running:
        screen.fill(pygame.Color('black'))
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                player.move(event)

        tiles_group.draw(screen)
        player_group.draw(screen)
        all_sprites.draw(screen)

        pygame.display.flip()
    pygame.quit()
