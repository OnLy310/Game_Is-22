import pygame as pg
vec = pg.math.Vector2

Title = "Only Jump!"
Width = 480
Height = 600
FPS = 60
FontName = 'arial'

# Свойства игрока
PLAYER_ACC = 0.7
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# Начальные платформы
PLATFORM_LIST = [(0, Height - 40, Width, 40),
                 (Width / 2 - 50, Height * 3 / 4, 100, 30),
                 (125, Height - 350, 100, 30),
                 (350, 200, 100, 30),
                 (175, 100, 50, 30)]

# Цвета
White = (255, 255, 255)
Gray = (236, 236, 236)
SkyBlue = (30, 205, 255)


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load('img/Cat1.png')
        self.rect = self.image.get_rect()
        self.rect.center = (Width / 2, Height / 2)
        self.pos = vec(Width / 2, Height / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        # Прыгать, только если на платформе
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # Трение
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # Уравнения движения
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > Width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = Width

        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(Gray)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
