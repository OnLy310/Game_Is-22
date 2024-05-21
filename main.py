import pygame

pygame.init()

screen_width = 1900
screen_height = 990

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Kitty Manipulator')

running = True
while running:

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
