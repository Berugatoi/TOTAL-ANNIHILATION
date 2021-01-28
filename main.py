import sys
import os
import pygame
from random import randrange

pygame.init()
size = WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def terminate():
    pygame.quit()
    sys.exit()


def main_menu():
    click = False
    while True:

        screen.fill((0, 0, 0))

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(WIDTH // 2 - 100, 100, 200, 50)
        button_2 = pygame.Rect(WIDTH // 2 - 100, 250, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                main()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        draw_text('START', font, (255, 255, 255), screen, WIDTH // 2 - 30, 110)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(FPS)


def options():
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_text('options', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        pygame.display.update()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.GroupSingle()
mobs = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением \'{fullname}\' не найден')
        sys.exit()
    image = pygame.image.load(fullname)

    if color_key:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Player(pygame.sprite.Sprite):
    image = load_image('player.png')

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, player_sprite)
        self.image = Player.image
        self.pos = pos_x, pos_y
        self.rect = self.image.get_rect().move(self.pos)
        self.speed = 5
        self.hp = 100
        self.velocity = [0, 0]

    def get_damage(self, damage):
        self.hp -= damage

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.velocity[0] = -self.speed
        elif keystate[pygame.K_d]:
            self.velocity[0] = self.speed
        else:
            self.velocity[0] = 0

        if keystate[pygame.K_w]:
            self.velocity[1] = -self.speed
        elif keystate[pygame.K_s]:
            self.velocity[1] = self.speed
        else:
            self.velocity[1] = 0
        self.move(*self.velocity)

    def move(self, vx, vy):
        self.rect = self.rect.move(vx, vy)
        self.pos = self.rect.x, self.rect.y


player = Player(200, 300)


class Mob(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, mobs)
        self.pos = pos_x, pos_y
        self.image = load_image('player.png')
        self.rect = self.image.get_rect().move(self.pos)
        self.speed = 3
        self.hp = 40
        self.damage = 10
        self.velocity = [0, 0]

    def update(self):
        vx = player.pos[0] - self.pos[0]
        vy = player.pos[1] - self.pos[1]

        if vx == 0 or abs(vx) < self.speed:
            self.velocity[0] = 0
        elif vx < 0:
            self.velocity[0] = -self.speed
        elif vx > 0:
            self.velocity[0] = self.speed

        if vy == 0 or abs(vy) < self.speed:
            self.velocity[1] = 0
        elif vy < 0:
            self.velocity[1] = -self.speed
        elif vy > 0:
            self.velocity[1] = self.speed

        if pygame.sprite.spritecollide(self, player_sprite, False):
            self.velocity = [0, 0]
            player.get_damage(self.damage)
        self.move(*self.velocity)

    def move(self, vx, vy):
        self.rect = self.rect.move(vx, vy)
        self.pos = self.rect.x, self.rect.y


def main():
    global player
    mob = Mob(100, 100)
    while True:
        screen.fill((0, 0, 0))
        draw_text(str(player.hp), font, (255, 0, 0), screen, 20, 1040)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        all_sprites.draw(screen)
        all_sprites.update()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main_menu()