import pygame
from sys import exit
from settings import screen_width, screen_height, tiles_map, exit_point, board_dimensions
from level import Level

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

level = Level(screen, board_dimensions, tiles_map, exit_point)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('grey')

    level.run()

    pygame.display.flip()
    clock.tick(60)
