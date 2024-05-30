import random

import pygame.mixer
from pygame import mixer
from settings import *

icon = pygame.image.load('img/Cat1.png')
pygame.display.set_icon(icon)

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()


class Game:
    def __init__(self):
        # Инициализация
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((Width, Height))
        pg.display.set_caption(Title)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FontName)

    def new(self):
        # Запуск новой игры
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        pg.mixer.music.load('music/OST.mp3')
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.4)
        self.run()

    def run(self):
        # Игровой цикл
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Игровой цикл - Update
        self.all_sprites.update()
        # Проверка, ударяется ли игрок о платформу - (только если падает)
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

        # Если игрок достигнет 1/4 верхней части экрана
        if self.player.rect.top <= Height / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= Height:
                    plat.kill()
                    self.score += 10

        # Смерть
        if self.player.rect.bottom > Height:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # Создавать новые платформы, чтобы сохранить среднее число
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            height = 30 - round(self.score/10)
            if height < 1:
                height = 1
            p = Platform(random.randrange(0, Width - width),
                         random.randrange(-75, -30),
                         width, height)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        # Игровой цикл - events
        for event in pg.event.get():
            # Проверить закрытие окна
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Игровой цикл - draw
        self.screen.fill(SkyBlue)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, White, Width / 2, 15)
        pg.display.flip()

    def show_start_screen(self):
        # Стартовый экран
        pass

    def show_go_screen(self):
        # Продолжить/закончить
        pass

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
