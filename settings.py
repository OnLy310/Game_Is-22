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
        self.rect = self.image.get_rect()   # Получение прямоугольника (rect) изображения, который используется для
                                            # определения положения и столкновений.
        self.rect.center = (Width / 2, Height / 2) # Установка начального положения игрока в центре экрана.
        self.pos = vec(Width / 2, Height / 2) # Позиция игрока как 2D-вектор.
        self.vel = vec(0, 0) # Скорость игрока как 2D-вектор.
        self.acc = vec(0, 0) # Ускорение игрока как 2D-вектор.

    def jump(self):
        # Прыгать, только если на платформе
        self.rect.x += 1 # Сдвиг прямоугольника Playera на 1 пиксель вправо для проверки столкновения.
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)  # Если столкновение есть, возвращаем
                                                                                # список столкновений.
        self.rect.x -= 1 # Возвращаем игрока на место после проверки.
        if hits:
            self.vel.y = -PLAYER_JUMP # Вертикальная скорость игрока для прыжка

    def update(self):
        self.acc = vec(0, PLAYER_GRAV) # Ускорение под действием гравитации.
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
