import pygame
import sys
from random import choice

ENEMY_GO = pygame.USEREVENT + 1


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.life = 1
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.x = pos_x
        self.y = pos_y
        # pygame.display.flip()

    def get_coords(self):
        return self.x, self.y

    def move(self, direction):
        if self.life == 0:
            return
        old_x, old_y = self.x, self.y
        if direction == 'up' and level[self.y - 1][self.x] != '#':
            self.y -= 1
        if direction == 'down' and level[self.y + 1][self.x] != '#':
            self.y += 1
        if direction == 'left' and level[self.y][self.x - 1] != '#':
            self.x -= 1
        if direction == 'right' and level[self.y][self.x + 1] != '#':
            self.x += 1
        if old_y != self.y:
            level_list_row_old = list(level[old_y])
            level_list_row = list(level[self.y])
            level_list_row[self.x] = '@'
            level_list_row_old[old_x] = '.'
            level[self.y] = ''.join(level_list_row)
            level[old_y] = ''.join(level_list_row_old)
        else:
            level_list_row = list(level[self.y])
            level_list_row[self.x] = '@'
            level_list_row[old_x] = '.'
            level[self.y] = ''.join(level_list_row)

        self.rect = self.image.get_rect().move(tile_width * self.x + 15, tile_height * self.y + 5)
        # print('ENEMY', enemy.get_coords())
        # print('PLAYER', self.x, self.y)

        if enemy.get_coords() == (self.x, self.y):
            game_over()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = enemy_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.x = pos_x
        self.y = pos_y

    def get_coords(self):
        return self.x, self.y

    def move(self, direction):
        is_success = False
        old_x, old_y = self.x, self.y
        if direction == 'up' and level[self.y - 1][self.x] != '#':
            self.y -= 1
            is_success = True
        if direction == 'down' and level[self.y + 1][self.x] != '#':
            self.y += 1
            is_success = True
        if direction == 'left' and level[self.y][self.x - 1] != '#':
            self.x -= 1
            is_success = True
        if direction == 'right' and level[self.y][self.x + 1] != '#':
            self.x += 1
            is_success = True
        if is_success:
            self.rect = self.image.get_rect().move(tile_width * self.x + 15, tile_height * self.y + 5)
            if old_y != self.y:
                level_list_row_old = list(level[old_y])
                level_list_row = list(level[self.y])
                level_list_row[self.x] = '?'
                level_list_row_old[old_x] = '.'
                level[self.y] = ''.join(level_list_row)
                level[old_y] = ''.join(level_list_row_old)
            else:
                level_list_row = list(level[self.y])
                level_list_row[self.x] = '?'
                level_list_row[old_x] = '.'
                level[self.y] = ''.join(level_list_row)
            # print(*level, sep='\n')
            
            

        if player.get_coords() == (self.x, self.y):
            game_over()
        return is_success

    def choice_move(self):
        see_coords = [('up', level[self.y - 1][self.x]),
                      ('up', level[self.y - 2][self.x]),
                      ('down', level[self.y + 1][self.x]),
                      ('down', level[self.y + 2][self.x]),
                      ('left', level[self.y][self.x - 1]),
                      ('left', level[self.y][self.x - 2]),
                      ('right', level[self.y][self.x + 1]),
                      ('right', level[self.y][self.x + 2]),
                      ('lup', level[self.y - 1][self.x - 1]),
                      ('rup', level[self.y + 1][self.x - 1]),
                      ('ldown', level[self.y + 1][self.x - 1]),
                      ('rdown', level[self.y + 1][self.x + 1]),
                      ('lup', level[self.y - 2][self.x - 2]),
                      ('rup', level[self.y + 2][self.x - 2]),
                      ('ldown', level[self.y + 2][self.x - 2]),
                      ('rdown', level[self.y + 2][self.x + 2])]
        moved_1, moved_2 = False, False
        for move, coord in see_coords:
            if coord == '@':
                print('detected player')
                moved_1, moved_2 = False, True
                if move == 'up':
                    moved_1 = self.move('up')
                elif move == 'down':
                    moved_1 = self.move('down')
                elif move == 'left':
                    moved_1 = self.move('left')
                elif move == 'right':
                    moved_1 = self.move('right')
                elif move == 'ldown':
                    moved_1 = self.move('left')
                    moved_2 = self.move('down')
                elif move == 'rdown':
                    moved_1 = self.move('right')
                    moved_2 = self.move('down')
                elif move == 'lup':
                    moved_1 = self.move('left')
                    moved_2 = self.move('up')
                elif move == 'ldown':
                    moved_1 = self.move('left')
                    moved_2 = self.move('down')
        if moved_1 or moved_2:
            print('attack!')
        elif not self.move(choice(['up', 'down', 'right', 'left'])):
            available_coords = {'up': level[self.y - 1][self.x],
                                'down': level[self.y + 1][self.x],
                                'left': level[self.y][self.x - 1],
                                'right': level[self.y][self.x + 1]}
            for move, coord in available_coords.items():
                if coord != '#' and coord != '?':
                    if move == 'up':
                        self.y -= 1
                    elif move == 'down':
                        self.y += 1
                    elif move == 'left':
                        self.x -= 1
                    elif move == 'right':
                        self.x += 1
                    break
            self.rect = self.image.get_rect().move(tile_width * self.x + 15, tile_height * self.y + 5)


def terminate():
    pygame.quit()
    sys.exit()


def game_over():
    player.life = 0
    print('game over!!!!')
    player_image = pygame.image.load('mar_dead.png')
    player.image = player_image


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Ходи, пока не поймает Гитлер.",
                  "Очень интересно и захватывающе."]

    fon = pygame.transform.scale(pygame.image.load('sozrel_vopros.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y, new_enemy = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '?':
                Tile('empty', x, y)
                new_enemy = Enemy(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, new_enemy


pygame.init()
size = WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()
pygame.time.set_timer(ENEMY_GO, 1000)
tile_images = {'wall': pygame.image.load('box.png'), 'empty': pygame.image.load('grass.png')}
player_image = pygame.image.load('mar.png')
enemy_image = pygame.image.load('enemy.png')
tile_width = tile_height = 50

player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

start_screen()
level = load_level('map.txt')
print(level)
player, level_x, level_y, enemy = generate_level(level)
pygame.display.flip()

while True:
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move('up')
            elif event.key == pygame.K_DOWN:
                player.move('down')
            elif event.key == pygame.K_RIGHT:
                player.move('right')
            elif event.key == pygame.K_LEFT:
                player.move('left')
        elif event.type == ENEMY_GO:
            enemy.choice_move()

    pygame.display.flip()
    clock.tick(FPS)
