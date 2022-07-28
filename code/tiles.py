from tabnanny import check
import pygame
from settings import tile_size

class Tile(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y, goal):
        super().__init__()
        self.image = pygame.Surface((w * tile_size, h * tile_size))
        self.image.fill('burlywood')

        # borders
        pygame.draw.rect(self.image, 'black', self.image.get_rect(), 1)

        # circle at center
        size = (w,h)
        if size in [(1,2), (2,1)]:
            color_center = 'red'
        elif size == (1,1):
            color_center = 'yellow'
        elif size == (2,2):
            color_center = 'green'
        else:
            color_center = 'black'
        pygame.draw.circle(self.image, color_center, (w * tile_size / 2, h * tile_size / 2), tile_size / 3)

        # goal tile
        self.goal_tile = goal

        self.rect = self.image.get_rect(topleft = (x * tile_size,y * tile_size))

    def offset(self, x, y):
        self.rect.move_ip(x, y)

class Board(pygame.sprite.Sprite):
    def __init__(self, border_thickness, board_dimensions):
        super().__init__()

        self.image = pygame.Surface((
            2 * border_thickness + board_dimensions[0] * tile_size,
            2 * border_thickness + board_dimensions[1] * tile_size),
            flags= pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        # for collisions detection
        self.collision_rects = []
        board_width = 4 * tile_size + 2 * border_thickness
        board_height = 5 * tile_size + 2 * border_thickness
        board_borders = [
            [0, 0, board_width, border_thickness],
            [0, 0, border_thickness, board_height],
            [board_width - border_thickness, 0, border_thickness, board_height],
            [border_thickness, board_height - border_thickness, tile_size, border_thickness],
            [border_thickness + tile_size * 3, board_height - border_thickness, tile_size, border_thickness]
        ]
        for x, y, w, h in board_borders:
            rect = pygame.Rect(x, y, w, h)
            self.collision_rects.append(rect)

        # collision for exit
        self.exit_rect = pygame.Rect(
            border_thickness + tile_size,
            board_height - border_thickness,
            2 * tile_size,
            border_thickness
        )

        # make visual
        for rect in self.collision_rects:
            pygame.draw.rect(self.image, 'burlywood4', rect)
        
        pygame.draw.rect(self.image, 'burlywood3', self.exit_rect)
