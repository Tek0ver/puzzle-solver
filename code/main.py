import pygame
from sys import exit
from settings import tiles_map, exit_point, board_dimensions, tile_size, border_thickness
from level import Level

pygame.init()

def start_level():
    global level
    level = Level(screen, board_dimensions, border_thickness, tiles_map, exit_point, start_level)

# dynamic window dimensions
goal_tile = [tile for tile in tiles_map if tile[4] is True]
goal_tile_dimensions = (goal_tile[0][0], goal_tile[0][1])
screen_width = board_dimensions[0] * tile_size + 2 * border_thickness
screen_height = board_dimensions[1] * tile_size + 2 * border_thickness + goal_tile_dimensions[1] * tile_size

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

start_level()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('grey')

    level.run()

    pygame.display.flip()
    clock.tick(60)
